# HTTP API with OpenAPI

## Overview

This recipe builds on basic HTTP routes and adds generated OpenAPI metadata
plus Swagger UI. It is ideal when consumers need discoverable contracts,
parameter descriptions, and explicit response documentation.

The paired runnable project is `examples/http_api_openapi`.

## Primary use case

Use this pattern when you need:

- browsable API docs for integrators
- machine-readable API contract output
- stronger alignment between endpoint behavior and docs
- easier cross-team API communication

## Architecture diagram (text)

```text
Client
  |
  | GET /api/products or /api/products/{product_id}
  v
Azure Functions Host
  |
  v
function_app.py
  |- list_products + @openapi metadata
  |- get_product + path parameter schema
  |- openapi_spec (serves /api/openapi.json)
  '- docs_ui (serves /api/docs)
  |
  +--> OpenAPI JSON for tooling
  +--> Swagger UI for interactive exploration
```

## Prerequisites

- Python 3.10+
- Azure Functions Core Tools v4
- `azure-functions`
- `azure-functions-openapi`

Install and run:

```bash
cd examples/http_api_openapi
pip install -r requirements.txt
func start
```

## Step-by-step implementation guide

The example implementation follows this sequence:

1. Import OpenAPI decorators and rendering helpers.
2. Define `app = func.FunctionApp()`.
3. Add product data source (in-memory for demonstration).
4. Implement JSON response utility.
5. Add list and detail routes with `@openapi` metadata.
6. Add `/api/openapi.json` endpoint via `get_openapi_json()`.
7. Add `/api/docs` endpoint via `render_swagger_ui()`.

These steps are implemented in `examples/http_api_openapi/function_app.py`.

## Complete code walkthrough

### Imports and app setup

```python
import azure.functions as func
from azure_functions_openapi.decorator import openapi
from azure_functions_openapi.openapi import get_openapi_json
from azure_functions_openapi.swagger_ui import render_swagger_ui

app = func.FunctionApp()
```

The OpenAPI package augments route handlers with metadata that can be rendered
as JSON and visualized in Swagger UI.

### Product dataset and response helper

```python
_PRODUCTS: dict[int, dict[str, str | int]] = {
    1: {"id": 1, "name": "Widget", "price": 9_99},
    2: {"id": 2, "name": "Gadget", "price": 19_99},
}

def _json_response(body: object, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body, ensure_ascii=False),
        mimetype="application/json",
        status_code=status_code,
    )
```

The dataset is intentionally small and local to keep API-contract behavior easy
to test.

### List route with OpenAPI metadata

```python
@app.route(route="products", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
@openapi(
    route="/api/products",
    summary="List all products",
    description="Returns every product in the catalogue.",
    tags=["Products"],
    response={200: {"description": "Array of product objects"}},
)
def list_products(req: func.HttpRequest) -> func.HttpResponse:
    return _json_response(list(_PRODUCTS.values()))
```

This is the baseline list endpoint plus OpenAPI annotations.

### Detail route with typed path parameter metadata

```python
@app.route(route="products/{product_id}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
@openapi(
    route="/api/products/{product_id}",
    summary="Get a product by ID",
    description="Returns a single product identified by *product_id*.",
    tags=["Products"],
    parameters=[
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "Unique product identifier",
        }
    ],
    response={
        200: {"description": "Product found"},
        404: {"description": "Product not found"},
    },
)
def get_product(req: func.HttpRequest) -> func.HttpResponse:
    raw_id = req.route_params.get("product_id", "")
    try:
        product_id = int(raw_id)
    except ValueError:
        return _json_response({"error": "Invalid product_id"}, 400)

    product = _PRODUCTS.get(product_id)
    if product is None:
        return _json_response({"error": "Not found"}, 404)
    return _json_response(product)
```

This route documents path parameter type and success/failure responses.

### OpenAPI JSON endpoint

```python
@app.route(route="openapi.json", auth_level=func.AuthLevel.ANONYMOUS)
def openapi_spec(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(get_openapi_json(), mimetype="application/json")
```

Tooling (SDK generators, API clients, CI validation) can consume this output.

### Swagger UI endpoint

```python
@app.route(route="docs", auth_level=func.AuthLevel.ANONYMOUS)
@app.function_name(name="swagger_ui")
def docs_ui(req: func.HttpRequest) -> func.HttpResponse:
    return render_swagger_ui()
```

This gives interactive API docs at a stable local URL.

## Run locally

```bash
cd examples/http_api_openapi
pip install -r requirements.txt
func start
```

### Verify endpoints

```bash
curl http://localhost:7071/api/products
curl http://localhost:7071/api/products/1
curl http://localhost:7071/api/openapi.json
```

Open in browser:

```text
http://localhost:7071/api/docs
```

## Expected output

List endpoint:

```json
[{"id":1,"name":"Widget","price":999},{"id":2,"name":"Gadget","price":1999}]
```

Detail endpoint:

```json
{"id":1,"name":"Widget","price":999}
```

Invalid path parameter:

```json
{"error":"Invalid product_id"}
```

## Production considerations

- Keep OpenAPI annotations updated with behavior changes.
- Include error response schemas (`400`, `401`, `403`, `404`, `500`).
- Protect docs/spec endpoints when exposing internal APIs.
- Add versioning strategy to routes or spec metadata.
- Validate generated spec in CI to catch accidental contract drift.
- Avoid ambiguous parameter definitions; keep names stable.
- Add authentication scheme documentation in OpenAPI metadata.

!!! warning
    Swagger UI convenience can expose internal API shape. Restrict access for
    non-public APIs.

## Related recipes

- For a simpler baseline without contract metadata, see [HTTP API Basic](http-api-basic.md).
- For signed inbound events, see [GitHub Webhook](github-webhook.md).

## Ecosystem links

- `azure-functions-openapi` for decorator-based contract generation
- `azure-functions-validation` for payload schema validation
- `azure-functions-logging` for structured diagnostics
- `azure-functions-scaffold` for template bootstrapping
