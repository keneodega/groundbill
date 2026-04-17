"""Tests for the Section I calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_i
from groundbill.models import ContractRoute, Project
from tests.fixtures.section_i_site import build_section_i_site


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


# --- Borehole instrumentation tests ---


def test_i1_piezometer_count():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I1").quantity == 1


def test_i2_standpipe_count():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I2").quantity == 2


def test_i3_piezometer_plain_depth():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I3").quantity == pytest.approx(10.0)


def test_i4_standpipe_plain_depth():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I4").quantity == pytest.approx(13.0)


def test_i5_standpipe_slotted_depth():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I5").quantity == pytest.approx(5.0)


def test_i6_standpipe_50mm_count():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I6").quantity == 1


def test_i7_standpipe_19mm_count():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I7").quantity == 1


def test_i8_end_caps():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I8").quantity == 3  # I1 + I2


def test_i9_flush_cover_rural():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I9").quantity == 1  # BH02


def test_i10_raised_cover_non_road():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I10").quantity == 2  # BH01 + BH03


# --- Dynamic sample instrumentation tests ---


def test_i11_ds_standpipe_count():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I11").quantity == 2


def test_i12_ds_plain_depth():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I12").quantity == pytest.approx(7.0)


def test_i13_ds_slotted_depth():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I13").quantity == pytest.approx(3.0)


def test_i14_ds_50mm_count():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I14").quantity == 1


def test_i15_ds_19mm_count():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I15").quantity == 1


def test_i16_ds_end_caps():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I16").quantity == 2  # = I11


def test_i17_ds_flush_cover_rural():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I17").quantity == 1


def test_i18_ds_raised_cover_non_road():
    items = compute_section_i(build_section_i_site())
    assert _by_code(items, "I18").quantity == 1


# --- Structural tests ---


def test_empty_project_produces_zero_quantities():
    items = compute_section_i(_empty_project())
    for code in (
        "I1",
        "I2",
        "I3",
        "I4",
        "I5",
        "I6",
        "I7",
        "I8",
        "I9",
        "I10",
        "I11",
        "I12",
        "I13",
        "I14",
        "I15",
        "I16",
        "I17",
        "I18",
    ):
        assert _by_code(items, code).quantity == 0, code


def test_static_items():
    items = compute_section_i(build_section_i_site())
    for code in (
        "I19",
        "I20",
        "I21",
        "I22",
        "I23",
        "I24",
        "I25",
        "I26",
        "I27",
        "I28",
        "I29",
        "I30",
        "I31",
        "I32",
        "I33",
        "I34",
        "I35",
    ):
        assert _by_code(items, code).quantity == "Not Required", code


def test_item_codes_are_unique_within_section_i():
    codes = _codes(compute_section_i(build_section_i_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section I: {codes}"


def test_section_i_item_count_is_stable():
    assert len(compute_section_i(_empty_project())) == len(
        compute_section_i(build_section_i_site())
    )
