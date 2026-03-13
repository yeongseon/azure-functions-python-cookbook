"""Smoke tests for examples/ projects.

Each test dynamically imports the example's ``function_app.py`` module and
verifies that the Azure Functions app object and its registered functions
are accessible without crashing.
"""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import azure.functions as func

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def _load_example_module(example_name: str) -> Any:
    """Import an example's function_app.py and return the module."""
    module_path = EXAMPLES_DIR / example_name / "function_app.py"
    spec = spec_from_file_location(f"cookbook_example_{example_name}", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load example module from {module_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# http_api_basic
# ---------------------------------------------------------------------------


class TestHttpApiBasic:
    """Smoke tests for examples/http_api_basic."""

    def test_module_loads(self) -> None:
        module = _load_example_module("http_api_basic")
        assert hasattr(module, "app")

    def test_list_items_returns_json(self) -> None:
        module = _load_example_module("http_api_basic")
        req = func.HttpRequest(
            method="GET",
            url="/api/items",
            body=b"",
            headers={},
        )
        response = module.list_items(req)
        assert response.status_code == 200
        items = json.loads(response.get_body())
        assert isinstance(items, list)
        assert len(items) >= 2

    def test_get_item_found(self) -> None:
        module = _load_example_module("http_api_basic")
        req = func.HttpRequest(
            method="GET",
            url="/api/items/1",
            body=b"",
            headers={},
            route_params={"item_id": "1"},
        )
        response = module.get_item(req)
        assert response.status_code == 200
        item = json.loads(response.get_body())
        assert item["id"] == 1

    def test_get_item_not_found(self) -> None:
        module = _load_example_module("http_api_basic")
        req = func.HttpRequest(
            method="GET",
            url="/api/items/999",
            body=b"",
            headers={},
            route_params={"item_id": "999"},
        )
        response = module.get_item(req)
        assert response.status_code == 404

    def test_create_item(self) -> None:
        module = _load_example_module("http_api_basic")
        req = func.HttpRequest(
            method="POST",
            url="/api/items",
            body=json.dumps({"name": "Test", "category": "test"}).encode(),
            headers={"Content-Type": "application/json"},
        )
        response = module.create_item(req)
        assert response.status_code == 201
        created = json.loads(response.get_body())
        assert created["name"] == "Test"

    def test_create_item_missing_name(self) -> None:
        module = _load_example_module("http_api_basic")
        req = func.HttpRequest(
            method="POST",
            url="/api/items",
            body=json.dumps({}).encode(),
            headers={"Content-Type": "application/json"},
        )
        response = module.create_item(req)
        assert response.status_code == 400

    def test_delete_item(self) -> None:
        module = _load_example_module("http_api_basic")
        req = func.HttpRequest(
            method="DELETE",
            url="/api/items/1",
            body=b"",
            headers={},
            route_params={"item_id": "1"},
        )
        response = module.delete_item(req)
        assert response.status_code == 204


# ---------------------------------------------------------------------------
# http_api_openapi
# ---------------------------------------------------------------------------


class TestHttpApiOpenapi:
    """Smoke tests for examples/http_api_openapi."""

    def test_module_loads(self) -> None:
        module = _load_example_module("http_api_openapi")
        assert hasattr(module, "app")

    def test_list_products(self) -> None:
        module = _load_example_module("http_api_openapi")
        req = func.HttpRequest(
            method="GET",
            url="/api/products",
            body=b"",
            headers={},
        )
        response = module.list_products(req)
        assert response.status_code == 200
        products = json.loads(response.get_body())
        assert isinstance(products, list)

    def test_get_product_found(self) -> None:
        module = _load_example_module("http_api_openapi")
        req = func.HttpRequest(
            method="GET",
            url="/api/products/1",
            body=b"",
            headers={},
            route_params={"product_id": "1"},
        )
        response = module.get_product(req)
        assert response.status_code == 200
        product = json.loads(response.get_body())
        assert product["id"] == 1

    def test_get_product_not_found(self) -> None:
        module = _load_example_module("http_api_openapi")
        req = func.HttpRequest(
            method="GET",
            url="/api/products/999",
            body=b"",
            headers={},
            route_params={"product_id": "999"},
        )
        response = module.get_product(req)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# github_webhook
# ---------------------------------------------------------------------------


class TestGithubWebhook:
    """Smoke tests for examples/github_webhook."""

    def test_module_loads(self) -> None:
        module = _load_example_module("github_webhook")
        assert hasattr(module, "app")

    def test_invalid_signature_rejected(self) -> None:
        module = _load_example_module("github_webhook")
        req = func.HttpRequest(
            method="POST",
            url="/api/github/webhook",
            body=b'{"action": "opened"}',
            headers={
                "X-Hub-Signature-256": "sha256=invalid",
                "X-GitHub-Event": "push",
                "X-GitHub-Delivery": "test-delivery-1",
            },
        )
        response = module.github_webhook(req)
        assert response.status_code == 401

    def test_missing_signature_rejected(self) -> None:
        module = _load_example_module("github_webhook")
        req = func.HttpRequest(
            method="POST",
            url="/api/github/webhook",
            body=b'{"action": "opened"}',
            headers={
                "X-GitHub-Event": "push",
                "X-GitHub-Delivery": "test-delivery-2",
            },
        )
        response = module.github_webhook(req)
        assert response.status_code == 401

    def test_push_event_handler(self) -> None:
        module = _load_example_module("github_webhook")
        body = {"ref": "refs/heads/main", "pusher": {"name": "bot"}, "commits": [{}]}
        result = module._handle_push(body)
        assert "main" in result
        assert "bot" in result

    def test_pull_request_event_handler(self) -> None:
        module = _load_example_module("github_webhook")
        body = {"action": "opened", "pull_request": {"title": "Fix bug", "number": 42}}
        result = module._handle_pull_request(body)
        assert "#42" in result
        assert "Fix bug" in result

    def test_issues_event_handler(self) -> None:
        module = _load_example_module("github_webhook")
        body = {"action": "closed", "issue": {"title": "Track issue", "number": 7}}
        result = module._handle_issues(body)
        assert "#7" in result
        assert "closed" in result


# ---------------------------------------------------------------------------
# queue_worker
# ---------------------------------------------------------------------------


class TestQueueWorker:
    """Smoke tests for examples/queue_worker."""

    def test_module_loads(self) -> None:
        module = _load_example_module("queue_worker")
        assert hasattr(module, "app")

    def test_process_task_helper(self) -> None:
        module = _load_example_module("queue_worker")
        result = module._process_task({"id": "t-1", "action": "send_email"})
        assert "t-1" in result

    def test_process_queue_message_valid_json(self) -> None:
        module = _load_example_module("queue_worker")
        msg = MagicMock(spec=func.QueueMessage)
        msg.id = "msg-001"
        msg.get_body.return_value = json.dumps({"id": "t-1", "action": "test"}).encode()
        msg.dequeue_count = 1
        # Should not raise
        module.process_queue_message(msg)

    def test_process_queue_message_invalid_json(self) -> None:
        module = _load_example_module("queue_worker")
        msg = MagicMock(spec=func.QueueMessage)
        msg.id = "msg-002"
        msg.get_body.return_value = b"not json"
        msg.dequeue_count = 1
        # Should not raise — logs error and returns
        module.process_queue_message(msg)


# ---------------------------------------------------------------------------
# timer_job
# ---------------------------------------------------------------------------


class TestTimerJob:
    """Smoke tests for examples/timer_job."""

    def test_module_loads(self) -> None:
        module = _load_example_module("timer_job")
        assert hasattr(module, "app")

    def test_perform_maintenance_helper(self) -> None:
        module = _load_example_module("timer_job")
        result = module._perform_maintenance()
        assert "complete" in result

    def test_scheduled_job_normal(self) -> None:
        module = _load_example_module("timer_job")
        timer = MagicMock(spec=func.TimerRequest)
        timer.past_due = False
        # Should not raise
        module.scheduled_job(timer)

    def test_scheduled_job_past_due(self) -> None:
        module = _load_example_module("timer_job")
        timer = MagicMock(spec=func.TimerRequest)
        timer.past_due = True
        # Should not raise — logs warning about past due
        module.scheduled_job(timer)
