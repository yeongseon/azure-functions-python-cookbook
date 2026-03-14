# HTTP API Basic

## Overview

This recipe demonstrates a minimal REST-style API using Azure Functions Python
v2 decorators and an in-memory store. It is the most direct path to understand
HTTP-triggered functions, route parameters, query parameters, JSON payloads,
and status-code handling.

The paired runnable project is `examples/http_api_basic`.

## Primary use case

Use this pattern when you need:

- small internal APIs
- quick CRUD prototypes
- straightforward request/response semantics
- a baseline before adding OpenAPI, queues, or durable workflows

## Architecture diagram (text)

```text
Client
  |
  | HTTP request (GET/POST/DELETE)
  v
Azure Functions Host
  |
  | route match: /api/items or /api/items/{item_id}
  v
function_app.py
  |- list_items(req)
  |- get_item(req)
  |- create_item(req)
  '- delete_item(req)
  |
  | JSON response + HTTP status
  v
Client
```

## Prerequisites

- Python 3.10+
- Azure Functions Core Tools v4
- Dependencies from `examples/http_api_basic/requirements.txt`

Install and run:

```bash
cd examples/http_api_basic
pip install -r requirements.txt
func start
```

## Step-by-step implementation guide

The implementation follows this flow:

1. Create `app = func.FunctionApp()`.
2. Define shared in-memory state (`_ITEMS`, `_NEXT_ID`).
3. Add helper `_json_response` for consistent JSON output.
4. Register `GET /api/items` with optional category filtering.
5. Register `GET /api/items/{item_id}` with path parsing and 404 behavior.
6. Register `POST /api/items` with JSON parsing and validation.
7. Register `DELETE /api/items/{item_id}` with id parsing and 204 response.

These steps directly match `examples/http_api_basic/function_app.py`.

## Complete code walkthrough

### App and in-memory store

```python
import azure.functions as func

app = func.FunctionApp()

_ITEMS: dict[int, dict[str, str | int]] = {
    1: {"id": 1, "name": "Laptop", "category": "electronics"},
    2: {"id": 2, "name": "Coffee Mug", "category": "kitchen"},
}
_NEXT_ID: int = 3
```

This gives a deterministic local dataset for testing request behavior.

### JSON response helper

```python
def _json_response(body: object, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body, ensure_ascii=False),
        mimetype="application/json",
        status_code=status_code,
    )
```

All handlers use one response utility for consistent content type.

### List endpoint (`GET /api/items`)

```python
@app.route(route="items", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def list_items(req: func.HttpRequest) -> func.HttpResponse:
    category = req.params.get("category")
    items = list(_ITEMS.values())
    if category:
        items = [item for item in items if item.get("category") == category]
    return _json_response(items)
```

This endpoint shows query-string filtering with a simple list comprehension.

### Detail endpoint (`GET /api/items/{item_id}`)

```python
@app.route(route="items/{item_id}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_item(req: func.HttpRequest) -> func.HttpResponse:
    raw_id = req.route_params.get("item_id", "")
    try:
        item_id = int(raw_id)
    except ValueError:
        return _json_response({"error": "Invalid item_id"}, 400)

    item = _ITEMS.get(item_id)
    if item is None:
        return _json_response({"error": "Not found"}, 404)
    return _json_response(item)
```

Path conversion failures return `400`; missing records return `404`.

### Create endpoint (`POST /api/items`)

```python
@app.route(route="items", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def create_item(req: func.HttpRequest) -> func.HttpResponse:
    global _NEXT_ID
    try:
        body = req.get_json()
    except ValueError:
        return _json_response({"error": "Invalid JSON"}, 400)

    name = body.get("name")
    if not name:
        return _json_response({"error": "name is required"}, 400)

    item = {"id": _NEXT_ID, "name": name, "category": body.get("category", "")}
    _ITEMS[_NEXT_ID] = item
    _NEXT_ID += 1
    return _json_response(item, 201)
```

The endpoint creates records in memory and returns `201` on success.

### Delete endpoint (`DELETE /api/items/{item_id}`)

```python
@app.route(route="items/{item_id}", methods=["DELETE"], auth_level=func.AuthLevel.ANONYMOUS)
def delete_item(req: func.HttpRequest) -> func.HttpResponse:
    raw_id = req.route_params.get("item_id", "")
    try:
        item_id = int(raw_id)
    except ValueError:
        return _json_response({"error": "Invalid item_id"}, 400)

    _ITEMS.pop(item_id, None)
    return func.HttpResponse(status_code=204)
```

Delete returns `204` regardless of prior existence, which keeps semantics simple.

## Run locally

```bash
cd examples/http_api_basic
pip install -r requirements.txt
func start
```

### cURL checks

```bash
curl http://localhost:7071/api/items
curl "http://localhost:7071/api/items?category=electronics"
curl http://localhost:7071/api/items/1
curl -X POST http://localhost:7071/api/items -H "Content-Type: application/json" -d '{"name":"Notebook","category":"office"}'
curl -X DELETE http://localhost:7071/api/items/1
```

## Expected output

Representative responses:

```json
[{"id":1,"name":"Laptop","category":"electronics"},{"id":2,"name":"Coffee Mug","category":"kitchen"}]
```

```json
{"id":3,"name":"Notebook","category":"office"}
```

Error examples:

```json
{"error":"Invalid JSON"}
```

```json
{"error":"Not found"}
```

## Production considerations

- Replace in-memory state with durable storage.
- Add request/response schema validation (for example Pydantic models).
- Add authentication/authorization for non-public APIs.
- Keep error responses deterministic and non-sensitive.
- Add structured logging and correlation IDs.
- Add rate limiting in front with API Management where needed.
- Consider cold start impact for latency-sensitive endpoints.

!!! warning
    In-memory state is process-local and resets on restart. It is for learning,
    not persistence.

## Related recipes

- If you need API docs and contracts, continue to [HTTP API with OpenAPI](http-api-openapi.md).
- If API calls should enqueue heavy background work, continue to [Queue Worker](queue-worker.md).

## Ecosystem links

- `azure-functions-validation` for validation helpers
- `azure-functions-openapi` for API contracts
- `azure-functions-logging` for operational visibility
- `azure-functions-scaffold` for starter generation
