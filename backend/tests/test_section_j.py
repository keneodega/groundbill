"""Tests for the Section J calculation engine.

Section J has no computed quantities: every Calculator cell in column D is the
static text "Not Required". The tests therefore pin the item list itself
(codes, units, sub-headings) and confirm the output does not vary with the
project. Row-for-row agreement with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

from groundbill.engine import BoqItem, compute_section_j
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


def test_codes_are_j1_through_j25_in_order():
    codes = [i.code for i in compute_section_j(_empty_project())]
    assert codes == [f"J{i}" for i in range(1, 26)]


def test_all_items_are_not_required():
    for item in compute_section_j(_empty_project()):
        assert item.quantity == "Not Required", f"{item.code} should be 'Not Required'"


def test_units_match_workbook():
    units = {i.code: i.unit for i in compute_section_j(_empty_project())}
    # Everything is "nr" except the purging extra-overs (hours), the free
    # product equipment (lump sum) and the data logger visit (day).
    other_units = {"J6": "h", "J15": "h", "J18": "sum", "J21": "day"}
    assert units == {f"J{i}": other_units.get(f"J{i}", "nr") for i in range(1, 26)}


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {
        i.code: i.subheading for i in compute_section_j(_empty_project()) if i.subheading
    }
    # J1-J8 sit directly under the section title, so J1 carries no sub-heading.
    assert subheadings == {
        "J9": "Installation monitoring and sampling (post Fieldwork Period)",
        "J22": "Surface water body sampling and testing",
    }


def test_j1_is_water_level_reading_during_fieldwork():
    j1 = _by_code(compute_section_j(_empty_project()), "J1")
    assert j1.description == (
        "Reading of water level in standpipe or standpipe piezometer during fieldwork period"
    )


def test_j9_is_return_visit_after_fieldwork():
    j9 = _by_code(compute_section_j(_empty_project()), "J9")
    assert j9.description == (
        "Return visit to site following completion of fieldwork for field instrumentation"
    )


def test_section_j_does_not_depend_on_project_contents():
    assert compute_section_j(build_basic_site()) == compute_section_j(_empty_project())
