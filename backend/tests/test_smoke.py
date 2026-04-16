"""Minimal smoke test — confirms the package imports and pytest is wired up."""

import groundbill


def test_package_imports():
    assert groundbill.__version__ == "0.1.0"
