"""Tests for the Section E calculation engine.

Expected quantities come from ``tests/fixtures/section_e_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions and units with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_e
from groundbill.models import ContractRoute, InspectionPit, Project, Trench
from tests.fixtures.section_e_site import EXPECTED_E, build_section_e_site


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


def test_fixture_quantities_match_hand_derived_values():
    items = compute_section_e(build_section_e_site())
    actual = {i.code: i.quantity for i in items}
    assert list(actual) == list(EXPECTED_E)  # same codes, same order
    for code, expected in EXPECTED_E.items():
        if isinstance(expected, int | float):
            assert actual[code] == pytest.approx(expected), code
        else:
            assert actual[code] == expected, code


def test_e2_is_one_tub_sample_per_metre_of_hole():
    items = compute_section_e(build_section_e_site())
    # CP 20 + trial pits 5 + trenches 0 + inspection pits 1.5 + dynamic sampling 10
    assert _by_code(items, "E2").quantity == pytest.approx(36.5)


def test_e2_ignores_rotary_metres():
    # Boreholes!K92 sums the CP column only; BH02's 5 m of rotary coring is excluded.
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E5").quantity == pytest.approx(20 / 5)


def test_e2_trench_term_is_zero_whatever_the_trench_dimensions():
    # Open item: Trenches!N93 is an empty cell, translated literally as 0.
    base = build_section_e_site()
    more_trenches = base.model_copy(
        update={
            "trenches": [
                *base.trenches,
                Trench(
                    trench_number="TR02",
                    overall_length_m=10.0,
                    overall_width_m=1.0,
                    overall_total_depth_m=3.0,
                    non_paved_length_m=10.0,
                    non_paved_width_m=1.0,
                    non_paved_depth_m=3.0,
                ),
            ]
        }
    )
    assert (
        _by_code(compute_section_e(more_trenches), "E2").quantity
        == _by_code(compute_section_e(base), "E2").quantity
    )


def test_e2_sums_every_inspection_pit_not_only_rows_65_to_91():
    # Deliberate deviation from 'Inspection pit'!E92 (=SUM(E65:E91)): all pits count.
    pits = [
        InspectionPit(
            inspection_pit_number=f"IP{n:02d}", scheduled_depth_m=1.2, recorded_depth_m=1.2
        )
        for n in range(1, 71)
    ]
    project = _empty_project().model_copy(update={"inspection_pits": pits})
    assert _by_code(compute_section_e(project), "E2").quantity == pytest.approx(70 * 1.2)


def test_e3_equals_e2_and_e6_equals_e5():
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E3").quantity == _by_code(items, "E2").quantity
    assert _by_code(items, "E6").quantity == _by_code(items, "E5").quantity


def test_divisions_are_not_rounded():
    # 'Section E'!D14: =D12/10 — 36.5 / 10 = 3.65, no ROUNDUP in the workbook.
    items = compute_section_e(build_section_e_site())
    assert _by_code(items, "E4").quantity == pytest.approx(3.65)


def test_e12_counts_holes_with_ev_selected():
    items = compute_section_e(build_section_e_site())
    # TP01 + IP01 + TR01 + BH02 + DS01
    assert _by_code(items, "E12").quantity == 5
    assert _by_code(items, "E16").quantity == 5


def test_e9_groundwater_sample_quantity_is_blank():
    assert _by_code(compute_section_e(build_section_e_site()), "E9").quantity is None


def test_empty_project_produces_zero_quantities():
    items = compute_section_e(_empty_project())
    for code in ("E2", "E3", "E4", "E5", "E6", "E8.1", "E8.2", "E12", "E16"):
        assert _by_code(items, code).quantity == 0, code


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {
        i.code: i.subheading for i in compute_section_e(_empty_project()) if i.subheading
    }
    assert subheadings == {
        "E1": "Samples for geotechnical purposes",
        "E12": "Samples for environmental / contamination analysis",
    }


def test_all_units_are_nr():
    assert {i.unit for i in compute_section_e(_empty_project())} == {"nr"}


def test_footnote_is_carried_on_e17():
    items = compute_section_e(_empty_project())
    notes = {i.code: i.note for i in items if i.note}
    assert notes == {"E17": ("(Note sample rate includes provision of specialist containers)")}
