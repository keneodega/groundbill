"""Tests for the Section J calculation engine."""

from groundbill.engine import BoqItem, compute_section_j
from groundbill.models import ContractRoute, Project


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


def test_all_items_are_not_required():
    items = compute_section_j(_empty_project())
    for item in items:
        assert item.quantity == "Not Required", f"{item.code} should be 'Not Required'"


def test_section_j_has_25_items():
    items = compute_section_j(_empty_project())
    assert len(items) == 25


def test_item_codes_are_unique_within_section_j():
    codes = _codes(compute_section_j(_empty_project()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section J: {codes}"


def test_codes_are_j1_through_j25():
    codes = _codes(compute_section_j(_empty_project()))
    assert codes == [f"J{i}" for i in range(1, 26)]
