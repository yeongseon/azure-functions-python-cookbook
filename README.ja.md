# Azure Functions Python Cookbook

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/yeongseon/azure-functions-python-cookbook)
[![CI](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/ci-smoke.yml/badge.svg)](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/ci-smoke.yml)
[![Docs](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/docs.yml/badge.svg)](https://github.com/yeongseon/azure-functions-python-cookbook/actions/workflows/docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

他の言語: [English](README.md) | [한국어](README.ko.md) | [简体中文](README.zh-CN.md)

Pythonを使用して実用的なAzure Functionsを構築するためのレシピ集です。

## Why Use It

新しいAzure Functionsプロジェクトを開始する際、散在するドキュメント、ブログ記事、サンプルコードを繋ぎ合わせるのは時間がかかります。このクックブックでは、以下のような疑問に応える、厳選された実行可能なレシピを提供します。

- このシナリオでは何を構築すべきか？
- アーキテクチャはどのような構成にすべきか？
- どのようにして動作するベースラインから開始できるか？

## Scope

- Azure Functions Python **v2 プログラミングモデル**
- デコレータベースの `func.FunctionApp()` アプリケーション
- 実行可能な例を含む実用的なレシピ
- アーキテクチャの解説と本番環境での注意点

本リポジトリはコンテンツを重視しており、CLIツールではありません。

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

各レシピは `recipes/` 配下にあり、対応する実行可能プロジェクトが `examples/` にあります。

## Repository Layout

```text
recipes/           厳選されたレシピドキュメント（31レシピ）
examples/          カテゴリ別実行可能プロジェクト
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
docs/              公開ドキュメント
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

- 製品要件: `PRD.md`
- 設計原則: `DESIGN.md`
- コントリビューションガイド: `CONTRIBUTING.md`

## Ecosystem (Optional)

これらのコンパニオンパッケージは**オプションのアクセラレーター**です — クックブックは単独で完全に動作します。
プロジェクトが成長し、追加のインフラが必要になったときに使用してください：
- [azure-functions-validation](https://github.com/yeongseon/azure-functions-validation) — リクエストとレスポンスのバリデーション
- [azure-functions-openapi](https://github.com/yeongseon/azure-functions-openapi) — OpenAPI と Swagger UI
- [azure-functions-logging](https://github.com/yeongseon/azure-functions-logging) — 構造化ロギング
- [azure-functions-doctor](https://github.com/yeongseon/azure-functions-doctor) — 診断 CLI
- [azure-functions-scaffold](https://github.com/yeongseon/azure-functions-scaffold) — プロジェクトスキャフォールディング

## Disclaimer

本プロジェクトは独立したコミュニティプロジェクトであり、Microsoftと提携、承認、または保守されているものではありません。

AzureおよびAzure Functionsは、Microsoft Corporationの商標です。

## License

MIT
