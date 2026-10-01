"""Tests for the Section C calculation engine.

Expected quantities come from ``tests/fixtures/section_c_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions and units with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_c
from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    Project,
)
from tests.fixtures.section_c_site import (
    EXPECTED_C_COMPUTED,
    EXPECTED_C_TEXT,
    build_section_c_site,
)


def _by_code(items: list[BoqItem], code: str) -> BoqItem:
    matches = [i for i in items if i.code == code]
    assert len(matches) == 1, f"Expected exactly one item with code {code}, got {len(matches)}"
    return matches[0]


def _project(boreholes: list[Borehole]) -> Project:
    return Project(
        name="Test",
        site_address="Nowhere",
        contract_route=ContractRoute.PRIVATE,
        boreholes=boreholes,
    )


def _borehole(number: str, *phases: tuple[DrillingMethod, float], **kwargs) -> Borehole:
    return Borehole(
        hole_number=number,
        phases=[DrillingPhase(method=m, depth_m=d) for m, d in phases],
        total_schedule_depth_m=sum(d for _, d in phases),
        **kwargs,
    )


_CP = DrillingMethod.CABLE_PERCUSSION
_CORE_HARD = DrillingMethod.ROTARY_CORE_HARD


def test_fixture_computed_quantities_match_hand_derived_values():
    items = compute_section_c(build_section_c_site())
    for code, expected in EXPECTED_C_COMPUTED.items():
        assert _by_code(items, code).quantity == pytest.approx(expected), code


def test_fixture_text_placeholders_match_calculator():
    items = compute_section_c(build_section_c_site())
    for code, expected in EXPECTED_C_TEXT.items():
        assert _by_code(items, code).quantity == expected, code


def test_every_other_item_is_not_required():
    items = compute_section_c(build_section_c_site())
    accounted_for = set(EXPECTED_C_COMPUTED) | set(EXPECTED_C_TEXT)
    others = [i for i in items if i.code not in accounted_for]
    assert len(others) == 92 - len(accounted_for)
    for item in others:
        assert item.quantity == "Not Required", item.code


def test_section_c_has_92_items_with_unique_codes():
    codes = [i.code for i in compute_section_c(_project([]))]
    assert len(codes) == 92
    assert len(set(codes)) == 92


# --- Set-ups ---


def test_c15_splits_cp_rc_from_rc_and_by_barrier():
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C15.1.1").quantity == 2  # BH01, BH06: CP/RC, no barrier
    assert _by_code(items, "C15.1.2").quantity == 1  # BH02: CP/RC, barrier
    assert _by_code(items, "C15.2.1").quantity == 1  # BH03: RC, no barrier
    assert _by_code(items, "C15.2.2").quantity == 1  # BH04: RC, barrier


def test_c15_1_counts_all_cp_rc_boreholes_not_only_rows_2_to_38():
    # Deliberate deviation from $B$2:$B38: the 38th borehole onwards still counts.
    boreholes = [_borehole(f"BH{n:02d}", (_CP, 5.0), (_CORE_HARD, 5.0)) for n in range(1, 51)]
    items = compute_section_c(_project(boreholes))
    assert _by_code(items, "C15.1.1").quantity == 50


def test_c18_counts_every_borehole_with_road_yes_including_cp_only():
    # 'Section C'!D36: =(COUNTIF(Boreholes!$BH$2:$BH91,"YES"))*0.125
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C18").quantity == pytest.approx(0.25)


def test_c18_ignores_road_values_other_than_yes():
    # Open item: column BH is free text; only the literal "YES" matches.
    boreholes = [_borehole("BH01", (_CORE_HARD, 10.0), road="RURAL")]
    assert _by_code(compute_section_c(_project(boreholes)), "C18").quantity == 0


def test_c19_standing_time_is_one_hour_per_rotary_set_up():
    # 'Section C'!D37: =D32+D31+D30+D29
    items = compute_section_c(build_section_c_site())
    assert _by_code(items, "C19").quantity == 5


def test_cp_only_borehole_adds_no_set_ups_or_metres():
    items = compute_section_c(_project([_borehole("BH01", (_CP, 20.0))]))
    for code in EXPECTED_C_COMPUTED:
        assert _by_code(items, code).quantity == 0, code


# --- Depth bands ---


@pytest.mark.parametrize(
    ("cp_depth", "rotary_depth", "bands"),
    [
        (0.0, 8.0, (8.0, 0.0, 0.0, 0.0)),
        (0.0, 10.0, (10.0, 0.0, 0.0, 0.0)),  # exactly on the 10 m boundary
        (10.0, 8.0, (0.0, 8.0, 0.0, 0.0)),  # starts exactly on the boundary
        (5.0, 12.0, (5.0, 7.0, 0.0, 0.0)),
        (18.0, 17.0, (0.0, 2.0, 10.0, 5.0)),  # crosses three bands
        (0.0, 40.0, (10.0, 10.0, 10.0, 10.0)),
        (0.0, 45.0, (10.0, 10.0, 10.0, 10.0)),  # metres below 40 m are not measured
    ],
)
def test_rotary_depth_bands(cp_depth: float, rotary_depth: float, bands: tuple[float, ...]):
    phases = [(_CORE_HARD, rotary_depth)]
    if cp_depth:
        phases.insert(0, (_CP, cp_depth))
    items = compute_section_c(_project([_borehole("BH01", *phases)]))
    actual = tuple(_by_code(items, code).quantity for code in ("C41", "C42", "C43", "C44"))
    assert actual == pytest.approx(bands)


def test_phase_starting_below_30m_gives_no_negative_metres():
    # Deliberate deviation: the Log Tracker's 20-30 m formula returns 30-START
    # (here 30-32 = -2) for a phase starting below 30 m. The engine returns 0.
    items = compute_section_c(_project([_borehole("BH01", (_CP, 32.0), (_CORE_HARD, 6.0))]))
    actual = tuple(_by_code(items, code).quantity for code in ("C41", "C42", "C43", "C44"))
    assert actual == pytest.approx((0.0, 0.0, 0.0, 6.0))


def test_each_rotary_method_feeds_its_own_items():
    methods = {
        DrillingMethod.ROTARY_NO_CORE_SOFT: "C21",
        DrillingMethod.ROTARY_NO_CORE_HARD: "C27",
        DrillingMethod.ROTARY_CORE_SOFT: "C34",
        DrillingMethod.ROTARY_CORE_HARD: "C41",
    }
    for method, first_band_code in methods.items():
        items = compute_section_c(_project([_borehole("BH01", (method, 6.0))]))
        for code in methods.values():
            expected = 6.0 if code == first_band_code else 0.0
            assert _by_code(items, code).quantity == pytest.approx(expected), (method, code)


# --- Structure ---


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {i.code: i.subheading for i in compute_section_c(_project([])) if i.subheading}
    assert subheadings == {
        "C1": "Hand augering",
        "C7": "Continuous flight and hollow-stem flight augering",
        "C15": "Rotary drilling with and without core recovery",
        "C21": "Drilling without cores",
        "C34": "Drilling to obtain cores",
        "C50": "Rotary percussive drilling (Odex / Symmetrix)",
        "C59": "Geobor S Rotary Drilling",
        "C64": "Geobor S Rotary Coring (to produce 102mm diameter cores)",
        "C76": "Geobor S Rotary Drilling - Additional Items",
        "C81": "Reinstatement of Rotary Boreholes",
    }


def test_obstruction_and_backfill_units_use_cubic_metres():
    items = compute_section_c(_project([]))
    for code in ("C9", "C18", "C33", "C48", "C62", "C76", "C79", "C80", "C85"):
        assert _by_code(items, code).unit == "m³", code
