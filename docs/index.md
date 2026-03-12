# Azure Functions Python Cookbook

The Azure Functions Python Cookbook provides a collection of practical recipes for building serverless applications with the Python v2 programming model. This resource is for developers who want to move beyond basic hello world examples and implement production-ready patterns for real-world scenarios.

## Why This Cookbook

Developers often find that official documentation is scattered across multiple services and lacks cohesive examples for complex workflows. While basic tutorials show how to create a single function, they rarely provide guidance on project structure, validation, or long-term maintenance. This cookbook solves these problems by offering curated recipes that follow best practices for the Azure Functions v2 decorator-based model.

Each recipe includes runnable examples and architecture guidance to ensure that your implementation is both efficient and scalable. We focus on providing a clear path from local development to production deployment, addressing common challenges like structured logging and request validation that are frequently omitted from standard documentation.

## What You Will Find

The cookbook is organized into five primary recipe categories that address the most common serverless integration patterns:

- HTTP API Basic: Simple REST endpoints implemented with Azure Functions v2 decorators for standard request-response cycles.
- HTTP API with OpenAPI: Implementation of auto-generated API documentation using the azure-functions-openapi library for better developer experience.
- GitHub Webhook Receiver: Event-driven processing of GitHub webhook payloads with security checks and asynchronous handling.
- Queue Worker: Background processing patterns using Azure Storage Queue bindings to decouple long-running tasks from the main execution flow.
- Timer Scheduled Job: Cron-based periodic task execution for maintenance jobs, data synchronization, and automated reporting.

## How Recipes Are Structured

To ensure consistency and ease of use, every recipe in this cookbook follows a strict contract. This structure allows you to quickly evaluate if a recipe fits your needs and provides all the information required for implementation:

- Overview: A high-level description of the recipe and the specific problem it solves.
- When to Use: Guidance on the scenarios where this pattern is most effective and when to consider alternatives.
- Architecture: A technical breakdown of how the components interact within the Azure environment.
- Project Structure: A visual representation of the recommended file and directory layout for the recipe.
- Local Run Instructions: Step-by-step commands to get the recipe running on your local machine using the Azure Functions Core Tools.
- Production Considerations: Critical advice on security, performance, and monitoring for live environments.
- Scaffold Guidance: Instructions on how to use the recipe as a template with our scaffolding tools.

## Getting Started

You can begin using the cookbook by cloning the repository and setting up your local environment. We provide a Makefile to automate common setup tasks:

```bash
git clone https://github.com/yeongseonchoe/azure-functions-python-cookbook.git
cd azure-functions-python-cookbook
make install
make docs
```

The documentation server will start locally, allowing you to browse all recipes and detailed guides in your browser.

## Related Projects

The cookbook is part of a larger ecosystem of tools designed to simplify Azure Functions development. These libraries are used throughout the recipes to provide essential functionality:

- [azure-functions-scaffold](https://github.com/yeongseonchoe/azure-functions-scaffold): A CLI tool for project scaffolding that uses cookbook recipes as templates.
- [azure-functions-validation](https://github.com/yeongseonchoe/azure-functions-validation): A library for robust request validation using Pydantic models.
- [azure-functions-openapi](https://github.com/yeongseonchoe/azure-functions-openapi): Tools for generating OpenAPI specifications directly from your function code.
- [azure-functions-logging](https://github.com/yeongseonchoe/azure-functions-logging): Utilities for structured logging and integration with Azure Monitor.
- [azure-functions-doctor](https://github.com/yeongseonchoe/azure-functions-doctor): A diagnostic tool for verifying your local development environment and Azure configurations.

## Repository Layout

The repository is organized to separate documentation from implementation details. This layout ensures that recipes are easy to discover and examples are simple to run:

```text
.
├── docs/                   # Documentation source files and static assets
├── examples/               # Complete, runnable example projects for each recipe
├── recipes/                # Recipe metadata and architectural guidance
└── src/                    # Supporting source code and shared utilities
```

- docs: Contains the markdown files used to build this documentation site.
- examples: Provides isolated environments where you can test each recipe individually.
- recipes: Holds the core content for each pattern, including the technical specs and diagrams.
- src: Includes common logic that is shared across multiple examples to reduce duplication.

## License

This project is licensed under the MIT License. You are free to use the recipes and examples in your own projects, provided that you include the original license and copyright notice.

The recipes provided here are intended as starting points. We encourage you to adapt them to your specific requirements and contribute improvements back to the community if you find ways to make them more effective.

The cookbook is a living resource. We regularly update it to reflect changes in the Azure Functions platform and the evolving Python ecosystem. If you encounter issues or have suggestions for new recipes, please open an issue in the repository.

Our goal is to build the most comprehensive resource for Python developers on Azure. By following the patterns established in this cookbook, you can focus on writing business logic rather than fighting with infrastructure configuration and boilerplate code.

We hope these recipes help you build better serverless applications.

Thank you for choosing the Azure Functions Python Cookbook.

For more information on the Azure Functions Python v2 model, please refer to the official Microsoft documentation and the Azure Functions Core Tools repository.

Happy coding.

The Cookbook Team.

Building serverless applications requires a deep understanding of both the cloud provider's infrastructure and the specific nuances of the programming language being used. This cookbook bridges that gap for Python developers.

Our team has spent significant time identifying the most common patterns and pain points in Azure Functions development. We believe that by providing clear, reusable code examples, we can help the community build more reliable and maintainable systems.

Whether you are building a simple webhook or a complex data processing pipeline, the principles outlined in this cookbook will help you navigate the complexities of cloud-native development.

We look forward to seeing what you build with these tools.

Community contributions are always welcome. If you have a pattern that you believe would benefit others, please feel free to submit a pull request with a new recipe following our established structure.

Together, we can create a robust library of patterns that empowers every Python developer to succeed on the Azure platform.

Stay tuned for updates as we continue to expand our collection of recipes and integration examples.

The documentation is built using MkDocs and the Material theme for a clean and responsive reading experience across all devices.

If you have questions that aren't addressed in the recipes, please check our GitHub Discussions page or join our community chat for real-time assistance.

Your feedback is essential to making this resource better for everyone.

Thank you for your support and interest in the Azure Functions Python Cookbook.
