"""Tests for the Section L calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_l
from groundbill.models import ContractRoute, Project
from tests.fixtures.section_l_site import build_section_l_site


def _codes(items: list[BoqItem]) -> list[str]:
    return [i.code for i in items]


def _by_code(items: list[BoqItem], code: str) -> BoqItem:
    matches = [i for i in items if i.code == code]
    assert len(matches) == 1, f"Expected exactly one item with code {code}, got {len(matches)}"
    return matches[0]


def _empty_project() -> Project:
    return Project(
        name="Empty",
        site_address="Nowhere",
        contract_route=ContractRoute.PRIVATE,
    )


def test_l1_chemical_testing():
    items = compute_section_l(build_section_l_site())
    # ev_count = 5, L.1 = 5 / 5 = 1.0
    assert _by_code(items, "L.1").quantity == pytest.approx(1.0)


def test_l5_groundwater_analysis():
    items = compute_section_l(build_section_l_site())
    # L.5 = L.1 = 1.0
    assert _by_code(items, "L.5").quantity == pytest.approx(1.0)


def test_l1_equals_l5():
    items = compute_section_l(build_section_l_site())
    assert _by_code(items, "L.1").quantity == _by_code(items, "L.5").quantity


def test_empty_project_produces_zero_quantities():
    items = compute_section_l(_empty_project())
    for code in ("L.1", "L.5"):
        assert _by_code(items, code).quantity == 0, code


def test_static_items():
    items = compute_section_l(build_section_l_site())
    for code in ("L.2", "L.3", "L.4", "L.6", "L.7"):
        assert _by_code(items, code).quantity == "Not Required", code


def test_item_codes_are_unique_within_section_l():
    codes = _codes(compute_section_l(build_section_l_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section L: {codes}"


def test_section_l_item_count_is_stable():
    assert len(compute_section_l(_empty_project())) == len(
        compute_section_l(build_section_l_site())
    )


def test_section_l_has_7_items():
    items = compute_section_l(_empty_project())
    assert len(items) == 7
