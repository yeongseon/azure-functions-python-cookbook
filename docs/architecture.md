# Architecture

## Overview

Azure Functions Python Cookbook is a content-first repository. It is not a library,
CLI tool, or framework. Its purpose is to provide curated, production-quality
recipes for building serverless applications with Azure Functions and the
Python v2 programming model.

Each recipe documents a complete implementation pattern: the problem it solves,
the architecture behind it, the file layout, and the production considerations
that matter when the code runs at scale.

## Ecosystem Positioning

The cookbook sits at the discovery layer of the Azure Functions Python workflow.
It helps developers choose the right pattern before committing to a project
structure.

```text
Cookbook       ->    Scaffold       ->    Development
(discover)         (generate)            (build)
```

- **Cookbook**: Browse recipes, understand tradeoffs, pick a pattern.
- **Scaffold**: Generate a project from the chosen pattern using
  `azure-functions-scaffold`.
- **Development**: Build the application with supporting libraries
  (`azure-functions-validation`, `azure-functions-openapi`,
  `azure-functions-logging`, `azure-functions-doctor`).

The cookbook feeds into scaffold templates. When a recipe includes a
"Scaffold Starter" section, it maps directly to a scaffold template that
generates the corresponding project structure.

## Information Architecture

The repository is organized into three layers, each serving a distinct role.

### recipes/

Source recipe documents written in Markdown. Each file covers one scenario
end-to-end: overview, when to use, architecture, project structure, local
run instructions, production considerations, and scaffold guidance.

Recipe files are the canonical source of truth for implementation patterns.
The published documentation references these files but does not duplicate them.

### examples/

Runnable or near-runnable Azure Functions projects. Each example corresponds
to a recipe and provides working code that developers can clone, run locally
with `func start`, and deploy to Azure.

Examples follow the Azure Functions Python v2 programming model using
decorator-based `func.FunctionApp()` applications.

### docs/

The published documentation site built with MkDocs and the Material theme.
This layer provides navigation, cross-referencing, and a searchable index
over the recipe catalog.

Documentation pages reference recipes and examples but keep their own
editorial structure for readability.

## Recipe Structure

Every recipe follows a standard contract defined in `recipes/_template.md`.
This consistency makes recipes predictable and easy to navigate.

| Section | Purpose |
|---------|---------|
| Overview | One-paragraph problem statement and what the recipe demonstrates |
| When to Use | Concrete scenarios where this pattern applies |
| Architecture | Request flow, moving parts, and an ASCII diagram |
| Project Structure | File layout with annotations |
| Run Locally | Step-by-step commands to test locally |
| Production Considerations | Scaling, retries, idempotency, observability, security |
| Scaffold Starter | Command to generate the project with azure-functions-scaffold |

Each section exists for a reason:

- **Overview** anchors the reader in the problem space before showing the solution.
- **When to Use** prevents misapplication of patterns.
- **Architecture** builds mental models before code appears.
- **Project Structure** sets expectations for file organization.
- **Run Locally** ensures every recipe is testable without deployment.
- **Production Considerations** bridges the gap between demo and production.
- **Scaffold Starter** connects discovery to action.

## Design Principles

These principles guide all content decisions in the cookbook.

1. **Start from a developer problem, not a library feature.** Recipes answer
   "How do I build X?" rather than "Here is what library Y can do."

2. **Keep recipes focused on one use case and one architectural story.**
   A recipe that tries to cover multiple patterns becomes hard to follow
   and harder to maintain.

3. **Pair each recipe with a runnable example.** Documentation without
   working code is incomplete. Every recipe should have a corresponding
   project in `examples/` that a developer can clone and run.

4. **Preserve independence from other repositories at the documentation level.**
   Recipes reference ecosystem tools (scaffold, validation, openapi) but do
   not require them. Each recipe stands on its own.

5. **Keep examples grounded in real Azure Functions Python v2 patterns.**
   Examples use the decorator-based `func.FunctionApp()` API, not legacy
   function.json definitions.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Functions model | Azure Functions Python v2 (decorator-based) |
| Documentation | MkDocs with Material theme |
| Build system | Hatch |
| Linting | Ruff |
| Formatting | Black |
| Type checking | Mypy |
| Testing | Pytest |
| Security scanning | Bandit |

## Future Extension Points

The following capabilities are planned but not yet implemented:

- **Recipe search and tagging**: metadata-driven discovery by trigger type,
  complexity, or use case.
- **Scaffold command mapping**: direct links from recipes to scaffold
  templates for one-command project generation.
- **Static gallery**: a richer landing experience with visual recipe cards
  and filtering.
- **Automated example validation**: CI-driven verification that all example
  projects build, pass tests, and match their recipe descriptions.
