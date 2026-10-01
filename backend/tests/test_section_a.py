"""Tests for the Section A calculation engine."""

from groundbill.engine import BoqItem, compute_section_a
from groundbill.models import ContractRoute, Project, SiteCategory
from tests.fixtures.basic_site import build_basic_site


def _codes(items: list[BoqItem]) -> list[str]:
    return [i.code for i in items]


def _by_code(items: list[BoqItem], code: str) -> BoqItem:
    matches = [i for i in items if i.code == code]
    assert len(matches) == 1, f"Expected exactly one item with code {code}, got {len(matches)}"
    return matches[0]


def test_a8_counts_all_hole_types_with_trenches_double_counted():
    project = build_basic_site()
    items = compute_section_a(project)

    a8 = _by_code(items, "A8")
    assert a8.quantity == 9  # 3 BH + 2 TP + (1 trench * 2) + 1 CPT + 1 DS
    assert a8.unit == "Nr"


def test_a8_1_mirrors_a8():
    project = build_basic_site()
    items = compute_section_a(project)
    assert _by_code(items, "A8").quantity == _by_code(items, "A8.1").quantity


def test_a8_is_zero_for_empty_project():
    project = Project(
        name="Empty",
        site_address="Nowhere",
        contract_route=ContractRoute.PRIVATE,
    )
    items = compute_section_a(project)
    assert _by_code(items, "A8").quantity == 0
    assert _by_code(items, "A8.1").quantity == 0


def test_all_61_items_are_listed_for_every_site_category():
    # Decision of 2026-10-01: Section A does not vary with the site category.
    codes_a3_to_a5 = {"A3.1", "A3.2", "A4.1", "A4.2", "A5.1", "A5.2"}
    green = compute_section_a(build_basic_site())
    assert len(green) == 61
    assert codes_a3_to_a5 <= set(_codes(green))
    for category in (SiteCategory.YELLOW, SiteCategory.RED):
        project = build_basic_site().model_copy(update={"site_category": category})
        assert compute_section_a(project) == green, category


def test_a2_items_always_describe_a_green_category_site():
    items = compute_section_a(
        build_basic_site().model_copy(update={"site_category": SiteCategory.RED})
    )
    for code in ["A2"] + [f"A2.{n}" for n in range(1, 10)]:
        assert "for a Green Category site" in _by_code(items, code).description, code


def test_a3_to_a5_extra_overs_are_not_required():
    items = compute_section_a(build_basic_site())
    for code in ("A3.1", "A3.2", "A4.1", "A4.2", "A5.1", "A5.2"):
        item = _by_code(items, code)
        assert item.quantity == "Not Required", code
        assert item.unit == "provisional sum", code


def test_manual_entry_placeholders_are_carried_through():
    project = build_basic_site()
    items = compute_section_a(project)
    assert _by_code(items, "A1").quantity == "Not Required"
    assert _by_code(items, "A7.1").quantity == "Included in A7"
    assert _by_code(items, "A27").quantity == "included in A2"
    assert _by_code(items, "A26").quantity is None


def test_item_codes_are_unique_within_section_a():
    items = compute_section_a(build_basic_site())
    codes = _codes(items)
    assert len(codes) == len(set(codes)), f"duplicate codes in Section A: {codes}"


def test_texts_and_units_follow_the_contractor_workbook():
    items = {i.code: i for i in compute_section_a(build_basic_site())}
    assert items["A16"].unit == "provisional sum"
    assert items["A15"].description.endswith("on roads or pavement areas")
    assert items["A6"].description.endswith(
        "Note item to be remeasured with delivery dockets and records maintained by the "
        "Contractor."
    )
    assert "(PROVISIONAL)" not in items["A2.3"].description
