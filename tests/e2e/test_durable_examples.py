"""Smoke tests for Durable Functions examples.

Durable Functions require the Durable Task Framework storage backend,
which takes 90+ seconds to initialize with Azurite locally, making
real E2E tests impractical in CI/local environments.

These tests verify that each example's ``function_app.py`` can be imported
successfully, confirming valid Blueprint structure and dependency resolution.
"""

from __future__ import annotations

import importlib
import sys
from types import ModuleType

import pytest

from tests.e2e.conftest import EXAMPLES_ROOT

pytestmark = pytest.mark.smoke


def _import_function_app(example_path: str) -> ModuleType:
    """Import a function_app.py module from an example directory."""
    example_dir = EXAMPLES_ROOT / example_path
    function_app_file = example_dir / "function_app.py"

    if not function_app_file.exists():
        pytest.fail(f"function_app.py not found: {function_app_file}")

    example_dir_str = str(example_dir)
    original_path = sys.path.copy()
    original_modules = set(sys.modules.keys())

    try:
        sys.path.insert(0, example_dir_str)

        # Clear any cached 'app' module to avoid cross-example conflicts
        modules_to_remove = [k for k in sys.modules if k == "app" or k.startswith("app.")]
        for mod_key in modules_to_remove:
            del sys.modules[mod_key]

        spec = importlib.util.spec_from_file_location(
            f"function_app_{example_path.replace('/', '_')}",
            function_app_file,
        )
        if spec is None or spec.loader is None:
            pytest.fail(f"Could not create import spec for {function_app_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path = original_path
        new_modules = set(sys.modules.keys()) - original_modules
        for mod_key in new_modules:
            if mod_key == "app" or mod_key.startswith("app."):
                del sys.modules[mod_key]


# ---------------------------------------------------------------------------
# durable_hello_sequence
# ---------------------------------------------------------------------------


class TestDurableHelloSequence:
    """Verify durable_hello_sequence imports cleanly."""

    def test_module_imports(self) -> None:
        module = _import_function_app("durable/durable_hello_sequence")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# durable_fan_out_fan_in
# ---------------------------------------------------------------------------


class TestDurableFanOutFanIn:
    """Verify durable_fan_out_fan_in imports cleanly."""

    def test_module_imports(self) -> None:
        module = _import_function_app("durable/durable_fan_out_fan_in")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# durable_human_interaction
# ---------------------------------------------------------------------------


class TestDurableHumanInteraction:
    """Verify durable_human_interaction imports cleanly."""

    def test_module_imports(self) -> None:
        module = _import_function_app("durable/durable_human_interaction")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# durable_entity_counter
# ---------------------------------------------------------------------------


class TestDurableEntityCounter:
    """Verify durable_entity_counter imports cleanly."""

    def test_module_imports(self) -> None:
        module = _import_function_app("durable/durable_entity_counter")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# durable_retry_pattern
# ---------------------------------------------------------------------------


class TestDurableRetryPattern:
    """Verify durable_retry_pattern imports cleanly."""

    def test_module_imports(self) -> None:
        module = _import_function_app("durable/durable_retry_pattern")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# durable_determinism_gotchas
# ---------------------------------------------------------------------------


class TestDurableDeterminismGotchas:
    """Verify durable_determinism_gotchas imports cleanly."""

    def test_module_imports(self) -> None:
        module = _import_function_app("durable/durable_determinism_gotchas")
        assert hasattr(module, "app")


# ---------------------------------------------------------------------------
# durable_unit_testing
# ---------------------------------------------------------------------------


class TestDurableUnitTesting:
    """Verify durable_unit_testing imports cleanly."""

    def test_module_imports(self) -> None:
        module = _import_function_app("durable/durable_unit_testing")
        assert hasattr(module, "app")
