"""GitHub webhook receiver with HMAC-SHA256 signature validation."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
from typing import Callable

import azure.functions as func

app = func.FunctionApp()

logger = logging.getLogger(__name__)


def _validate_signature(payload: bytes, signature: str | None) -> bool:
    """Verify the request was signed by GitHub using the shared secret."""
    if not signature:
        return False
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "").encode()
    expected = "sha256=" + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def _handle_push(body: dict) -> str:
    """Handle a push event."""
    ref = body.get("ref", "unknown")
    pusher = body.get("pusher", {}).get("name", "unknown")
    commits = body.get("commits", [])
    return f"Push to {ref} by {pusher} with {len(commits)} commit(s)"


def _handle_pull_request(body: dict) -> str:
    """Handle a pull_request event."""
    action = body.get("action", "unknown")
    pr = body.get("pull_request", {})
    title = pr.get("title", "untitled")
    number = pr.get("number", 0)
    return f"PR #{number} '{title}' {action}"


def _handle_issues(body: dict) -> str:
    """Handle an issues event."""
    action = body.get("action", "unknown")
    issue = body.get("issue", {})
    title = issue.get("title", "untitled")
    number = issue.get("number", 0)
    return f"Issue #{number} '{title}' {action}"


@app.route(route="github/webhook", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def github_webhook(req: func.HttpRequest) -> func.HttpResponse:
    """Receive and process GitHub webhook events."""
    signature = req.headers.get("X-Hub-Signature-256")
    event_type = req.headers.get("X-GitHub-Event", "ping")
    delivery_id = req.headers.get("X-GitHub-Delivery", "unknown")
    payload = req.get_body()

    if not _validate_signature(payload, signature):
        logger.warning("Invalid signature for delivery %s", delivery_id)
        return func.HttpResponse("Invalid signature", status_code=401)

    try:
        body: dict = json.loads(payload)
    except (ValueError, json.JSONDecodeError):
        return func.HttpResponse("Invalid JSON", status_code=400)

    handlers: dict[str, Callable[[dict], str]] = {
        "push": _handle_push,
        "pull_request": _handle_pull_request,
        "issues": _handle_issues,
    }

    handler = handlers.get(event_type)
    if handler is None:
        message = f"Received {event_type} event (no handler)"
        logger.info(message)
        return func.HttpResponse(json.dumps({"message": message}), mimetype="application/json")

    result = handler(body)
    logger.info("Processed %s: %s (delivery=%s)", event_type, result, delivery_id)
    return func.HttpResponse(
        json.dumps({"event": event_type, "result": result}),
        mimetype="application/json",
    )
