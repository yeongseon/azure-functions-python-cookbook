# Azure Functions Python Cookbook

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/yeongseon/azure-functions-cookbook-python)
[![CI](https://github.com/yeongseon/azure-functions-cookbook-python/actions/workflows/ci-smoke.yml/badge.svg)](https://github.com/yeongseon/azure-functions-cookbook-python/actions/workflows/ci-smoke.yml)
[![Docs](https://github.com/yeongseon/azure-functions-cookbook-python/actions/workflows/docs.yml/badge.svg)](https://github.com/yeongseon/azure-functions-cookbook-python/actions/workflows/docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

다른 언어: [English](README.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

Python으로 실제 서비스 가능한 Azure Functions를 구축하기 위한 실용적인 레시피 모음입니다.

## Why Use It

새로운 Azure Functions 프로젝트를 시작할 때 흩어져 있는 문서나 블로그 포스트, 샘플 코드를 일일이 찾아 맞추는 일은 번거롭습니다. 이 쿡북은 다음과 같은 질문에 답이 되는 엄선된 실행 가능한 레시피를 제공합니다.

- 이 시나리오에서는 무엇을 구축해야 할까?
- 아키텍처는 어떤 모습이어야 할까?
- 검증된 기본 코드에서 어떻게 시작할 수 있을까?

## Scope

- Azure Functions Python **v2 프로그래밍 모델**
- 데코레이터 기반 `func.FunctionApp()` 애플리케이션
- 실행 가능한 예제가 포함된 실용적인 레시피
- 아키텍처 설명 및 운영 시 고려사항

이 저장소는 콘텐츠 중심으로 구성되었습니다. CLI 도구가 아닙니다.

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

각 레시피는 `recipes/` 디렉토리에 있으며 실행 가능한 예제가 `examples/`에 있습니다.

## Repository Layout

```text
recipes/           엄선된 레시피 문서 (31개 레시피)
examples/          카테고리별 실행 가능한 예제 프로젝트
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
docs/              게시된 문서
```

## Development

```bash
git clone https://github.com/yeongseon/azure-functions-cookbook-python.git
cd azure-functions-cookbook-python
make install
make check-all
make docs
```

## Documentation

- 제품 요구사항: `PRD.md`
- 설계 원칙: `DESIGN.md`
- 기여 가이드: `CONTRIBUTING.md`

## Ecosystem (Optional)

이 컴패니언 패키지는 **선택적 가속기**입니다 — 쿡북은 독립적으로 완전히 동작합니다.
프로젝트가 성장하여 추가 인프라가 필요할 때 사용하세요:
- [azure-functions-validation-python](https://github.com/yeongseon/azure-functions-validation-python) — 요청 및 응답 검증
- [azure-functions-openapi-python](https://github.com/yeongseon/azure-functions-openapi-python) — OpenAPI 및 Swagger UI
- [azure-functions-logging-python](https://github.com/yeongseon/azure-functions-logging-python) — 구조화된 로깅
- [azure-functions-doctor-python](https://github.com/yeongseon/azure-functions-doctor-python) — 진단 CLI
- [azure-functions-scaffold-python](https://github.com/yeongseon/azure-functions-scaffold-python) — 프로젝트 스캐폴딩

## Disclaimer

본 프로젝트는 독립적인 커뮤니티 프로젝트이며, Microsoft와 제휴하거나 Microsoft의 보증 또는 지원을 받지 않습니다.

Azure 및 Azure Functions는 Microsoft Corporation의 상표입니다.

## License

MIT
