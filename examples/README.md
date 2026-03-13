# Examples

`azure-functions-python-cookbook` includes runnable Azure Functions projects
that match each recipe in `recipes/`. Every project is a self-contained
function app ready for `func start`.

| Role | Path | Description |
| --- | --- | --- |
| Representative | `examples/http_api_basic` | Minimal REST API with GET, POST, and DELETE for an in-memory item store. |
| Complex | `examples/http_api_openapi` | HTTP API with auto-generated OpenAPI spec and Swagger UI. |
| Focused | `examples/github_webhook` | GitHub webhook receiver with HMAC-SHA256 signature validation. |
| Focused | `examples/queue_worker` | Queue-triggered background worker with JSON message parsing. |
| Focused | `examples/timer_job` | Timer-triggered scheduled job with past-due detection. |

Each example corresponds to a recipe under `recipes/`.

## Run Any Example

```bash
cd examples/http_api_basic
pip install -r requirements.txt
func start
```
