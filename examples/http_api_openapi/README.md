# HTTP API with OpenAPI Example

REST API with auto-generated Swagger / OpenAPI documentation.

This example demonstrates:
- `@openapi` decorator for endpoint metadata
- Auto-generated `/api/openapi.json` spec endpoint
- Swagger UI at `/api/docs`
- Product catalogue with list and detail endpoints

This project corresponds to the `recipes/http-api-openapi.md` recipe.

## Run Locally

```bash
pip install -r requirements.txt
func start
# Open http://localhost:7071/api/docs for Swagger UI
```
