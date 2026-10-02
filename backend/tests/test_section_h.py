"""Tests for the Section H calculation engine.

Expected quantities come from ``tests/fixtures/section_h_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions and units with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_h
from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    InSituTest,
    InspectionPit,
    Project,
    Soakaway,
    Trench,
    TrialPit,
)
from tests.fixtures.section_h_site import EXPECTED_H_COMPUTED, build_section_h_site


def _by_code(items: list[BoqItem], code: str) -> BoqItem:
    matches = [i for i in items if i.code == code]
    assert len(matches) == 1, f"Expected exactly one item with code {code}, got {len(matches)}"
    return matches[0]


def _project(**holes) -> Project:
    return Project(
        name="Test", site_address="Nowhere", contract_route=ContractRoute.PRIVATE, **holes
    )


def _qty(project: Project, code: str):
    return _by_code(compute_section_h(project), code).quantity


def _borehole(*phases: tuple[DrillingMethod, float]) -> Borehole:
    return Borehole(
        hole_number="BH01",
        phases=[DrillingPhase(method=m, depth_m=d) for m, d in phases],
        total_schedule_depth_m=sum(d for _, d in phases),
    )


def test_fixture_computed_quantities_match_hand_derived_values():
    items = compute_section_h(build_section_h_site())
    for code, expected in EXPECTED_H_COMPUTED.items():
        assert _by_code(items, code).quantity == pytest.approx(expected), code


def test_every_other_item_is_not_required():
    items = compute_section_h(build_section_h_site())
    others = [i for i in items if i.code not in EXPECTED_H_COMPUTED]
    assert len(others) == 51 - len(EXPECTED_H_COMPUTED)
    for item in others:
        assert item.quantity == "Not Required", item.code


def test_empty_project():
    items = compute_section_h(_project())
    for code in EXPECTED_H_COMPUTED:
        # 'Section H'!D60: =IF(D56>0,1,"Not Required") — no plate tests, no report.
        expected = "Not Required" if code == "H34" else 0
        assert _by_code(items, code).quantity == expected, code


# --- Standard penetration tests ---


def test_h1_is_cp_metres_per_band_and_is_not_rounded():
    # 'Section H'!D10: =Boreholes!$N92 — no ROUNDUP in the workbook.
    project = _project(boreholes=[_borehole((DrillingMethod.CABLE_PERCUSSION, 12.5))])
    assert _qty(project, "H1.1") == pytest.approx(10.0)
    assert _qty(project, "H1.2") == pytest.approx(2.5)


def test_h1_4_and_h2_4_are_not_required_even_below_30m():
    project = _project(
        boreholes=[
            _borehole((DrillingMethod.CABLE_PERCUSSION, 35.0)),
            _borehole((DrillingMethod.ROTARY_CORE_SOFT, 35.0)),
        ]
    )
    assert _qty(project, "H1.4") == "Not Required"
    assert _qty(project, "H2.4") == "Not Required"


@pytest.mark.parametrize(
    ("soft_metres", "expected"),
    [
        (1.0, 1),  # 0.67 rounds up to 1
        (1.5, 1),
        (3.0, 2),
        (4.0, 3),  # 2.67 rounds up to 3
        (4.5, 3),  # exact multiple: 3.0 must stay 3
        (9.0, 6),
    ],
)
def test_h2_1_is_soft_rotary_metres_over_1_5_rounded_up(soft_metres: float, expected: int):
    project = _project(boreholes=[_borehole((DrillingMethod.ROTARY_NO_CORE_SOFT, soft_metres))])
    assert _qty(project, "H2.1") == expected


def test_h2_adds_cored_and_uncored_soft_metres_before_rounding():
    # (AQ92 + BA92) / 1.5 = (2 + 2) / 1.5 = 2.67 → 3; rounding each separately would give 4.
    project = _project(
        boreholes=[
            _borehole((DrillingMethod.ROTARY_CORE_SOFT, 2.0)),
            _borehole((DrillingMethod.ROTARY_NO_CORE_SOFT, 2.0)),
        ]
    )
    assert _qty(project, "H2.1") == 3


def test_h2_ignores_rotary_drilling_in_hard_strata():
    project = _project(
        boreholes=[
            _borehole((DrillingMethod.ROTARY_CORE_HARD, 9.0)),
            _borehole((DrillingMethod.ROTARY_NO_CORE_HARD, 9.0)),
        ]
    )
    assert _qty(project, "H2.1") == 0


def test_h3_1_is_total_dynamic_sampling_depth():
    # Open item: metres billed as a number of SPTs, not rounded.
    samples = [DynamicSample(sample_number="DS01", depth_m=4.5)]
    assert _qty(_project(dynamic_samples=samples), "H3.1") == pytest.approx(4.5)


# --- Tests in pits and trenches ---


def _one_of_each(test: InSituTest) -> Project:
    """One trial pit, inspection pit, trench and soakaway, each with *test* selected."""
    return _project(
        trial_pits=[TrialPit(trial_pit_number="TP01", schedule_depth_m=3.0, in_situ_tests={test})],
        inspection_pits=[
            InspectionPit(inspection_pit_number="IP01", scheduled_depth_m=1.2, in_situ_tests={test})
        ],
        trenches=[Trench(trench_number="TR01", in_situ_tests={test})],
        soakaways=[Soakaway(soakaway_id="SK01", schedule_depth_m=2.0, in_situ_tests={test})],
    )


def test_h6_dcp_counts_pits_inspection_pits_and_trenches_but_not_soakaways():
    assert _qty(_one_of_each(InSituTest.DCP), "H6") == 3


def test_h9_hand_vane_multiplies_only_the_trial_pit_term_by_four():
    # Open item, translated literally: trial pit × 4 + inspection pit + trench = 6.
    assert _qty(_one_of_each(InSituTest.HV), "H9") == 6


def test_h19_bre_also_counts_the_soakaway_sheet():
    assert _qty(_one_of_each(InSituTest.BRE), "H19") == 4


def test_h23_h25_h26_follow_h19():
    items = compute_section_h(_one_of_each(InSituTest.BRE))
    for code in ("H23", "H25", "H26"):
        assert _by_code(items, code).quantity == 4, code


def test_h30_plate_test_does_not_count_soakaways():
    assert _qty(_one_of_each(InSituTest.PT), "H30") == 3


def test_h34_is_one_report_when_any_plate_test_is_scheduled():
    assert _qty(_one_of_each(InSituTest.PT), "H34") == 1
    assert _qty(_one_of_each(InSituTest.DCP), "H34") == "Not Required"


# --- Structure ---


def test_section_h_has_51_items_with_unique_codes():
    codes = [i.code for i in compute_section_h(_project())]
    assert len(codes) == 51
    assert len(set(codes)) == 51


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {i.code: i.subheading for i in compute_section_h(_project()) if i.subheading}
    # H1.1-H9 sit directly under the section title, so H1.1 carries no sub-heading.
    assert subheadings == {
        "H10": "Other tests",
        "H11": "Permeability testing",
        "H19": "Soil infiltration test (BRE Digest 365)",
        "H27": "Soil infiltration test (EPA Percolation test)",
        "H30": "Plate Bearing Test",
        "H35": "Other specialist tests",
    }


def test_footnote_is_carried_on_h18():
    items = compute_section_h(_project())
    notes = {i.code: i.note for i in items if i.note}
    assert notes == {
        "H18": (
            "Note: rates for permeability test in boreholes or rotary holes to include standing time rate for plant and equipment"
        )
    }
