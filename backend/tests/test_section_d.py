"""Tests for the Section D calculation engine.

Expected quantities come from ``tests/fixtures/section_d_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions and units with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_d
from groundbill.models import ContractRoute, InspectionPit, Project, Trench, TrialPit
from tests.fixtures.section_d_site import (
    EXPECTED_D_COMPUTED,
    EXPECTED_D_TEXT,
    build_section_d_site,
)


def _by_code(items: list[BoqItem], code: str) -> BoqItem:
    matches = [i for i in items if i.code == code]
    assert len(matches) == 1, f"Expected exactly one item with code {code}, got {len(matches)}"
    return matches[0]


def _project(**holes) -> Project:
    return Project(
        name="Test", site_address="Nowhere", contract_route=ContractRoute.PRIVATE, **holes
    )


def _qty(project: Project, code: str):
    return _by_code(compute_section_d(project), code).quantity


def test_fixture_computed_quantities_match_hand_derived_values():
    items = compute_section_d(build_section_d_site())
    for code, expected in EXPECTED_D_COMPUTED.items():
        assert _by_code(items, code).quantity == pytest.approx(expected), code


def test_fixture_text_placeholders_match_calculator():
    items = compute_section_d(build_section_d_site())
    for code, expected in EXPECTED_D_TEXT.items():
        assert _by_code(items, code).quantity == expected, code


def test_every_other_item_is_not_required():
    items = compute_section_d(build_section_d_site())
    accounted_for = set(EXPECTED_D_COMPUTED) | set(EXPECTED_D_TEXT)
    others = [i for i in items if i.code not in accounted_for]
    assert len(others) == 57 - len(accounted_for)
    for item in others:
        assert item.quantity == "Not Required", item.code


def test_empty_project_produces_zero_quantities():
    items = compute_section_d(_project())
    for code in EXPECTED_D_COMPUTED:
        assert _by_code(items, code).quantity == 0, code


# --- Inspection pits ---


def test_d1_counts_inspection_pits_with_a_recorded_depth():
    # 'Inspection pit'!H: =IF(E2>0,1,0) — IP03 has no recorded depth.
    assert _qty(build_section_d_site(), "D1") == 2


def test_d1_sums_every_inspection_pit_not_only_rows_65_to_91():
    pits = [
        InspectionPit(
            inspection_pit_number=f"IP{n:02d}", scheduled_depth_m=1.2, recorded_depth_m=1.2
        )
        for n in range(1, 71)
    ]
    assert _qty(_project(inspection_pits=pits), "D1") == 70


def test_d2_uses_recorded_not_scheduled_dimensions():
    # 'Inspection pit'!J: =F2*G2*I2 — F and G are the *recorded* length and width.
    pit = InspectionPit(
        inspection_pit_number="IP01",
        scheduled_depth_m=1.2,
        scheduled_length_m=9.0,
        scheduled_width_m=9.0,
        recorded_depth_m=1.2,
        recorded_length_m=0.5,
        recorded_width_m=0.4,
        depth_hard_surface_obstruction_m=0.2,
    )
    assert _qty(_project(inspection_pits=[pit]), "D2") == pytest.approx(0.5 * 0.4 * 0.2)


# --- Paved / non-paved handling ---


def test_trench_volumes_are_not_filtered_on_the_paved_column():
    # TR03 is marked PAVED but its non-paved metres still count towards D9 (Trenches!AD93).
    project = build_section_d_site()
    without_tr03 = project.model_copy(
        update={"trenches": [t for t in project.trenches if t.trench_number != "TR03"]}
    )
    assert _qty(project, "D9") - _qty(without_tr03, "D9") == pytest.approx(4.5)


def test_d14_filters_trial_pits_on_paved_but_not_trenches():
    non_paved_pit = TrialPit(
        trial_pit_number="TP01", schedule_depth_m=2.0, width_m=1.0, length_m=3.0
    )
    non_paved_trench = Trench(trench_number="TR01", paved_length_m=4.0, paved_width_m=0.5)
    project = _project(trial_pits=[non_paved_pit], trenches=[non_paved_trench])
    # Pit perimeter (8.0) excluded; trench paved perimeter 2×4 + 2×0.5 = 9.0 included.
    assert _qty(project, "D14") == pytest.approx(9.0)


# --- Deliberate deviations and open items ---


def test_d16_is_paved_trial_pit_depth_0_to_1_2m():
    # Deviation from ='Trial Pits'!$V$92+Trenches!$Q93: follows D17's SUMIFS pattern on column Q.
    assert _qty(build_section_d_site(), "D16") == pytest.approx(2.2)


def test_d19_is_paved_trench_volume_1_2_to_3m():
    # Deviation from =Trenches!$X93 (empty column): uses Trenches!$T93.
    assert _qty(build_section_d_site(), "D19") == pytest.approx(2.4)


def test_d20_is_half_an_hour_per_non_paved_pit_or_trench():
    # 'Section D'!D34: =D15*0.5 — Calculator row 15 is item D3, not item D15.
    project = build_section_d_site()
    assert _qty(project, "D20") == pytest.approx(_qty(project, "D3") * 0.5)


def test_d55_is_always_zero():
    # Open item: the referenced Log Tracker cells are empty.
    assert _qty(build_section_d_site(), "D55") == 0


@pytest.mark.parametrize(
    ("depth", "band_0_3", "band_3_4_5"),
    [
        (2.5, 2.5, 0.0),
        (3.0, 3.0, 0.0),
        (4.0, 3.0, 1.0),
        (4.5, 3.0, 1.5),
        (5.0, 3.0, 1.5),  # workbook gives 4.5 here; engine caps at the band thickness
    ],
)
def test_non_paved_trial_pit_depth_bands(depth: float, band_0_3: float, band_3_4_5: float):
    pit = TrialPit(trial_pit_number="TP01", schedule_depth_m=depth, depth_m=depth)
    project = _project(trial_pits=[pit])
    assert _qty(project, "D6") == pytest.approx(band_0_3)
    assert _qty(project, "D7") == pytest.approx(band_3_4_5)


@pytest.mark.parametrize(
    ("depth", "band_0_1_2", "band_1_2_3"),
    [
        (1.0, 1.0, 0.0),
        (1.2, 1.2, 0.0),
        (2.0, 1.2, 0.8),
        (3.0, 1.2, 1.8),
        (3.5, 1.2, 1.8),
    ],
)
def test_paved_trial_pit_depth_bands(depth: float, band_0_1_2: float, band_1_2_3: float):
    pit = TrialPit(trial_pit_number="TP01", paved=True, schedule_depth_m=depth, depth_m=depth)
    project = _project(trial_pits=[pit])
    assert _qty(project, "D16") == pytest.approx(band_0_1_2)
    assert _qty(project, "D17") == pytest.approx(band_1_2_3)


# --- Backfill and reinstatement ---


def test_d49_is_holes_dug_minus_national_road_holes():
    assert _qty(build_section_d_site(), "D49") == 5


def test_d51_and_d53_split_rural_and_national_rules():
    rural = TrialPit(
        trial_pit_number="TP01", paved=True, road="RURAL", schedule_depth_m=1.5,
        width_m=0.6, length_m=2.0, depth_m=1.5,
    )  # fmt: skip
    national = rural.model_copy(update={"trial_pit_number": "TP02", "road": "NATIONAL"})
    # Rural: 100 mm surfacing and a 200 mm wider cut-back; national: 450 mm surfacing, no cut-back.
    assert _qty(_project(trial_pits=[rural]), "D51") == pytest.approx(0.6 * 2.0 * 1.4)
    assert _qty(_project(trial_pits=[national]), "D51") == pytest.approx(1.05 * 0.6 * 2.0)
    assert _qty(_project(trial_pits=[rural]), "D53") == pytest.approx(0.8 * 2.2)
    assert _qty(_project(trial_pits=[national]), "D53") == pytest.approx(0.6 * 2.0)


# --- Structure ---


def test_section_d_has_57_items_with_unique_codes():
    codes = [i.code for i in compute_section_d(_project())]
    assert len(codes) == 57
    assert len(set(codes)) == 57


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {i.code: i.subheading for i in compute_section_d(_project()) if i.subheading}
    assert subheadings == {
        "D1": (
            "Inspection pits Included for each exploratory hole: refer hand digging "
            "and CAT scan items at exploratory hole locations"
        ),
        "D3": "Trial pits and trenches (non paved areas)",
        "D12": "Trial pits and trenches (paved areas)",
        "D21": "Observation pits and trenches",
        "D36": "Daily provision of pitting crew and equipment",
        "D44": "General",
        "D49": "Trial pit / slit trench backfill & reinstatement works",
    }


def test_models_have_no_completed_flag():
    # "Completed" is derived from the recorded depth in the Log Tracker.
    for model in (TrialPit, Trench, InspectionPit):
        assert "completed" not in model.model_fields, model.__name__
