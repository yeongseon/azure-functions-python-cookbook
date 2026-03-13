# Azure Functions Python Cookbook

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/yeongseon/azure-functions-python-cookbook)
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

- 基本的なHTTP API (HTTP API Basic)
- OpenAPI対応のHTTP API (HTTP API with OpenAPI)
- GitHub Webhook 受信機 (GitHub Webhook Receiver)
- キューワーカー (Queue Worker)
- タイマー定期実行ジョブ (Timer Scheduled Job)

各レシピは `recipes/` 配下にあり、`_template.md` 形式に従っています。

## Repository Layout

```text
recipes/           厳選されたレシピドキュメント
examples/          実行可能なサンプルプロジェクト
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

## Ecosystem

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
