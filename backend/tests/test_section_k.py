"""Tests for the Section K calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_k
from groundbill.models import ContractRoute, Project
from tests.fixtures.section_k_site import build_section_k_site


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


def test_k1_1_moisture_content():
    items = compute_section_k(build_section_k_site())
    # K1.1 = E2 = 20 + 5 + 1.5 + 10 = 36.5
    assert _by_code(items, "K1.1").quantity == pytest.approx(36.5)


def test_k1_2_atterberg_limits():
    items = compute_section_k(build_section_k_site())
    # K1.2 = 0.5 × 36.5 = 18.25
    assert _by_code(items, "K1.2").quantity == pytest.approx(18.25)


def test_k1_9_bulk_density():
    items = compute_section_k(build_section_k_site())
    # K1.9 = 0.25 × 36.5 = 9.125
    assert _by_code(items, "K1.9").quantity == pytest.approx(9.125)


def test_k1_12_triaxial():
    items = compute_section_k(build_section_k_site())
    # K1.12 = 0.25 × 36.5 = 9.125
    assert _by_code(items, "K1.12").quantity == pytest.approx(9.125)


def test_empty_project_produces_zero_quantities():
    items = compute_section_k(_empty_project())
    for code in ("K1.1", "K1.2", "K1.9", "K1.12"):
        assert _by_code(items, code).quantity == 0, code


def test_static_items():
    items = compute_section_k(build_section_k_site())
    static_codes = [f"K1.{i}" for i in range(3, 91) if i not in (9, 12)]
    for code in static_codes:
        assert _by_code(items, code).quantity == "Not Required", code


def test_item_codes_are_unique_within_section_k():
    codes = _codes(compute_section_k(build_section_k_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section K: {codes}"


def test_section_k_item_count_is_stable():
    assert len(compute_section_k(_empty_project())) == len(
        compute_section_k(build_section_k_site())
    )


def test_section_k_has_90_items():
    items = compute_section_k(_empty_project())
    assert len(items) == 90
