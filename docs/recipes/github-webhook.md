# GitHub Webhook

## Overview

This recipe implements a secure inbound webhook endpoint for GitHub events.
It validates the HMAC-SHA256 signature, routes by event type, and returns
clear HTTP responses for handled and unhandled events.

The paired runnable project is `examples/github_webhook`.

## Primary use case

Use this pattern when you need:

- automated actions on repository events
- secure ingestion of externally-originated HTTP payloads
- event-type routing with lightweight handler functions
- delivery tracking and operational logging

## Architecture diagram (text)

```text
GitHub Event
  |
  | POST /api/github/webhook
  | headers: X-Hub-Signature-256, X-GitHub-Event, X-GitHub-Delivery
  v
Azure Functions Host
  |
  v
github_webhook(req)
  |- validate signature using GITHUB_WEBHOOK_SECRET
  |- parse JSON payload
  |- route to handler map:
  |    push -> _handle_push
  |    pull_request -> _handle_pull_request
  |    issues -> _handle_issues
  '- return JSON response
```

## Prerequisites

- Python 3.10+
- Azure Functions Core Tools v4
- `azure-functions`
- `GITHUB_WEBHOOK_SECRET` configured locally

Run locally:

```bash
cd examples/github_webhook
pip install -r requirements.txt
func start
```

## Step-by-step implementation guide

Implementation flow in `examples/github_webhook/function_app.py`:

1. Define `app = func.FunctionApp()` and logger.
2. Add `_validate_signature(payload, signature)` function.
3. Add event handlers for `push`, `pull_request`, and `issues`.
4. Register route `POST /api/github/webhook`.
5. Read signature/event/delivery headers.
6. Reject invalid signatures (`401`).
7. Parse JSON body; reject malformed payload (`400`).
8. Dispatch to handler map and return JSON result.

## Complete code walkthrough

### Signature validation

```python
def _validate_signature(payload: bytes, signature: str | None) -> bool:
    if not signature:
        return False
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "").encode()
    expected = "sha256=" + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

This function verifies authenticity and integrity of the payload bytes.

### Event handlers

```python
def _handle_push(body: dict) -> str:
    ref = body.get("ref", "unknown")
    pusher = body.get("pusher", {}).get("name", "unknown")
    commits = body.get("commits", [])
    return f"Push to {ref} by {pusher} with {len(commits)} commit(s)"

def _handle_pull_request(body: dict) -> str:
    action = body.get("action", "unknown")
    pr = body.get("pull_request", {})
    title = pr.get("title", "untitled")
    number = pr.get("number", 0)
    return f"PR #{number} '{title}' {action}"

def _handle_issues(body: dict) -> str:
    action = body.get("action", "unknown")
    issue = body.get("issue", {})
    title = issue.get("title", "untitled")
    number = issue.get("number", 0)
    return f"Issue #{number} '{title}' {action}"
```

Handlers are intentionally focused and return concise domain summaries.

### Main webhook route

```python
@app.route(route="github/webhook", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def github_webhook(req: func.HttpRequest) -> func.HttpResponse:
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
    return func.HttpResponse(json.dumps({"event": event_type, "result": result}), mimetype="application/json")
```

This route defines the trust boundary and event dispatch behavior.

## Run locally

```bash
cd examples/github_webhook
pip install -r requirements.txt
func start
```

Set secret in environment before testing signed requests.

### Manual payload testing

For quick unsigned behavior checks (expected `401`):

```bash
curl -X POST http://localhost:7071/api/github/webhook -H "Content-Type: application/json" -H "X-GitHub-Event: push" -d '{"ref":"refs/heads/main"}'
```

For real end-to-end GitHub tests, expose local host with a tunnel and set the
same secret in GitHub webhook settings and local environment.

## Expected output

Examples from successful handler responses:

```json
{"event":"push","result":"Push to refs/heads/main by octocat with 1 commit(s)"}
```

```json
{"event":"pull_request","result":"PR #42 'Improve docs' opened"}
```

Unregistered event response example:

```json
{"message":"Received release event (no handler)"}
```

## Production considerations

- Always verify signatures before parsing payload content.
- Rotate webhook secrets and store in secure app settings.
- Log delivery IDs for replay/duplicate investigation.
- Design handlers to be idempotent (GitHub can retry deliveries).
- Return quickly and offload long work to queue/service bus.
- Consider IP allowlisting and additional WAF rules.
- Avoid leaking internal details in error responses.
- Monitor event volume spikes and latency.

!!! warning
    Signature verification must use raw request bytes. Re-serialization before
    verification can break validation.

## Related recipes

- For normal API endpoints, see [HTTP API Basic](http-api-basic.md).
- For async downstream processing, combine with [Queue Worker](queue-worker.md).

## Ecosystem links

- `azure-functions-logging` for structured request/event logs
- `azure-functions-validation` for payload schema checks
- `azure-functions-scaffold` for starter generation
