# API Reference

`azure-functions-python-cookbook` is a documentation and example project. It does not export a public Python API.

## What this project provides

- **Recipes** — Standalone Azure Functions examples under `docs/recipes/`.
- **Concepts** — In-depth explanations under `docs/concepts/`.
- **Source examples** — Runnable code under `src/azure_functions_python_cookbook/`.

## Using the examples

Each recipe is a self-contained module. Copy the relevant handler into your own Functions app:

```python
# Example: minimal HTTP handler from hello-http-minimal recipe
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="hello")
@app.route(route="hello", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def hello(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello, world!")
```

## Public package symbol

```python
from azure_functions_python_cookbook import __version__
```

`__version__` is the only exported symbol. It follows [Semantic Versioning](https://semver.org/).

## Related Documents

- [Getting Started](getting-started.md)
- [Usage](usage.md)
- [Recipes](recipes/index.md)
- [Architecture](architecture.md)
