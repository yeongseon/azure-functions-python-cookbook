# Usage

This page explains how to use the cookbook effectively as a recipe catalog.

## Core model

Use the repository in this order:

1. Pick a pattern in `recipes/`.
2. Run the matching implementation in `examples/`.
3. Adapt the sample for your own function app.
4. Validate with tests, lint, and security checks.

!!! info
    There is no package API to import from this repository for app runtime.
    The value is in the recipe content and runnable examples.

## How recipes are organized

Current recipes:

- `http-api-basic`
- `http-api-openapi`
- `github-webhook`
- `queue-worker`
- `timer-job`

Each recipe targets a specific trigger style and operational concern.

| Recipe | Trigger | Focus |
| --- | --- | --- |
| HTTP API Basic | HTTP | Route design, request handling, CRUD baseline |
| HTTP API with OpenAPI | HTTP | API contract generation and Swagger UX |
| GitHub Webhook | HTTP | Signature validation, event routing |
| Queue Worker | Queue | Async processing, retries, message safety |
| Timer Job | Timer | Scheduled execution, deterministic periodic tasks |

## Recipe format contract

New or updated recipe files should follow `recipes/_template.md`:

- Overview
- When to Use
- Architecture
- Project Structure
- Run Locally
- Production Considerations
- Scaffold Starter

This consistent section contract keeps pages easy to scan and compare.

## Mapping between recipes and examples

Each recipe has a runnable app under `examples/`:

- `recipes/http-api-basic.md` -> `examples/http_api_basic`
- `recipes/http-api-openapi.md` -> `examples/http_api_openapi`
- `recipes/github-webhook.md` -> `examples/github_webhook`
- `recipes/queue-worker.md` -> `examples/queue_worker`
- `recipes/timer-job.md` -> `examples/timer_job`

!!! tip
    Keep docs and example code aligned in the same pull request.
    If behavior changes in code, update recipe narrative and run instructions.

## Typical usage patterns

### Pattern discovery

- Start with [Recipes Overview](recipes/index.md)
- Select by trigger and operational needs
- Open the deep-dive recipe page

### Prototype quickly

- Copy structure from an existing example
- Keep trigger decorator style (`func.FunctionApp` v2 model)
- Replace placeholder business logic first

### Production hardening

- Add input validation and explicit status codes
- Add idempotency for webhook and queue workflows
- Add observability and clear error paths
- Add security controls from [Security](security.md)

## Contributing new recipes

Recommended flow:

1. Duplicate `recipes/_template.md` into a new recipe page.
2. Add a matching runnable project under `examples/`.
3. Document local run steps and expected output.
4. Include production constraints and failure behavior.
5. Add docs navigation entry in `mkdocs.yml`.

See [Contributing Guidelines](contributing.md) for review standards.

## Ecosystem integration

The cookbook is designed to work with companion projects:

- `azure-functions-scaffold` for generating starter projects
- `azure-functions-validation` for request/response validation helpers
- `azure-functions-openapi` for contract generation and Swagger UI
- `azure-functions-logging` for structured logs
- `azure-functions-doctor` for local environment checks

Use recipes as the architecture baseline, then apply ecosystem tooling
incrementally as your app matures.

## Anti-patterns to avoid

- Treating examples as production-ready without review
- Copying snippets without local test execution
- Keeping secrets in source code
- Ignoring retry/idempotency behavior for queue and webhook patterns
- Updating examples without updating documentation

## Useful links

- Start here: [Getting Started](getting-started.md)
- Build and test: [Development](development.md), [Testing](testing.md)
- Diagnose problems: [Troubleshooting](troubleshooting.md)
- Read all recipes: [Recipes Overview](recipes/index.md)
