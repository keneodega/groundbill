"""Tests for the Section I calculation engine.

Expected quantities come from ``tests/fixtures/section_i_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions and units with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_i
from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    Project,
)
from tests.fixtures.section_i_site import EXPECTED_I_COMPUTED, build_section_i_site


def _by_code(items: list[BoqItem], code: str) -> BoqItem:
    matches = [i for i in items if i.code == code]
    assert len(matches) == 1, f"Expected exactly one item with code {code}, got {len(matches)}"
    return matches[0]


def _project(**holes) -> Project:
    return Project(
        name="Test", site_address="Nowhere", contract_route=ContractRoute.PRIVATE, **holes
    )


def _qty(project: Project, code: str):
    return _by_code(compute_section_i(project), code).quantity


def _borehole(**kwargs) -> Borehole:
    return Borehole(
        hole_number="BH01",
        phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0)],
        total_schedule_depth_m=10.0,
        **kwargs,
    )


def _sample(**kwargs) -> DynamicSample:
    return DynamicSample(sample_number="DS01", depth_m=4.0, **kwargs)


def test_fixture_computed_quantities_match_hand_derived_values():
    items = compute_section_i(build_section_i_site())
    for code, expected in EXPECTED_I_COMPUTED.items():
        assert _by_code(items, code).quantity == pytest.approx(expected), code


def test_every_other_item_is_not_required():
    items = compute_section_i(build_section_i_site())
    others = [i for i in items if i.code not in EXPECTED_I_COMPUTED]
    assert len(others) == 35 - len(EXPECTED_I_COMPUTED)
    for item in others:
        assert item.quantity == "Not Required", item.code


def test_empty_project_produces_zero_quantities():
    items = compute_section_i(_project())
    for code in EXPECTED_I_COMPUTED:
        assert _by_code(items, code).quantity == 0, code


# --- Pipe lengths ---


def test_i1_backfill_is_the_sum_of_plain_pipe_depths():
    # 'Section I'!D11: =Boreholes!$BJ92+Boreholes!$BM92+'Dynamic Sampling'!$L$92
    project = _project(
        boreholes=[
            _borehole(
                piezometer=True,
                piezometer_plain_depth_m=8.0,
                standpipe=True,
                standpipe_plain_depth_m=3.0,
                standpipe_slotted_depth_m=6.0,
            )
        ],
        dynamic_samples=[_sample(standpipe=True, plain_depth_m=1.0, slotted_depth_m=3.0)],
    )
    assert _qty(project, "I1") == pytest.approx(8.0 + 3.0 + 1.0)  # slotted lengths excluded
    assert _qty(project, "I4") == pytest.approx(8.0)
    assert _qty(project, "I6") == pytest.approx(6.0 + 3.0)
    assert _qty(project, "I8") == pytest.approx(3.0 + 1.0)


def test_depth_totals_are_not_filtered_on_the_yes_flags():
    # Open item: the totals row is read as is, so a depth without its flag still counts.
    project = _project(boreholes=[_borehole(piezometer_plain_depth_m=4.0)])
    assert _qty(project, "I4") == pytest.approx(4.0)
    assert _qty(project, "I2") == 0


# --- Counts ---


def test_i2_counts_dynamic_sampling_standpipes_as_piezometer_tips():
    # Open item, translated literally: the second term reads 'Dynamic Sampling'!K.
    project = _project(
        boreholes=[_borehole(piezometer=True), _borehole(standpipe=True)],
        dynamic_samples=[_sample(standpipe=True)],
    )
    assert _qty(project, "I2") == 2  # one borehole piezometer + one DS standpipe
    assert _qty(project, "I3") == 2


def test_i5_counts_borehole_piezometers_only():
    project = _project(
        boreholes=[_borehole(piezometer=True)], dynamic_samples=[_sample(standpipe=True)]
    )
    assert _qty(project, "I5") == 1


def test_i9_counts_standpipe_plain_depths_and_complete_dynamic_samples():
    # COUNTIF(Boreholes!BM,">0") reads the plain depth, not the BL flag.
    project = _project(
        boreholes=[
            _borehole(standpipe=True),  # flag but no plain depth → not counted
            _borehole(standpipe_plain_depth_m=2.0),  # depth but no flag → counted
        ],
        dynamic_samples=[_sample(standpipe=True), _sample()],
    )
    assert _qty(project, "I9") == 2


def test_i14_is_two_end_caps_per_installation():
    project = _project(
        boreholes=[_borehole(piezometer=True, standpipe=True)],  # both on one hole → 2
        dynamic_samples=[_sample(standpipe=True)],
    )
    assert _qty(project, "I14") == (1 + 1 + 1) * 2


# --- Covers ---


def test_on_road_installation_gets_flush_cover():
    project = _project(boreholes=[_borehole(on_road=True, standpipe=True)])
    assert _qty(project, "I16") == 1
    assert _qty(project, "I17") == 0


def test_off_road_installation_gets_raised_cover_fencing_and_marker_posts():
    project = _project(dynamic_samples=[_sample(on_road=False, standpipe=True)])
    assert _qty(project, "I16") == 0
    for code in ("I17", "I19", "I20"):
        assert _qty(project, code) == 1, code


def test_holes_without_an_installation_get_no_cover():
    project = _project(boreholes=[_borehole(on_road=True)], dynamic_samples=[_sample()])
    assert _qty(project, "I16") == 0
    assert _qty(project, "I17") == 0


# --- Structure ---


def test_section_i_has_35_items_with_unique_codes():
    codes = [i.code for i in compute_section_i(_project())]
    assert codes == [f"I{n}" for n in range(1, 36)]


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {i.code: i.subheading for i in compute_section_i(_project()) if i.subheading}
    assert subheadings == {
        "I1": "Standpipes and piezometers",
        "I21": "Standpipe and piezometer development / purging",
        "I27": "Inclinometer",
        "I32": "Slip Indicator",
    }


def test_models_use_yes_no_flags_for_instrumentation():
    for field in ("on_road", "piezometer", "standpipe"):
        assert Borehole.model_fields[field].annotation is bool, field
    for field in ("on_road", "standpipe"):
        assert DynamicSample.model_fields[field].annotation is bool, field
    for removed in ("road", "standpipe_diameter_mm", "installation_complete", "piezometer_type"):
        assert removed not in Borehole.model_fields, removed
