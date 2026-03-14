# Installation

This project is a documentation-first cookbook for Azure Functions Python v2.
You do not install it as a package to use an API. Instead, you clone the
repository, read a recipe, and run one of the matching example projects.

!!! info "Cookbook vs library"
    `azure-functions-python-cookbook` is not a runtime dependency.
    It is a recipe collection with runnable reference apps under `examples/`.

## Prerequisites

- Python `3.10` through `3.14` (the project currently targets `>=3.10,<3.15`)
- Azure Functions Core Tools v4 (`func` command)
- Git
- Optional: Azurite for local queue testing
- Optional: GNU Make for standardized development/test commands

## Clone the Repository

```bash
git clone https://github.com/yeongseon/azure-functions-python-cookbook.git
cd azure-functions-python-cookbook
```

## Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

## Install Development Dependencies

You can use either the Makefile workflow or direct `pip` commands.

### Option A: Makefile workflow (recommended)

```bash
make install
```

This bootstraps Hatch and installs the project environments used for
linting, testing, security checks, and docs.

### Option B: pip workflow

```bash
pip install -e ".[dev,docs]"
```

## Verify Tooling

```bash
func --version
python --version
```

If you plan to run queue recipes locally, start Azurite in another terminal:

```bash
azurite --queuePort 10001
```

## Project Structure Overview

```text
azure-functions-python-cookbook/
  docs/                 Published documentation site content
  recipes/              Source recipe documents (pattern narratives)
  examples/             Runnable Azure Functions sample apps
    http_api_basic/
    http_api_openapi/
    github_webhook/
    queue_worker/
    timer_job/
  src/                  Internal package metadata and tooling support
  tests/                Repository test suite
  mkdocs.yml            Documentation site navigation and config
  Makefile              Standardized developer commands
```

## Run a First Example

```bash
cd examples/http_api_basic
pip install -r requirements.txt
func start
```

Then call:

```bash
curl http://localhost:7071/api/items
```

## What to Read Next

- Start with [Getting Started](getting-started.md)
- Compare recipes in [Recipes Overview](recipes/index.md)
- Understand the architecture in [Architecture](architecture.md)

!!! tip "New contributors"
    If you want to improve cookbook content, continue with
    [Development](development.md), [Testing](testing.md), and
    [Contributing Guidelines](contributing.md).
