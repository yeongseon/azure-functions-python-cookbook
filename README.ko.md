# Azure Functions Python Cookbook

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/yeongseon/azure-functions-python-cookbook)
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

- 기본 HTTP API (HTTP API Basic)
- OpenAPI를 포함한 HTTP API (HTTP API with OpenAPI)
- GitHub 웹훅 수신기 (GitHub Webhook Receiver)
- 큐 워커 (Queue Worker)
- 타이머 예약 작업 (Timer Scheduled Job)

각 레시피는 `recipes/` 디렉토리에 있으며 `_template.md` 형식을 따릅니다.

## Repository Layout

```text
recipes/           엄선된 레시피 문서
examples/          실행 가능한 예제 프로젝트
docs/              게시된 문서
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

- 제품 요구사항: `PRD.md`
- 설계 원칙: `DESIGN.md`
- 기여 가이드: `CONTRIBUTING.md`

## Ecosystem

- [azure-functions-validation](https://github.com/yeongseon/azure-functions-validation) — 요청 및 응답 검증
- [azure-functions-openapi](https://github.com/yeongseon/azure-functions-openapi) — OpenAPI 및 Swagger UI
- [azure-functions-logging](https://github.com/yeongseon/azure-functions-logging) — 구조화된 로깅
- [azure-functions-doctor](https://github.com/yeongseon/azure-functions-doctor) — 진단 CLI
- [azure-functions-scaffold](https://github.com/yeongseon/azure-functions-scaffold) — 프로젝트 스캐폴딩

## Disclaimer

본 프로젝트는 독립적인 커뮤니티 프로젝트이며, Microsoft와 제휴하거나 Microsoft의 보증 또는 지원을 받지 않습니다.

Azure 및 Azure Functions는 Microsoft Corporation의 상표입니다.

## License

MIT
