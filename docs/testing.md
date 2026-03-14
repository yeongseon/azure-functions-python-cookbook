# Testing

Testing in this cookbook has two goals:

1. Validate repository quality checks.
2. Validate that each runnable example behaves as documented.

## Repository-level checks

Run the full quality suite:

```bash
make check-all
```

This includes:

- Linting and type checks
- Unit tests
- Security scan

For docs integrity:

```bash
make docs
```

## Individual commands

| Command | What it validates |
| --- | --- |
| `make format` | Formatting conventions |
| `make lint` | Ruff + mypy correctness |
| `make test` | Automated tests |
| `make cov` | Coverage report generation |
| `make security` | Bandit static security checks |
| `make docs` | MkDocs build and link rendering |

## Testing recipe examples locally

### HTTP API Basic

```bash
cd examples/http_api_basic
pip install -r requirements.txt
func start
```

Smoke checks:

```bash
curl http://localhost:7071/api/items
curl http://localhost:7071/api/items/1
curl -X POST http://localhost:7071/api/items -H "Content-Type: application/json" -d '{"name":"Paper","category":"office"}'
curl -X DELETE http://localhost:7071/api/items/1
```

### HTTP API with OpenAPI

```bash
cd examples/http_api_openapi
pip install -r requirements.txt
func start
```

Smoke checks:

```bash
curl http://localhost:7071/api/products
curl http://localhost:7071/api/openapi.json
```

Manual UI check: `http://localhost:7071/api/docs`.

### GitHub Webhook

```bash
cd examples/github_webhook
pip install -r requirements.txt
func start
```

Set `GITHUB_WEBHOOK_SECRET`, then send signed and unsigned test payloads.
Expected behavior: unsigned or invalid signatures return `401`.

### Queue Worker

```bash
cd examples/queue_worker
pip install -r requirements.txt
func start
```

Run Azurite and enqueue JSON messages into `work-items`.
Verify logs show dequeue count, JSON parsing, and task completion.

### Timer Job

```bash
cd examples/timer_job
pip install -r requirements.txt
func start
```

Verify scheduled runs in logs, then manually trigger with:

```bash
curl -X POST http://localhost:7071/admin/functions/scheduled_job -H "Content-Type: application/json" -d '{"input":"test"}'
```

## What to test when editing docs

When documentation changes include command examples or paths:

- Confirm every path exists
- Confirm commands are still valid for current repo layout
- Confirm route names match real handlers in `examples/*/function_app.py`
- Confirm recipe page cross-links resolve

## CI alignment

Local validation should mirror CI as closely as possible.
Before PR submission, run at minimum:

```bash
make check-all
make docs
```

If your change touches trigger behavior, also run the relevant example app and
manually verify expected responses or logs.

See also: [Development](development.md), [Troubleshooting](troubleshooting.md)
