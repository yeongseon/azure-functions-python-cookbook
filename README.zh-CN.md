# Azure Functions Python Cookbook

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/yeongseon/azure-functions-python-cookbook)
[![CI](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/ci-smoke.yml/badge.svg)](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/ci-smoke.yml)
[![Docs](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/docs.yml/badge.svg)](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

其他语言: [English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

使用 Python 构建实际 Azure Functions 的实用食谱集合。

## Why Use It

启动新的 Azure Functions 项目时，往往需要整合零散的文档、博客文章和示例代码。本食谱提供精选的、可运行的示例，旨在回答：

- 针对此场景我应该构建什么？
- 架构应该是什么样的？
- 我如何从一个可工作的基准开始？

## Scope

- Azure Functions Python **v2 编程模型**
- 基于装饰器的 `func.FunctionApp()` 应用程序
- 包含可运行示例的实用食谱
- 架构说明和生产环境注意事项

本仓库以内容为主，不是 CLI 工具。

## Recipes

### HTTP

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Hello HTTP Minimal | Beginner | Smallest possible HTTP trigger |
| HTTP Routing, Query, and Body | Beginner | Route params, query strings, JSON body, status codes |
| HTTP Auth Levels | Beginner | Anonymous, Function, and Admin auth levels |
| GitHub Webhook | Intermediate | HMAC-SHA256 signature verification |
| EasyAuth Claims | Intermediate | EasyAuth principal extraction with role-based access control |
| JWT Bearer Validation | Intermediate | JWT Bearer token validation with claim-based access control |
| Multi-Tenant Auth | Intermediate | Multi-tenant access control with tenant allowlist |

### Timer

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Timer Cron Job | Beginner | NCRONTAB expressions, timezone, catch-up |

### Queue

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Queue Producer | Beginner | HTTP trigger with Queue output binding |
| Queue Consumer | Beginner | Queue trigger message processing |

### Blob

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Blob Upload Processor | Intermediate | Polling-based blob trigger |
| Blob Event Grid Trigger | Intermediate | Event Grid-based blob trigger (faster) |

### Service Bus

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Service Bus Worker | Intermediate | Service Bus queue trigger |

### Event Hub

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Event Hub Consumer | Intermediate | Event Hub stream processing |

### Cosmos DB

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Change Feed Processor | Intermediate | Cosmos DB change feed trigger |

### Patterns

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Blueprint Modular App | Intermediate | Modular function apps with Blueprints |
| Retry and Idempotency | Intermediate | Retry policies and idempotency patterns |
| Output Binding vs SDK | Intermediate | Side-by-side binding vs SDK client comparison |
| Managed Identity (Storage) | Advanced | Identity-based Storage connection |
| Managed Identity (Service Bus) | Advanced | Identity-based Service Bus connection |
| host.json Tuning | Advanced | host.json configuration guide |
| Concurrency Tuning | Advanced | Dynamic concurrency for Queue/Blob/Service Bus |

### Durable Functions

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Hello Sequence | Beginner | Activity chaining pattern |
| Fan-Out / Fan-In | Intermediate | Parallel activity execution |
| Human Interaction | Intermediate | External events with timeout |
| Entity Counter | Intermediate | Durable entity state management |
| Retry Pattern | Intermediate | Activity retry with RetryOptions |
| Determinism Gotchas | Advanced | Orchestrator determinism rules |
| Unit Testing | Intermediate | Mock-based orchestrator testing |

### AI

| Recipe | Difficulty | Description |
| --- | --- | --- |
| MCP Server | Advanced | Model Context Protocol server on Azure Functions |

### Local Development

| Recipe | Difficulty | Description |
| --- | --- | --- |
| Local Run and Direct Invoke | Beginner | func start vs direct Python invocation |

每个食谱都位于 `recipes/` 目录下，对应的可运行项目在 `examples/` 中。

## Repository Layout

```text
recipes/           精选食谱文档（31个食谱）
examples/          按类别组织的可运行示例项目
  http/            HTTP trigger examples
  timer/           Timer trigger examples
  queue/           Queue trigger examples
  blob/            Blob trigger examples
  servicebus/      Service Bus trigger examples
  eventhub/        Event Hub trigger examples
  cosmosdb/        Cosmos DB trigger examples
  recipes/         Pattern and recipe examples
  durable/         Durable Functions examples
  ai/              AI integration examples
docs/              发布的文档
```

## Development

```bash
git clone https://github.com/yeongseon/azure-functions-python-cookbook.git
cd azure-functions-python-cookbook
make install
make check-all
make docs
```

## Documentation

- 产品需求: `PRD.md`
- 设计原则: `DESIGN.md`
- 贡献指南: `CONTRIBUTING.md`

## Ecosystem (Optional)

这些配套包是**可选的加速器** — 食谱集可以完全独立使用。
当您的项目扩展并需要额外基础设施时使用：
- [azure-functions-validation](https://github.com/yeongseon/azure-functions-validation) — 请求与响应校验
- [azure-functions-openapi](https://github.com/yeongseon/azure-functions-openapi) — OpenAPI 与 Swagger UI
- [azure-functions-logging](https://github.com/yeongseon/azure-functions-logging) — 结构化日志
- [azure-functions-doctor](https://github.com/yeongseon/azure-functions-doctor) — 诊断 CLI
- [azure-functions-scaffold](https://github.com/yeongseon/azure-functions-scaffold) — 项目脚手架

## Disclaimer

本项目是一个独立的社区项目，不隶属于 Microsoft，也不受其认可或维护。

Azure 和 Azure Functions 是 Microsoft Corporation 的商标。

## License

MIT
