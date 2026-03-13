# pyright: reportMissingImports=false
"""HTTP API with OpenAPI documentation using azure-functions-openapi."""

from __future__ import annotations

import json

import azure.functions as func
from azure_functions_openapi.decorator import openapi
from azure_functions_openapi.openapi import get_openapi_json
from azure_functions_openapi.swagger_ui import render_swagger_ui

app = func.FunctionApp()

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


@app.route(
    route="products",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
@openapi(
    route="/api/products",
    summary="List all products",
    description="Returns every product in the catalogue.",
    tags=["Products"],
    response={200: {"description": "Array of product objects"}},
)
def list_products(req: func.HttpRequest) -> func.HttpResponse:
    """Return all products."""
    return _json_response(list(_PRODUCTS.values()))


@app.route(
    route="products/{product_id}",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
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
    """Return a single product."""
    raw_id = req.route_params.get("product_id", "")
    try:
        product_id = int(raw_id)
    except ValueError:
        return _json_response({"error": "Invalid product_id"}, 400)

    product = _PRODUCTS.get(product_id)
    if product is None:
        return _json_response({"error": "Not found"}, 404)
    return _json_response(product)


@app.route(route="openapi.json", auth_level=func.AuthLevel.ANONYMOUS)
def openapi_spec(req: func.HttpRequest) -> func.HttpResponse:
    """Serve the generated OpenAPI JSON specification."""
    return func.HttpResponse(get_openapi_json(), mimetype="application/json")


@app.route(route="docs", auth_level=func.AuthLevel.ANONYMOUS)
@app.function_name(name="swagger_ui")
def docs_ui(req: func.HttpRequest) -> func.HttpResponse:
    """Serve the Swagger UI."""
    return render_swagger_ui()
