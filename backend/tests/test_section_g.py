"""Tests for the Section G calculation engine.

Section G has no computed quantities: every Calculator cell in column D is the
static text "Not Required". The tests therefore pin the item list itself
(codes, units, sub-headings) and confirm the output does not vary with the
project. Row-for-row agreement with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

from groundbill.engine import BoqItem, compute_section_g
from groundbill.models import ContractRoute, Project
from tests.fixtures.basic_site import build_basic_site


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


def test_codes_are_g1_through_g10_in_order():
    codes = [i.code for i in compute_section_g(_empty_project())]
    assert codes == [f"G{i}" for i in range(1, 11)]


def test_all_items_are_not_required():
    for item in compute_section_g(_empty_project()):
        assert item.quantity == "Not Required", f"{item.code} should be 'Not Required'"


def test_units_match_workbook():
    units = {i.code: i.unit for i in compute_section_g(_empty_project())}
    assert units == {
        "G1": "m²",
        "G2": "ln m",
        "G3": "ln m",
        "G4": "ln m",
        "G5": "ln m",
        "G6": "sum",
        "G7": "m",
        "G8": "nr",
        "G9": "sum",
        "G10": "day",
    }


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {
        i.code: i.subheading for i in compute_section_g(_empty_project()) if i.subheading
    }
    assert subheadings == {
        "G1": "Land-based mapping techniques",
        "G6": "Borehole geophysical surveying",
        "G9": "Marine (overwater) geophysical surveying",
    }


def test_g1_is_gpr_to_pas_128():
    g1 = _by_code(compute_section_g(_empty_project()), "G1")
    assert g1.description == (
        "Conduct and process Ground Penetrating Radar (GPR) profiles to "
        "PAS 128 QL B1P as per the specification"
    )


def test_section_g_does_not_depend_on_project_contents():
    assert compute_section_g(build_basic_site()) == compute_section_g(_empty_project())
