# HTTP API Basic Example

Minimal REST API built with the Azure Functions Python v2 programming model.

This example demonstrates:
- GET all items with optional category filter
- GET single item by ID
- POST to create a new item
- DELETE an item by ID

All data is stored in an in-memory dictionary. This project corresponds
to the `recipes/http-api-basic.md` recipe.

## Run Locally

```bash
pip install -r requirements.txt
func start
```
