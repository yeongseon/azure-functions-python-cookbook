# Getting Started

This guide shows the fastest path from clone to running recipe-aligned
Azure Functions examples locally.

!!! info "What you are using"
    This repository is a cookbook. You consume it by reading recipes in
    `recipes/` and running matching sample apps in `examples/`.

## 1) Clone and set up the environment

```bash
git clone https://github.com/yeongseon/azure-functions-python-cookbook.git
cd azure-functions-python-cookbook
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
make install
```

Alternative:

```bash
pip install -e ".[dev,docs]"
```

## 2) Pick a recipe based on your use case

Use this quick map:

| Need | Recipe | Example |
| --- | --- | --- |
| Basic HTTP endpoint | `recipes/hello-http-minimal.md` | `examples/http/hello_http_minimal` |
| Full CRUD with routing | `recipes/http-routing-query-body.md` | `examples/http/http_routing_query_body` |
| GitHub event ingestion | `recipes/webhook-github.md` | `examples/http/webhook_github` |
| Async queue processing | `recipes/queue-consumer.md` | `examples/queue/queue_consumer` |
| Scheduled jobs | `recipes/timer-cron-job.md` | `examples/timer/timer_cron_job` |

## 3) Read the recipe first

Each recipe describes:

- Why the pattern exists
- Trigger flow and architecture
- Project structure and local run steps
- Production concerns (security, scaling, retries, observability)

!!! tip
    Read the recipe before editing the example code. It gives important
    context for design decisions and operational behavior.

## 4) Run the matching example

### Hello HTTP Minimal

```bash
cd examples/http/hello_http_minimal
pip install -e .
func start
```

Test endpoints:

```bash
curl http://localhost:7071/api/hello
curl "http://localhost:7071/api/hello?name=Azure"
```

### GitHub Webhook Receiver

```bash
cd examples/http/webhook_github
pip install -e .
func start
```

Set `GITHUB_WEBHOOK_SECRET` before receiving signed webhook traffic.

### Queue Consumer

```bash
cd examples/queue/queue_consumer
pip install -e .
func start
```

For local queue emulation:

```bash
azurite --queuePort 10001
```

Set local storage connection to `UseDevelopmentStorage=true`.

### Timer Cron Job

```bash
cd examples/timer/timer_cron_job
pip install -e .
func start
```

Manual trigger for quick testing:

```bash
curl -X POST http://localhost:7071/admin/functions/scheduled_job -H "Content-Type: application/json" -d '{"input":"test"}'
```

## 5) Adapt a recipe to your needs

After you confirm an example runs:

1. Replace in-memory or placeholder logic with your domain logic.
2. Move secrets to environment variables / Key Vault.
3. Add structured logging and request correlation IDs.
4. Add tests for happy-path and failure-path behavior.
5. Validate production concerns listed in the recipe page.

## 6) Validate changes

```bash
make check-all
make docs
```

This verifies linting, typing, tests, security scan, and docs build.

## Common first-week workflow

```text
Choose recipe -> Run sample -> Confirm endpoint/trigger behavior ->
Customize code -> Add tests -> Re-run checks -> Document changes
```

## Where to go next

- Pattern orientation: [Recipes Overview](recipes/index.md)
- Contributor workflow: [Development](development.md)
- Test strategy: [Testing](testing.md)
- Frequent issues: [Troubleshooting](troubleshooting.md)
- Project direction: [Roadmap](roadmap.md)
