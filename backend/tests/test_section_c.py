"""Tests for the Section C calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_c
from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    Project,
)
from tests.fixtures.section_c_site import build_section_c_site


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


def test_c15_counts_split_cp_rc_vs_rc_and_barrier_flag():
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C15.1.1").quantity == 1  # BH01: CP/RC, no barrier
    assert _by_code(items, "C15.1.2").quantity == 1  # BH02: CP/RC, barrier
    assert _by_code(items, "C15.2.1").quantity == 1  # BH03: RC, no barrier
    assert _by_code(items, "C15.2.2").quantity == 1  # BH04: RC, barrier


def test_c15_3_counts_rc_only_boreholes_for_cat_scan():
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C15.3").quantity == 2  # BH03, BH04


def test_c16_counts_all_rotary_boreholes_on_slopes():
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C16").quantity == 2  # BH02, BH04


def test_c18_road_flag():
    # Same formula as B3.1: COUNTIF(road="YES") * 0.125
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C18").quantity == 0  # No boreholes with road="YES"


def test_c18_with_road_yes():
    project = Project(
        name="Road flag",
        site_address="X",
        contract_route=ContractRoute.PRIVATE,
        boreholes=[
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=10.0)],
                total_schedule_depth_m=10.0,
                road="YES",
            ),
        ],
    )
    items = compute_section_c(project)
    assert _by_code(items, "C18").quantity == pytest.approx(0.125)


def test_c19_standing_time_equals_total_rotary_bh_count():
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C19").quantity == 4


def test_c21_c24_soft_no_core_bands():
    """RC_NO_CORE_SOFT: BH02 has 12 m starting at offset 5 m → [5, 7, 0, 0]."""
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C21").quantity == 5
    assert _by_code(items, "C22").quantity == 7
    assert _by_code(items, "C23").quantity == 0
    assert _by_code(items, "C24").quantity == 0


def test_c27_c30_hard_no_core_bands():
    """RC_NO_CORE_HARD: BH04 has 25 m starting at offset 0 → [10, 10, 5, 0]."""
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C27").quantity == 10
    assert _by_code(items, "C28").quantity == 10
    assert _by_code(items, "C29").quantity == 5
    assert _by_code(items, "C30").quantity == 0


def test_c34_c37_soft_core_bands():
    """RC_CORE_SOFT: BH03 has 15 m starting at offset 0 → [10, 5, 0, 0]."""
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C34").quantity == 10
    assert _by_code(items, "C35").quantity == 5
    assert _by_code(items, "C36").quantity == 0
    assert _by_code(items, "C37").quantity == 0


def test_c41_c44_hard_core_bands():
    """RC_CORE_HARD: BH01 has 8 m starting at offset 10 → [0, 8, 0, 0]."""
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C41").quantity == 0
    assert _by_code(items, "C42").quantity == 8
    assert _by_code(items, "C43").quantity == 0
    assert _by_code(items, "C44").quantity == 0


def test_cp_only_borehole_excluded_from_section_c():
    project = Project(
        name="CP only",
        site_address="X",
        contract_route=ContractRoute.PRIVATE,
        boreholes=[
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=20.0)],
                total_schedule_depth_m=20.0,
            ),
        ],
    )
    items = compute_section_c(project)
    for code in ("C15.1.1", "C15.1.2", "C15.2.1", "C15.2.2", "C15.3", "C16", "C19"):
        assert _by_code(items, code).quantity == 0


def test_empty_project_produces_zero_quantities():
    items = compute_section_c(_empty_project())
    for code in (
        "C15.1.1",
        "C15.1.2",
        "C15.2.1",
        "C15.2.2",
        "C15.3",
        "C16",
        "C18",
        "C19",
        "C21",
        "C22",
        "C23",
        "C24",
        "C27",
        "C28",
        "C29",
        "C30",
        "C34",
        "C35",
        "C36",
        "C37",
        "C41",
        "C42",
        "C43",
        "C44",
    ):
        assert _by_code(items, code).quantity == 0, code


def test_static_items_are_not_required():
    items = compute_section_c(build_section_c_site())
    for code in (
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
        "C9",
        "C10",
        "C11",
        "C12",
        "C13",
        "C14",
        "C25",
        "C26",
        "C31",
        "C32",
        "C38",
        "C39",
        "C45",
        "C46",
        "C55",
        "C57",
        "C58",
        "C59",
        "C60",
        "C61",
        "C62",
        "C63",
        "C64",
        "C65",
        "C66",
        "C67",
        "C68",
        "C69",
        "C70",
        "C71",
        "C72",
        "C73",
        "C74",
        "C75",
        "C76",
        "C77",
        "C78",
        "C79",
        "C80",
        "C81",
        "C82",
        "C83",
        "C84",
        "C85",
    ):
        assert _by_code(items, code).quantity == "Not Required", code


def test_included_placeholders():
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C17").quantity == "Included in C15 to C15.2.2"
    assert _by_code(items, "C20").quantity == "Included in C15 to C15.2.2"
    assert _by_code(items, "C33").quantity == "Included in C21 to C32"
    assert _by_code(items, "C40").quantity == "Included in C34 to C39"
    assert _by_code(items, "C47").quantity == "Included in C41 to C46"
    assert _by_code(items, "C53").quantity == "Included in D53"


def test_item_codes_are_unique_within_section_c():
    codes = _codes(compute_section_c(build_section_c_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section C: {codes}"


def test_section_c_item_count_is_stable():
    assert len(compute_section_c(_empty_project())) == len(
        compute_section_c(build_section_c_site())
    )
