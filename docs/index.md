# Azure Functions Python Cookbook

Practical, production-oriented recipes for building Azure Functions with the
Python v2 programming model.

!!! info "What this project is"
    This repository is a cookbook and pattern catalog.
    It is not a runtime library you install as application dependency.

## Why this cookbook exists

Azure Functions documentation is broad, but many teams still need concrete,
copy-adapt-run patterns for common workloads. This cookbook focuses on that
gap by pairing clear recipe narratives with runnable examples.

## What you get

- Trigger-focused recipes for real workloads (HTTP, webhook, queue, timer)
- Runnable sample apps under `examples/`
- Production considerations in every recipe
- Consistent structure for learning, implementation, and contribution

## Recipe cards

### HTTP API Basic

- Trigger: HTTP
- Best for: minimal CRUD APIs and route handling
- Learn more: [HTTP API Basic](recipes/http-api-basic.md)

### HTTP API with OpenAPI

- Trigger: HTTP
- Best for: contract-first docs and Swagger UI
- Learn more: [HTTP API with OpenAPI](recipes/http-api-openapi.md)

### GitHub Webhook

- Trigger: HTTP
- Best for: secure signed event ingestion from GitHub
- Learn more: [GitHub Webhook](recipes/github-webhook.md)

### Queue Worker

- Trigger: Queue
- Best for: asynchronous background processing
- Learn more: [Queue Worker](recipes/queue-worker.md)

### Timer Job

- Trigger: Timer
- Best for: scheduled maintenance and periodic automation
- Learn more: [Timer Job](recipes/timer-job.md)

## Quick start

```bash
git clone https://github.com/yeongseon/azure-functions-python-cookbook.git
cd azure-functions-python-cookbook
python -m venv .venv
source .venv/bin/activate
```

Run one example:

```bash
cd examples/http_api_basic
pip install -r requirements.txt
func start
```

Then test:

```bash
curl http://localhost:7071/api/items
```

## Recommended learning path

1. [Installation](installation.md)
2. [Getting Started](getting-started.md)
3. [Recipes Overview](recipes/index.md)
4. Pick one deep-dive recipe page
5. Run the matching `examples/<name>` project
6. Validate with [Testing](testing.md)

## Repository map

```text
docs/       Documentation site pages and recipe deep-dives
recipes/    Source recipe narratives and template contract
examples/   Runnable Azure Functions app implementations
```

## Ecosystem projects

These companion projects integrate well with cookbook patterns:

- `azure-functions-scaffold` -> project bootstrap from known templates
- `azure-functions-validation` -> request/response validation helpers
- `azure-functions-openapi` -> generated API contracts and Swagger UI
- `azure-functions-logging` -> structured telemetry and diagnostics
- `azure-functions-doctor` -> local environment diagnosis

## Contributing and quality

If you want to improve recipes or examples:

- Use [Development](development.md) for workflow
- Use [Testing](testing.md) before submitting changes
- Follow [Contributing Guidelines](contributing.md)

## Additional references

- Pattern model and boundaries: [Architecture](architecture.md)
- Planned expansion: [Roadmap](roadmap.md)
- Common failures and fixes: [Troubleshooting](troubleshooting.md)
- Frequently asked questions: [FAQ](faq.md)

!!! tip
    The fastest path to value is: pick one recipe, run its example, then adapt
    for your production constraints.
