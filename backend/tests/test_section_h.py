"""Tests for the Section H calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_h
from groundbill.models import ContractRoute, Project
from tests.fixtures.section_h_site import build_section_h_site


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


# --- CP SPT tests (H1.x) ---


def test_h1_1_cp_spt_band_0_10():
    items = compute_section_h(build_section_h_site())
    # CP bands: BH01=[10,2,0,0], BH02=[8,0,0,0], BH03=[6,0,0,0] → total [24,2,0,0]
    assert _by_code(items, "H1.1").quantity == 24


def test_h1_2_cp_spt_band_10_20():
    items = compute_section_h(build_section_h_site())
    assert _by_code(items, "H1.2").quantity == 2


def test_h1_3_cp_spt_band_20_30():
    items = compute_section_h(build_section_h_site())
    assert _by_code(items, "H1.3").quantity == 0


def test_h1_4_cp_spt_band_30_40():
    items = compute_section_h(build_section_h_site())
    assert _by_code(items, "H1.4").quantity == 0


# --- Rotary SPT tests (H2.x) ---


def test_h2_1_rotary_spt_band_0_10():
    items = compute_section_h(build_section_h_site())
    # Soft rotary: BH02 offset=8,end=13 → [2,3,0,0]; BH03 offset=6,end=15 → [4,5,0,0]
    # Total soft: [6, 8, 0, 0]. H2.1 = ceil(6/1.5) = 4
    assert _by_code(items, "H2.1").quantity == 4


def test_h2_2_rotary_spt_band_10_20():
    items = compute_section_h(build_section_h_site())
    # H2.2 = ceil(8/1.5) = ceil(5.33) = 6
    assert _by_code(items, "H2.2").quantity == 6


def test_h2_3_rotary_spt_band_20_30():
    items = compute_section_h(build_section_h_site())
    assert _by_code(items, "H2.3").quantity == 0


def test_h2_4_rotary_spt_band_30_40():
    items = compute_section_h(build_section_h_site())
    assert _by_code(items, "H2.4").quantity == 0


# --- Other computed items ---


def test_h3_1_ds_depth_sum():
    items = compute_section_h(build_section_h_site())
    assert _by_code(items, "H3.1").quantity == pytest.approx(10.0)


def test_h6_dcp_count():
    items = compute_section_h(build_section_h_site())
    # TP01 + IP01 + SK01 = 3
    assert _by_code(items, "H6").quantity == 3


def test_h9_hand_vane_count():
    items = compute_section_h(build_section_h_site())
    # (TP01 + TR01) × 4 = 8
    assert _by_code(items, "H9").quantity == 8


def test_h19_bre_test_count():
    items = compute_section_h(build_section_h_site())
    # TP02 + SK01 = 2
    assert _by_code(items, "H19").quantity == 2


def test_h30_permeability_test_count():
    items = compute_section_h(build_section_h_site())
    # SK01 = 1
    assert _by_code(items, "H30").quantity == 1


def test_h34_report_with_holes():
    items = compute_section_h(build_section_h_site())
    assert _by_code(items, "H34").quantity == 1


def test_h34_report_empty_project():
    items = compute_section_h(_empty_project())
    assert _by_code(items, "H34").quantity == 0


# --- Structural tests ---


def test_empty_project_produces_zero_quantities():
    items = compute_section_h(_empty_project())
    for code in (
        "H1.1",
        "H1.2",
        "H1.3",
        "H1.4",
        "H2.1",
        "H2.2",
        "H2.3",
        "H2.4",
        "H3.1",
        "H6",
        "H9",
        "H19",
        "H30",
        "H34",
    ):
        assert _by_code(items, code).quantity == 0, code


def test_static_items():
    items = compute_section_h(build_section_h_site())
    for code in (
        "H4",
        "H5",
        "H7",
        "H8",
        "H10",
        "H11",
        "H12",
        "H13",
        "H14",
        "H15",
        "H16",
        "H17",
        "H18",
        "H20",
        "H21",
        "H22",
        "H23",
        "H24",
        "H25",
        "H26",
        "H27",
        "H28",
        "H29",
        "H31",
        "H32",
        "H33",
        "H35",
        "H36",
        "H37",
        "H38",
        "H39",
        "H40",
    ):
        assert _by_code(items, code).quantity == "Not Required", code


def test_item_codes_are_unique_within_section_h():
    codes = _codes(compute_section_h(build_section_h_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section H: {codes}"


def test_section_h_item_count_is_stable():
    assert len(compute_section_h(_empty_project())) == len(
        compute_section_h(build_section_h_site())
    )
