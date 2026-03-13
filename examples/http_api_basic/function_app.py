"""Basic HTTP API with in-memory item store."""

from __future__ import annotations

import json

import azure.functions as func

app = func.FunctionApp()

# In-memory store
_ITEMS: dict[int, dict[str, str | int]] = {
    1: {"id": 1, "name": "Laptop", "category": "electronics"},
    2: {"id": 2, "name": "Coffee Mug", "category": "kitchen"},
}
_NEXT_ID: int = 3


def _json_response(body: object, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body, ensure_ascii=False),
        mimetype="application/json",
        status_code=status_code,
    )


@app.route(
    route="items",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def list_items(req: func.HttpRequest) -> func.HttpResponse:
    """Return all items, optionally filtered by category query param."""
    category = req.params.get("category")
    items = list(_ITEMS.values())
    if category:
        items = [item for item in items if item.get("category") == category]
    return _json_response(items)


@app.route(
    route="items/{item_id}",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def get_item(req: func.HttpRequest) -> func.HttpResponse:
    """Return a single item by id."""
    raw_id = req.route_params.get("item_id", "")
    try:
        item_id = int(raw_id)
    except ValueError:
        return _json_response({"error": "Invalid item_id"}, 400)

    item = _ITEMS.get(item_id)
    if item is None:
        return _json_response({"error": "Not found"}, 404)
    return _json_response(item)


@app.route(
    route="items",
    methods=["POST"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def create_item(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new item from JSON body."""
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


@app.route(
    route="items/{item_id}",
    methods=["DELETE"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def delete_item(req: func.HttpRequest) -> func.HttpResponse:
    """Delete an item by id. Returns 204 regardless."""
    raw_id = req.route_params.get("item_id", "")
    try:
        item_id = int(raw_id)
    except ValueError:
        return _json_response({"error": "Invalid item_id"}, 400)

    _ITEMS.pop(item_id, None)
    return func.HttpResponse(status_code=204)
