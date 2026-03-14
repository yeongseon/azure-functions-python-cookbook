"""Smoke tests for examples that cannot be fully E2E tested locally.

These tests verify that each example's ``function_app.py`` module can be
imported without errors, confirming that the Blueprint structure is valid
and all dependencies are resolvable.

Non-emulatable triggers include:
- Service Bus (no Azurite support)
- Event Hub (no Azurite support)
- Cosmos DB change feed (no Azurite support)
- Timer/cron (no HTTP endpoint)
- Managed Identity examples (require real Azure credentials)
- MCP Server (requires FUNCTION-level auth key)
- host.json / concurrency tuning (timer + queue only)
- Retry and idempotency (timer + queue only)
"""

from __future__ import annotations

import importlib
import sys
from types import ModuleType

import pytest

from tests.e2e.conftest import EXAMPLES_ROOT

pytestmark = pytest.mark.smoke


def _import_function_app(example_path: str) -> ModuleType:
    """Import a function_app.py module from an example directory.

    Uses importlib to load the module by file path, avoiding sys.path
    pollution and module name collisions between examples.
    """
    example_dir = EXAMPLES_ROOT / example_path
    function_app_file = example_dir / "function_app.py"

    if not function_app_file.exists():
        pytest.fail(f"function_app.py not found: {function_app_file}")

    # Add example dir to sys.path temporarily so relative imports work
    example_dir_str = str(example_dir)
    original_path = sys.path.copy()
    original_modules = set(sys.modules.keys())

    try:
        sys.path.insert(0, example_dir_str)

        # Clear any cached 'app' module to avoid cross-example conflicts
        modules_to_remove = [k for k in sys.modules if k == "app" or k.startswith("app.")]
        for mod_key in modules_to_remove:
            del sys.modules[mod_key]

        spec = importlib.util.spec_from_file_location(
            f"function_app_{example_path.replace('/', '_')}",
            function_app_file,
        )
        if spec is None or spec.loader is None:
            pytest.fail(f"Could not create import spec for {function_app_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path = original_path
        # Clean up loaded app.* modules to prevent leakage
        new_modules = set(sys.modules.keys()) - original_modules
        for mod_key in new_modules:
            if mod_key == "app" or mod_key.startswith("app."):
                del sys.modules[mod_key]


# ---------------------------------------------------------------------------
# Service Bus
# ---------------------------------------------------------------------------


class TestServiceBusWorkerSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("servicebus/servicebus_worker")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# Event Hub
# ---------------------------------------------------------------------------


class TestEventHubConsumerSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("eventhub/eventhub_consumer")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# Cosmos DB
# ---------------------------------------------------------------------------


class TestChangeFeedProcessorSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("cosmosdb/change_feed_processor")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# Timer
# ---------------------------------------------------------------------------


class TestTimerCronJobSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("timer/timer_cron_job")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# Managed Identity
# ---------------------------------------------------------------------------


class TestManagedIdentityStorageSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("recipes/managed_identity_storage")
        assert hasattr(module, "app")


class TestManagedIdentityServiceBusSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("recipes/managed_identity_servicebus")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# host.json / Concurrency tuning
# ---------------------------------------------------------------------------


class TestHostJsonTuningSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("recipes/host_json_tuning")
        assert hasattr(module, "app")


class TestConcurrencyTuningSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("recipes/concurrency_tuning")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# Retry and Idempotency
# ---------------------------------------------------------------------------


class TestRetryAndIdempotencySmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("recipes/retry_and_idempotency")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# AI / MCP Server
# ---------------------------------------------------------------------------


class TestMcpServerSmoke:
    def test_module_imports(self) -> None:
        module = _import_function_app("ai/mcp_server_example")
        assert hasattr(module, "app")
