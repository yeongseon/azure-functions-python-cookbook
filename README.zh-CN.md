# Azure Functions Python Cookbook

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/yeongseon/azure-functions-python-cookbook)
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

- 基础 HTTP API (HTTP API Basic)
- 带有 OpenAPI 的 HTTP API (HTTP API with OpenAPI)
- GitHub Webhook 接收器 (GitHub Webhook Receiver)
- 队列工作者 (Queue Worker)
- 定时器计划任务 (Timer Scheduled Job)

每个食谱都位于 `recipes/` 目录下，并遵循 `_template.md` 格式。

## Repository Layout

```text
recipes/           精选食谱文档
examples/          可运行的示例项目
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

## Disclaimer

本项目是一个独立的社区项目，不隶属于 Microsoft，也不受其认可或维护。

Azure 和 Azure Functions 是 Microsoft Corporation 的商标。

## License

MIT
