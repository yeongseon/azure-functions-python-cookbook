# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.2] - 2026-03-21

### Added

- 28 production-quality example recipes restructured to Blueprint pattern
- E2E test infrastructure with Azurite + func host
- Configuration guide (`configuration.md`) and API reference (`api.md`)
- Mermaid diagrams for architecture documentation

### Changed

- GitHub Actions versions upgraded to Node.js 24 compatible versions
- Repository consistency fixes (LICENSE, .gitignore standardization)
- Coverage threshold enforced at 95%

### Fixed

- Repair broken recipe links in `index.md` and `configuration.md`
- Exclude e2e/smoke from default test run

## [0.1.1] - 2026-03-14

### Added

- Unified tooling: Ruff (lint + format), pre-commit hooks, standardized Makefile
- Comprehensive documentation overhaul (MkDocs site with standardized nav)
- Translated README files (Korean, Japanese, Chinese)
- Standardized documentation quality across ecosystem
- GitHub Pages docs workflow (`.github/workflows/docs.yml`)
- 5 runnable example projects with smoke tests

## [0.1.0] - 2026-03-08

### Added

- Initial repository structure for the Azure Functions Python Cookbook
- Common repository tooling, CI workflows, and release workflow
- Initial product documents: README, AGENT, DESIGN, and PRD
- Initial documentation site structure
- Initial recipe placeholders and recipe template
