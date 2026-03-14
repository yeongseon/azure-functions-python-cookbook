# FAQ

## What is this cookbook?

It is a curated collection of Azure Functions Python v2 recipes and runnable
examples. It focuses on production-oriented patterns, not just minimal demos.

## Is this a Python library I install with pip?

No. This repository is content-first and example-first. You clone it,
read recipes, and run example apps locally.

## Can I use these recipes in production?

Yes, as starting points. You should still do normal production hardening:

- secret management
- identity and access controls
- observability and alerting
- retries and idempotency validation
- cost/performance review

## Do I need an Azure subscription to use this repository?

Not for initial learning and local execution. You can run examples locally
with Azure Functions Core Tools. Queue workflows can be tested with Azurite.

## Which Python versions are supported?

The project targets `>=3.10,<3.15`.

## Which Azure Functions model is used?

All recipes use the Python v2 programming model with decorators and
`func.FunctionApp()`.

## How do I run examples locally?

General flow:

```bash
cd examples/<example_name>
pip install -r requirements.txt
func start
```

Example names:

- `http_api_basic`
- `http_api_openapi`
- `github_webhook`
- `queue_worker`
- `timer_job`

## What is the difference between recipes and examples?

- `recipes/`: narrative pattern docs (why/how/architecture/operations)
- `examples/`: executable function apps that implement those patterns

Use both together. Recipes explain intent; examples prove execution.

## How do I choose the right recipe?

Start from trigger and operational requirement:

- Simple HTTP API -> HTTP API Basic
- HTTP API + contract docs -> HTTP API with OpenAPI
- Signed GitHub events -> GitHub Webhook
- Async background work -> Queue Worker
- Periodic scheduled tasks -> Timer Job

## Where is the recipe template for adding new patterns?

Use `recipes/_template.md` as the contract for new recipe pages.

## How do I contribute a new recipe?

1. Add a recipe file under `recipes/` using `_template.md`.
2. Add a matching runnable example under `examples/`.
3. Add docs page under `docs/recipes/`.
4. Add navigation entry in `mkdocs.yml`.
5. Run checks and open a PR.

See [Contributing Guidelines](contributing.md) for details.

## Why are some examples intentionally simple?

Examples are designed to teach core trigger mechanics clearly. Complex
production concerns are covered in recipe and documentation notes so the
baseline code stays readable.

## Does the cookbook cover Durable Functions?

Not in the initial five core recipes. See [Roadmap](roadmap.md) for future
expansion areas.

## Is OpenAPI support built into Azure Functions Python?

In this repository, OpenAPI capabilities are demonstrated through the
`azure-functions-openapi` ecosystem package used in
`examples/http_api_openapi`.

## How do I test queue and timer recipes quickly?

- Queue: run Azurite and enqueue JSON messages to `work-items`
- Timer: use the admin endpoint to trigger immediately

See [Testing](testing.md) for step-by-step checks.

## Why am I getting webhook signature failures?

Common causes:

- mismatched `GITHUB_WEBHOOK_SECRET`
- missing `X-Hub-Signature-256` header
- signing different bytes than those received by function

See [Troubleshooting](troubleshooting.md) for a full checklist.

## What ecosystem projects are related?

- `azure-functions-scaffold`
- `azure-functions-validation`
- `azure-functions-openapi`
- `azure-functions-logging`
- `azure-functions-doctor`

They complement this cookbook; they do not replace recipe guidance.

## Where should I start if I am new?

Begin with [Installation](installation.md), then [Getting Started](getting-started.md),
then [Recipes Overview](recipes/index.md).
