"""Tests for the Section E calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_e
from groundbill.models import (
    ContractRoute,
    Project,
)
from tests.fixtures.section_e_site import build_section_e_site


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


def test_e2_tub_sample_count():
    items = compute_section_e(build_section_e_site())
    # total_cp=20 + tp=5 + trench=0 + ip=1.5 + ds=10 = 36.5
    assert _by_code(items, "E2").quantity == pytest.approx(36.5)


def test_e3_equals_e2():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E3").quantity == _by_code(items, "E2").quantity


def test_e4_large_bulk_sample():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E4").quantity == pytest.approx(3.65)  # 36.5 / 10


def test_e5_thick_walled_samples():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E5").quantity == pytest.approx(4.0)  # 20 / 5


def test_e6_equals_e5():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E6").quantity == _by_code(items, "E5").quantity


def test_e8_1_extra_thick_walled():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E8.1").quantity == pytest.approx(2.0)  # 20 / 10


def test_e8_2_extra_thin_walled():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E8.2").quantity == pytest.approx(2.0)  # 20 / 10


def test_e12_ev_test_count():
    items = compute_section_e(build_section_e_site())
    # BH02 + TP01 + TR01 + IP01 + DS01 = 5
    assert _by_code(items, "E12").quantity == 5


def test_e16_equals_e12():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E16").quantity == _by_code(items, "E12").quantity


def test_empty_project_produces_zero_quantities():
    items = compute_section_e(_empty_project())
    for code in ("E2", "E3", "E4", "E5", "E6", "E8.1", "E8.2", "E12", "E16"):
        assert _by_code(items, code).quantity == 0, code


def test_static_items():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E1").quantity == "Not Required"
    assert _by_code(items, "E7").quantity == "Not Required"
    assert _by_code(items, "E8.3").quantity == "Not Required"
    assert _by_code(items, "E9").quantity is None
    assert _by_code(items, "E10").quantity == "Not Required"
    assert _by_code(items, "E11").quantity == "Not Required"
    assert _by_code(items, "E13").quantity == "Not Required"
    assert _by_code(items, "E14").quantity == "Not Required"
    assert _by_code(items, "E15").quantity == "Not Required"
    assert _by_code(items, "E17").quantity == "Not Required"


def test_item_codes_are_unique_within_section_e():
    codes = _codes(compute_section_e(build_section_e_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section E: {codes}"


def test_section_e_item_count_is_stable():
    assert len(compute_section_e(_empty_project())) == len(
        compute_section_e(build_section_e_site())
    )
