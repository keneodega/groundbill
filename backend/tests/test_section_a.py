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


def test_green_site_omits_yellow_and_red_only_items():
    project = build_basic_site()  # GREEN
    codes = set(_codes(compute_section_a(project)))
    for omitted in ("A3.1", "A3.2", "A4.1", "A4.2", "A5.1", "A5.2"):
        assert omitted not in codes


def test_yellow_site_emits_yellow_extras_and_not_red():
    project = build_basic_site()
    project = project.model_copy(update={"site_category": SiteCategory.YELLOW})
    codes = set(_codes(compute_section_a(project)))
    assert {"A3.1", "A4.1", "A5.1"}.issubset(codes)
    assert not {"A3.2", "A4.2", "A5.2"} & codes


def test_red_site_emits_red_extras_and_not_yellow():
    project = build_basic_site()
    project = project.model_copy(update={"site_category": SiteCategory.RED})
    codes = set(_codes(compute_section_a(project)))
    assert {"A3.2", "A4.2", "A5.2"}.issubset(codes)
    assert not {"A3.1", "A4.1", "A5.1"} & codes


def test_a2_description_reflects_site_category():
    for category, expected in [
        (SiteCategory.GREEN, "Green Category site"),
        (SiteCategory.YELLOW, "Yellow Category site"),
        (SiteCategory.RED, "Red Category site"),
    ]:
        project = Project(
            name="X",
            site_address="Y",
            contract_route=ContractRoute.PRIVATE,
            site_category=category,
        )
        a2 = _by_code(compute_section_a(project), "A2")
        assert expected in a2.description


def test_manual_entry_placeholders_are_carried_through():
    project = build_basic_site()
    items = compute_section_a(project)
    assert _by_code(items, "A1").quantity == "Not Required"
    assert _by_code(items, "A7.1").quantity == "Included in A7"
    assert _by_code(items, "A27").quantity == "included in A2"
    assert _by_code(items, "A26").quantity is None


def test_section_a_emits_expected_item_count_per_category():
    project = build_basic_site()
    green_count = len(compute_section_a(project))

    yellow_project = project.model_copy(update={"site_category": SiteCategory.YELLOW})
    yellow_count = len(compute_section_a(yellow_project))

    red_project = project.model_copy(update={"site_category": SiteCategory.RED})
    red_count = len(compute_section_a(red_project))

    assert yellow_count == green_count + 3
    assert red_count == green_count + 3


def test_item_codes_are_unique_within_section_a():
    items = compute_section_a(build_basic_site())
    codes = _codes(items)
    assert len(codes) == len(set(codes)), f"duplicate codes in Section A: {codes}"
