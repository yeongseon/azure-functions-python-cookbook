# HTTP API Basic

## Overview
The Azure Functions Python v2 programming model uses a decorator-based approach for defining serverless functions. This recipe demonstrates how to build a basic REST API that handles common HTTP operations like GET, POST, PUT, and DELETE. By using the `func.FunctionApp` object, developers can define routes, methods, and request handlers directly in Python code. This simplifies the development process compared to the older v1 model which required separate `function.json` files for every function.

This recipe focuses on the core mechanics of HTTP triggers. It shows how to access request data, handle different HTTP methods, and return structured responses. The goal is to provide a clean, maintainable foundation for serverless web services.

## When to Use
- Building simple REST endpoints without the overhead of full OpenAPI documentation
- Creating internal microservices that communicate over HTTP
- Prototyping serverless applications quickly using familiar Python patterns
- Migrating existing Flask or FastAPI endpoints to a serverless architecture
- Handling webhooks from third-party services like GitHub or Stripe
- Implementing backend logic for single-page applications (SPAs)

## Architecture
The request flow for an HTTP-triggered Azure Function is straightforward. When a client sends a request to the function endpoint, the Azure Functions host receives it and matches it against the defined routes.

1. Client sends an HTTP request to the Azure Functions endpoint.
2. The Azure Functions Host receives the request and determines which function to invoke.
3. The host routes the request to `function_app.py` based on the route and method decorators.
4. The Python function processes the request, performing logic or database operations.
5. The function returns an `func.HttpResponse` object back to the host.
6. The host sends the HTTP response back to the client.

```text
+----------+      +-----------------------+      +-----------------+      +----------+
|  Client  | ---> | Azure Functions Host  | ---> | function_app.py | ---> | Response |
+----------+      +-----------------------+      +-----------------+      +----------+
```

The application is contained within a single `function_app.py` file in its simplest form. The `func.FunctionApp` instance acts as the central registry for all functions. Each function is decorated with `@app.route`, which specifies the URL path and allowed HTTP methods.

## Project Structure
A standard project following the v2 programming model usually contains the following files:

```text
http-api-basic/
  .venv/               # Python virtual environment (local only)
  function_app.py      # Main entry point with function definitions
  host.json            # Global configuration for the function app
  local.settings.json  # Environment variables for local development
  requirements.txt     # List of Python package dependencies
  tests/               # Directory for unit and integration tests
    test_functions.py  # Test cases for the HTTP functions
```

The `function_app.py` file is the heart of the project. Unlike the v1 model, there are no subdirectories for each function. This makes the project structure much flatter and easier to navigate for developers coming from other Python web frameworks.

## Code Example
The following snippet shows how to define a basic GET endpoint using the v2 model.

```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="items", methods=["GET"])
def get_items(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request for items.")
    # In a real app, you would fetch items from a database here
    return func.HttpResponse("[]", mimetype="application/json", status_code=200)

@app.route(route="items/{id}", methods=["GET"])
def get_item_by_id(req: func.HttpRequest) -> func.HttpResponse:
    item_id = req.route_params.get("id")
    return func.HttpResponse(f"Item {item_id}", status_code=200)
```

## Run Locally
To test the API on your machine, follow these steps:

1. Install the Azure Functions Core Tools:
```bash
npm install -g azure-functions-core-tools@4
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Start the function app:
```bash
func start
```

Once the host starts, it will provide local URLs for each of your functions (e.g., `http://localhost:7071/api/items`). You can use tools like cURL or Postman to send requests to these endpoints.

## Production Considerations
- **Scaling**: Azure Functions on the Consumption plan scale automatically. If traffic increases, the platform allocates more instances to handle the load.
- **Authentication**: You can secure endpoints using function keys or app-level keys. These are configured in the Azure portal or via `host.json`. For production APIs, consider using Azure Active Directory (Microsoft Entra ID).
- **CORS**: If your API is accessed from a browser, you must configure Cross-Origin Resource Sharing (CORS). This is managed in the Azure portal or defined in `host.json`.
- **Logging**: Use the standard Python `logging` module. When deployed, these logs are automatically captured by Application Insights, allowing for detailed monitoring and diagnostics.
- **Error Handling**: Always wrap logic in try-except blocks and return appropriate HTTP status codes (400 for bad requests, 404 for missing resources, 500 for internal errors). Do not return stack traces to the client.
- **Cold Start**: Functions on the Consumption plan may experience latency during the first request after being idle. If low latency is critical, consider the Premium plan or Dedicated (App Service) plan.
- **Rate Limiting**: Azure Functions does not have built-in rate limiting at the code level. Use Azure API Management (APIM) in front of your functions to implement throttling and advanced security.
- **Security**: Never hardcode secrets in `function_app.py`. Use environment variables and store sensitive information like connection strings in Azure Key Vault.

## Scaffold Starter
You can quickly generate a new project using the following command:

```bash
azure-functions-scaffold new my-http-api --template http-basic
```

This command creates the directory structure and populates it with a boilerplate `function_app.py` and configuration files, allowing you to start coding your logic immediately.

## Best Practices
Keep your functions small and focused on a single task. If your `function_app.py` grows too large, you can split it into multiple files using the `Blueprint` feature in the v2 model. Blueprints allow you to define functions in separate modules and then register them with the main app object.

Always validate the request body and parameters. For POST and PUT requests, ensure the content type is correct and the JSON payload matches your expected schema. Using libraries like Pydantic can help with data validation and serialization.

Ensure your `requirements.txt` file is kept up to date. Avoid using broad version ranges for dependencies to prevent unexpected breaking changes during deployment. Regularly audit your dependencies for security vulnerabilities.
