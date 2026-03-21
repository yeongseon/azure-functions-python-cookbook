# pyright: reportMissingImports=false, reportUnknownVariableType=false
from azure_functions_python_cookbook import __version__


def test_version_is_present() -> None:
    assert __version__ == "0.1.2"
