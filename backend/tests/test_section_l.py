"""Tests for the Section L calculation engine.

Expected quantities come from ``tests/fixtures/section_l_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions and units with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_l
from groundbill.models import ContractRoute, InSituTest, Project, TrialPit
from tests.fixtures.section_l_site import EXPECTED_L, build_section_l_site


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


def test_codes_are_l1_through_l6_in_order():
    codes = [i.code for i in compute_section_l(_empty_project())]
    assert codes == ["L.1", "L.2", "L.3", "L.4", "L.5", "L.6"]


def test_fixture_quantities_match_hand_derived_values():
    items = compute_section_l(build_section_l_site())
    actual = {i.code: i.quantity for i in items}
    assert actual == pytest.approx(EXPECTED_L)


def test_l1_is_environmental_sample_count_divided_by_five():
    # 'Section L'!D11: ='Section E'!D25/5 — 6 holes with "EV" → 6 / 5 = 1.2
    items = compute_section_l(build_section_l_site())
    assert _by_code(items, "L.1").quantity == pytest.approx(1.2)


def test_l5_follows_e16_which_equals_e12():
    # 'Section L'!D15: ='Section E'!D29/5, and 'Section E'!D29 is =D25
    items = compute_section_l(build_section_l_site())
    assert _by_code(items, "L.5").quantity == _by_code(items, "L.1").quantity


def test_result_is_not_rounded():
    # One hole with "EV" → 1 / 5 = 0.2; the workbook applies no ROUNDUP.
    project = _empty_project().model_copy(
        update={
            "trial_pits": [
                TrialPit(
                    trial_pit_number="TP01", schedule_depth_m=3.0, in_situ_tests={InSituTest.EV}
                )
            ]
        }
    )
    assert _by_code(compute_section_l(project), "L.1").quantity == pytest.approx(0.2)


def test_empty_project_produces_zero_quantities():
    items = compute_section_l(_empty_project())
    for code in ("L.1", "L.5"):
        assert _by_code(items, code).quantity == 0, code


def test_static_items_are_not_required():
    items = compute_section_l(build_section_l_site())
    for code in ("L.2", "L.3", "L.4", "L.6"):
        assert _by_code(items, code).quantity == "Not Required", code


def test_descriptions_are_tests_suite_e_to_j():
    descriptions = [i.description for i in compute_section_l(_empty_project())]
    assert descriptions == [f"Tests Suite {s}" for s in "EFGHIJ"]


def test_subheading_sits_on_first_item():
    items = compute_section_l(_empty_project())
    assert items[0].subheading == (
        "Contamination testing of soil, groundwater, gas and fill material)"
    )
    assert all(i.subheading is None for i in items[1:])
