# HTTP API with OpenAPI

## Overview
An HTTP API with auto-generated OpenAPI (Swagger) documentation. This recipe extends the basic HTTP API pattern by integrating the azure-functions-openapi package to produce a browsable API specification. Clients can discover endpoints, parameter schemas, and response formats through the generated OpenAPI UI. By decorating your Python functions with metadata, you create a self-documenting service that reduces the friction between backend developers and API consumers. This approach ensures that your documentation remains in sync with your code, as both are maintained in the same source files.

## When to Use
- Building public-facing APIs that require high-quality documentation for external developers.
- Teams that rely on Swagger UI for API exploration, testing, and manual verification of changes.
- Projects where API contracts must be shared across frontend and backend teams to avoid integration errors.
- APIs that need client SDK generation from standard OpenAPI specifications to support multiple platforms.
- Internal microservices that need clear definitions for service-to-service communication in a distributed system.
- Projects where maintaining a separate documentation site is too time-consuming or error-prone.

## Architecture
The request flow remains similar to a standard HTTP API but adds an OpenAPI middleware layer. The azure-functions-openapi decorators annotate your functions with schema metadata, which the library then aggregates into a single specification file.

```text
                                    +-----------------------+
                                    | /api/openapi/ui       |
                                    | (Swagger UI)          |
                                    +-----------------------+
                                               ^
                                               |
+----------+       +-----------------------+   |   +-----------------------+
|  Client  | ----> | Azure Functions Host  | --+-> | function_app.py       |
+----------+       +-----------------------+       | (OpenAPI Decorators)  |
                                                   +-----------------------+
                                                              |
                                                              v
                                                   +-----------------------+
                                                   | /api/openapi/spec     |
                                                   | (JSON/YAML)           |
                                                   +-----------------------+
```

1. The client sends a request to a standard API endpoint.
2. The Azure Functions host routes the request to the corresponding Python function.
3. The function_app.py file contains decorators that define the expected inputs and outputs.
4. A dedicated endpoint (typically /api/openapi/spec) serves the generated JSON or YAML.
5. A Swagger UI endpoint provides the interactive documentation interface for developers.

## Project Structure
```text
http-api-openapi/
  function_app.py       # Main application with OpenAPI decorators
  host.json             # Function host configuration
  local.settings.json   # Local development settings (CORS, keys)
  requirements.txt      # Dependencies including azure-functions-openapi
  tests/                # Unit and integration tests
    test_functions.py   # Tests for API logic and schema compliance
```

## Implementation Detail

The integration requires the `azure-functions-openapi` package. Below is an example of how to structure your `function_app.py` to support OpenAPI generation. The decorators allow you to specify types, descriptions, and even example values for your parameters and responses.

```python
import azure.functions as func
from azure_functions_openapi import Blueprint, OpenAPI

app = Blueprint()
openapi = OpenAPI(app)

@app.route(route="products/{id}", methods=["GET"])
@openapi.doc(
    summary="Get product details",
    description="Returns product information for a given ID from the database",
    params={"id": "The unique product identifier (UUID)"},
    responses={
        200: {"description": "Product found", "content": {"application/json": {}}},
        404: {"description": "Product not found if the ID does not exist"}
    }
)
def get_product(req: func.HttpRequest) -> func.HttpResponse:
    product_id = req.route_params.get('id')
    # Business logic to fetch product from your database or service
    # return func.HttpResponse(f"Product {product_id}", status_code=200)
    return func.HttpResponse(
        "{\"id\": \"" + product_id + "\", \"name\": \"Sample Product\"}",
        mimetype="application/json",
        status_code=200
    )
```

## Run Locally
To run this project locally, ensure you have the Azure Functions Core Tools installed.

1. Install the necessary dependencies from the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the function host:
   ```bash
   func start
   ```

3. Access the OpenAPI UI:
   Navigate to `http://localhost:7071/api/openapi/ui` in your browser to view the interactive documentation. You can test your endpoints directly from this interface.

## Production Considerations
- OpenAPI spec versioning: Ensure that your API version in the OpenAPI metadata matches your deployment cycle and semantic versioning.
- Spec validation: Use automated tests to verify that the generated JSON matches your expected schema before every deployment.
- Security: Consider disabling the Swagger UI endpoint in production environments or protecting it behind an authentication layer like Azure AD to prevent leaking internal API structures.
- Schema validation: The library can enforce request/response contracts, ensuring that incoming data adheres strictly to your defined models.
- CORS: Configure Cross-Origin Resource Sharing settings in the Azure portal to allow frontend applications or external developers to consume the API.
- Performance: Generating large OpenAPI specs on the fly can add minor overhead. Consider caching the generated spec if your API surface area is extremely large.

## Scaffold Starter
You can quickly generate a project with OpenAPI support using the following command from the CLI:

```bash
azure-functions-scaffold new my-api --with-openapi
```

## Key Benefits
Using OpenAPI with Azure Functions provides a standardized way to communicate your API's capabilities. It allows for the use of tools like Postman or Insomnia to import the spec directly for automated testing. Additionally, it enables automatic generation of client libraries in various languages, significantly speeding up integration for downstream consumers and reducing the burden on your team to provide code samples.

The decorator-based approach ensures that documentation stays close to the code, reducing the likelihood of the documentation becoming stale as the API evolves. Every change to the function signature or return type can be immediately reflected in the metadata, providing a single source of truth for your API contract.

## Best Practices
- Use descriptive summaries and long-form descriptions for every endpoint.
- Define explicit models for request bodies and response types using Pydantic or standard Python classes for better type safety.
- Tag related endpoints to group them logically in the Swagger UI, making it easier for users to navigate your API.
- Always include error response definitions (400, 401, 403, 500) so consumers know how to handle failures gracefully.
- Utilize example values in your schemas to help developers understand the expected data format without reading the entire spec.
- Document any required headers or authentication schemes using the security metadata features of the library.
- Keep the spec updated as you add new features or deprecate old ones.
- Share the OpenAPI spec file (JSON or YAML) with your stakeholders early in the development process for feedback.
