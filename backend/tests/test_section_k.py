"""Tests for the Section K calculation engine.

Expected quantities come from ``tests/fixtures/section_k_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions, units and sub-headings with the reference workbook is
checked in ``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_e, compute_section_k
from groundbill.models import ContractRoute, LabSchedule, LabTestAllocation, Project
from tests.fixtures.section_k_site import (
    EXPECTED_K_BLANK,
    EXPECTED_K_COMPUTED,
    build_section_k_site,
)


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


def test_fixture_computed_quantities_match_hand_derived_values():
    items = compute_section_k(build_section_k_site())
    for code, expected in EXPECTED_K_COMPUTED.items():
        assert _by_code(items, code).quantity == pytest.approx(expected), code


def test_k1_1_equals_section_e_tub_sample_count():
    # 'Section K'!D11: ='Section E'!D12
    project = build_section_k_site()
    e2 = _by_code(compute_section_e(project), "E2").quantity
    assert _by_code(compute_section_k(project), "K1.1").quantity == e2


def test_k1_2_is_half_of_k1_1():
    # Open item: formula is =0.5*(D11) although the Calculator's note says 25%.
    items = compute_section_k(build_section_k_site())
    assert _by_code(items, "K1.2").quantity == pytest.approx(0.5 * _by_code(items, "K1.1").quantity)


def test_k1_9_and_k1_12_are_a_quarter_of_k1_1():
    items = compute_section_k(build_section_k_site())
    k1_1 = _by_code(items, "K1.1").quantity
    assert _by_code(items, "K1.9").quantity == pytest.approx(0.25 * k1_1)
    assert _by_code(items, "K1.12").quantity == pytest.approx(0.25 * k1_1)


def test_k1_9_is_wet_sieving_and_k1_12_is_hydrometer():
    items = compute_section_k(_empty_project())
    assert _by_code(items, "K1.9").description == "Particle size distribution by wet sieving"
    assert _by_code(items, "K1.12").description == "Sedimentation by hydrometer"


def test_empty_project_produces_zero_quantities():
    items = compute_section_k(_empty_project())
    for code in EXPECTED_K_COMPUTED:
        assert _by_code(items, code).quantity == 0, code


def test_blank_calculator_cells_are_none():
    items = compute_section_k(build_section_k_site())
    assert len(EXPECTED_K_BLANK) == 29
    for code in EXPECTED_K_BLANK:
        assert _by_code(items, code).quantity is None, code


def test_every_other_item_is_not_required():
    items = compute_section_k(build_section_k_site())
    accounted_for = set(EXPECTED_K_COMPUTED) | set(EXPECTED_K_BLANK)
    others = [i for i in items if i.code not in accounted_for]
    assert len(others) == 109 - 4 - 29
    for item in others:
        assert item.quantity == "Not Required", item.code


def test_lab_schedule_is_not_read():
    # Decision of 2026-10-01: blank Calculator cells stay blank; no formula links
    # Section K to the Log Tracker's 'Lab Schedules' sheet.
    base = build_section_k_site()
    with_schedule = base.model_copy(
        update={
            "lab_schedule": LabSchedule(
                allocations=[LabTestAllocation(test_name="Organic matter content", quantity=7)]
            )
        }
    )
    assert compute_section_k(with_schedule) == compute_section_k(base)


def test_section_k_has_109_items_with_unique_codes():
    codes = [i.code for i in compute_section_k(_empty_project())]
    assert len(codes) == 109
    assert len(set(codes)) == 109


def test_group_headings_carry_their_codes():
    headings = {
        i.code: (i.subheading_code, i.subheading)
        for i in compute_section_k(_empty_project())
        if i.subheading
    }
    assert headings == {
        "K1.1": ("K1", "Classification"),
        "K2.1": ("K2", "Chemical and electrochemical"),
        "K3.1": ("K3", "Compaction related"),
        "K4.1": ("K4", "Compressibility, permeability and durability"),
        "K6.1": ("K6", "Shear strength (total stress)"),
        "K7.1": ("K7", "Shear strength (effective stress)"),
        "K8.1": ("K8", "Rock testing"),
        "K9.1": (
            "K.9",
            "Special tests on rock core or trial pit samples to assess potential for "
            "pyrite induced expansion or swelling",
        ),
    }


def test_k5_is_an_item_not_a_heading():
    # Row 61 has a unit and a quantity in the workbook, unlike the other group headings.
    k5 = _by_code(compute_section_k(_empty_project()), "K5")
    assert k5.description == "Consolidation and permeability in hydraulic cells"
    assert k5.unit == "nr"
    assert k5.quantity == "Not Required"
