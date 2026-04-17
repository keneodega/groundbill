"""Tests for the Section F calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_f
from groundbill.models import ContractRoute, Project
from tests.fixtures.section_f_site import build_section_f_site


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


# --- Dynamic probe tests ---


def test_f1_completed_dp_count():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F1").quantity == 2


def test_f2_slope_dp_count():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F2").quantity == 1


def test_f3_dph_band_0_5():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F3").quantity == pytest.approx(9.0)


def test_f4_dph_band_5_10():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F4").quantity == pytest.approx(5.0)


def test_f5_dph_band_10_15():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F5").quantity == pytest.approx(2.0)


def test_f6_standing_time():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F6").quantity == 2


# --- CPT tests ---


def test_f8_standard_cpt_count():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F8").quantity == 2


def test_f9_piezocone_cpt_count():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F9").quantity == 1


def test_f10_slope_cpt_count():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F10").quantity == 1


def test_f11_cpt_band_0_10():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F11").quantity == pytest.approx(28.0)


def test_f12_cpt_band_10_20():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F12").quantity == pytest.approx(15.0)


def test_f13_cpt_band_20_30():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F13").quantity == pytest.approx(2.0)


def test_f14_cpt_band_30_40():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F14").quantity == pytest.approx(0.0)


def test_f15_cpt_standing_time():
    items = compute_section_f(build_section_f_site())
    assert _by_code(items, "F15").quantity == 3


# --- Structural tests ---


def test_empty_project_produces_zero_quantities():
    items = compute_section_f(_empty_project())
    for code in (
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "F13",
        "F14",
        "F15",
    ):
        assert _by_code(items, code).quantity == 0, code


def test_static_items():
    items = compute_section_f(build_section_f_site())
    for code in ("F7", "F16", "F17", "F18", "F19", "F20", "F21", "F22"):
        assert _by_code(items, code).quantity == "Not Required", code


def test_item_codes_are_unique_within_section_f():
    codes = _codes(compute_section_f(build_section_f_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section F: {codes}"


def test_section_f_item_count_is_stable():
    assert len(compute_section_f(_empty_project())) == len(
        compute_section_f(build_section_f_site())
    )
