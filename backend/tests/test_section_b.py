"""Tests for the Section B calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_b
from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    Project,
)
from tests.fixtures.section_b_site import build_section_b_site


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


def test_b1_counts_split_cp_vs_cp_rc_and_barrier_flag():
    items = compute_section_b(build_section_b_site())
    assert _by_code(items, "B1.1.1").quantity == 3
    assert _by_code(items, "B1.1.2").quantity == 1
    assert _by_code(items, "B1.2.1").quantity == 1
    assert _by_code(items, "B1.2.2").quantity == 1


def test_b2_counts_slope_boreholes_by_drilling_type():
    items = compute_section_b(build_section_b_site())
    # CP-only on slope: one borehole (BH04). CP/RC on slope: two (BH05, BH06).
    assert _by_code(items, "B2.1").quantity == 1
    assert _by_code(items, "B2.2").quantity == 2


def test_b3_equals_total_borehole_count():
    items = compute_section_b(build_section_b_site())
    total = sum(_by_code(items, code).quantity for code in ("B1.1.1", "B1.1.2", "B1.2.1", "B1.2.2"))
    assert _by_code(items, "B3").quantity == total == 6


def test_b4_b7_distribute_cp_metreage_across_10m_bands():
    items = compute_section_b(build_section_b_site())
    # See fixture docstring for the hand-computed expected values.
    assert _by_code(items, "B4").quantity == 54
    assert _by_code(items, "B5").quantity == 19
    assert _by_code(items, "B6").quantity == 10
    assert _by_code(items, "B7").quantity == 5


def test_b8_is_static_not_required():
    items = compute_section_b(build_section_b_site())
    assert _by_code(items, "B8").quantity == "Not Required"


def test_b9_is_total_bh_times_two_hours():
    items = compute_section_b(build_section_b_site())
    assert _by_code(items, "B9").quantity == 12  # 6 BHs * 2 h
    assert _by_code(items, "B9").unit == "h"


def test_b12_equals_total_borehole_count_in_hours():
    items = compute_section_b(build_section_b_site())
    assert _by_code(items, "B12").quantity == 6
    assert _by_code(items, "B12").unit == "h"


def test_dynamic_sampling_counts_and_bands():
    items = compute_section_b(build_section_b_site())
    assert _by_code(items, "B13").quantity == 3
    assert _by_code(items, "B14").quantity == 1  # one DS flagged slope > 20%
    assert _by_code(items, "B15").quantity == 3
    assert _by_code(items, "B16").quantity == 3
    assert _by_code(items, "B17").quantity == 13  # 3 + 5 + 5
    assert _by_code(items, "B18").quantity == 8  # 0 + 3 + 5
    assert _by_code(items, "B19").quantity == 4  # 0 + 0 + 4
    assert _by_code(items, "B20").quantity == pytest.approx(1.5)  # 3 * 0.5 h


def test_pure_rotary_borehole_is_excluded_from_section_b():
    project = Project(
        name="Rotary only",
        site_address="X",
        contract_route=ContractRoute.PRIVATE,
        boreholes=[
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=20.0)],
                total_schedule_depth_m=20.0,
            ),
        ],
    )
    items = compute_section_b(project)
    for code in ("B1.1.1", "B1.1.2", "B1.2.1", "B1.2.2", "B3", "B4", "B5", "B6", "B7", "B9", "B12"):
        assert _by_code(items, code).quantity == 0


def test_b3_1_counts_boreholes_on_a_road():
    # COUNTIF(Boreholes!BH, "YES") * 0.125 — column BH 'ROAD' is a yes/no flag.
    project = Project(
        name="Road flag",
        site_address="X",
        contract_route=ContractRoute.PRIVATE,
        boreholes=[
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=5.0)],
                total_schedule_depth_m=5.0,
                on_road=True,
            ),
            Borehole(
                hole_number="BH02",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=5.0)],
                total_schedule_depth_m=5.0,
                on_road=False,
            ),
        ],
    )
    items = compute_section_b(project)
    assert _by_code(items, "B3.1").quantity == pytest.approx(0.125)


def test_ds_depths_clip_at_band_edges():
    # A 5.0 m sample sits exactly on the boundary: all in 0-5, none in 5-10.
    project = Project(
        name="DS edge",
        site_address="X",
        contract_route=ContractRoute.PRIVATE,
        dynamic_samples=[DynamicSample(sample_number="DS01", depth_m=5.0)],
    )
    items = compute_section_b(project)
    assert _by_code(items, "B17").quantity == 5
    assert _by_code(items, "B18").quantity == 0
    assert _by_code(items, "B19").quantity == 0


def test_empty_project_produces_zero_quantities():
    items = compute_section_b(_empty_project())
    for code in (
        "B1.1.1",
        "B1.1.2",
        "B1.2.1",
        "B1.2.2",
        "B2.1",
        "B2.2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B9",
        "B12",
        "B13",
        "B14",
        "B15",
        "B16",
        "B17",
        "B18",
        "B19",
    ):
        assert _by_code(items, code).quantity == 0, code
    assert _by_code(items, "B20").quantity == 0


def test_placeholder_items_are_carried_through_verbatim():
    items = compute_section_b(build_section_b_site())
    assert _by_code(items, "B10").quantity == "Included in B1 to B1.2.2"
    assert _by_code(items, "B11").quantity == "Included in B1 to B1.2.2"
    assert _by_code(items, "B21").quantity == "Included in B13"
    assert _by_code(items, "B22").quantity == "Included in B1.1 & B1.2"
    assert _by_code(items, "B23").quantity == "Included in D53"
    assert _by_code(items, "B24").quantity == "Included in B1.1, B1.2 & B13"
    assert _by_code(items, "B25").quantity == "Not Required"
    assert _by_code(items, "B26").quantity == "Included in B1 to B1.2.2"


def test_item_codes_are_unique_within_section_b():
    codes = _codes(compute_section_b(build_section_b_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section B: {codes}"


def test_section_b_item_count_is_stable():
    # Section B has a fixed inventory (no site-category-dependent extras).
    assert len(compute_section_b(_empty_project())) == len(
        compute_section_b(build_section_b_site())
    )
