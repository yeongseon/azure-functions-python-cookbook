# Recipes Overview

The cookbook currently ships five core recipes aligned to common Azure
Functions Python v2 workloads.

!!! info
    Each recipe page is paired with a runnable project in `examples/`.
    Read the recipe, then run the matching example.

## Catalog

| Recipe | Trigger | Difficulty | Best for | Example |
| --- | --- | --- | --- | --- |
| [HTTP API Basic](http-api-basic.md) | HTTP | Beginner | Small REST APIs and CRUD baselines | `examples/http_api_basic` |
| [HTTP API with OpenAPI](http-api-openapi.md) | HTTP | Intermediate | Contract-first API docs and discoverability | `examples/http_api_openapi` |
| [GitHub Webhook](github-webhook.md) | HTTP | Intermediate | Signed event ingestion and routing | `examples/github_webhook` |
| [Queue Worker](queue-worker.md) | Queue | Intermediate | Async background processing | `examples/queue_worker` |
| [Timer Job](timer-job.md) | Timer | Beginner | Scheduled automation and maintenance | `examples/timer_job` |

## Quick comparison

| Capability | HTTP Basic | HTTP OpenAPI | GitHub Webhook | Queue Worker | Timer Job |
| --- | --- | --- | --- | --- | --- |
| Public HTTP endpoints | Yes | Yes | Inbound webhook only | No | No |
| Auto-generated API docs | No | Yes | No | No | No |
| Signature validation | Optional | Optional | Required | N/A | N/A |
| Retry semantics | Client-driven | Client-driven | Delivery retries from GitHub | Runtime dequeue retry | Schedule + catch-up semantics |
| Local emulator dependency | No | No | No | Azurite recommended | No |

## Prerequisites by recipe

### Shared prerequisites

- Python 3.10+
- Azure Functions Core Tools v4
- Virtual environment for dependencies

### Additional prerequisites

- HTTP OpenAPI: `azure-functions-openapi`
- GitHub Webhook: `GITHUB_WEBHOOK_SECRET`
- Queue Worker: Azurite and storage connection config

## How to choose quickly

Pick by first constraint:

1. Need synchronous request/response API -> HTTP recipes.
2. Need external event ingestion with trust boundary -> GitHub Webhook.
3. Need decoupled async workload -> Queue Worker.
4. Need periodic execution -> Timer Job.

Then pick by second constraint:

- Need Swagger/OpenAPI output -> HTTP API with OpenAPI.
- Need minimal baseline and speed -> HTTP API Basic.

## Structure of each recipe page

Every deep-dive page in this section follows a production-oriented contract:

- Overview and use case
- Text architecture diagram
- Prerequisites
- Step-by-step implementation
- Code walkthrough based on real example code
- Local run and test instructions
- Expected output examples
- Production considerations
- Related recipes and ecosystem links

## Workflow recommendation

```text
Read recipe page -> Run matching example -> Validate expected output ->
Adapt for your domain -> Add tests and checks -> Deploy
```

## Related user guides

- [Installation](../installation.md)
- [Getting Started](../getting-started.md)
- [Usage](../usage.md)
- [Testing](../testing.md)
- [Troubleshooting](../troubleshooting.md)

## Recipe source documents

If you want the raw recipe narratives used to build these docs, see:

- `recipes/http-api-basic.md`
- `recipes/http-api-openapi.md`
- `recipes/github-webhook.md`
- `recipes/queue-worker.md`
- `recipes/timer-job.md`
- `recipes/_template.md`

!!! tip
    When contributing a new pattern, update both the source recipe file in
    `recipes/` and its reader-friendly page in `docs/recipes/`.
