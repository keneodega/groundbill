"""Tests for the Section F calculation engine.

Expected quantities come from ``tests/fixtures/section_f_site.py``, where the
arithmetic is set out against the Calculator formulas. Row-for-row agreement
of codes, descriptions and units with the reference workbook is checked in
``test_workbook_fidelity.py``.
"""

import pytest

from groundbill.engine import BoqItem, compute_section_f
from groundbill.models import CPT, ContractRoute, DynamicProbe, Project
from tests.fixtures.section_f_site import EXPECTED_F, build_section_f_site


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


def _project_with(**holes) -> Project:
    return _empty_project().model_copy(update=holes)


def test_fixture_quantities_match_hand_derived_values():
    items = compute_section_f(build_section_f_site())
    actual = {i.code: i.quantity for i in items}
    assert list(actual) == list(EXPECTED_F)  # same codes, same order
    for code, expected in EXPECTED_F.items():
        if isinstance(expected, int | float):
            assert actual[code] == pytest.approx(expected), code
        else:
            assert actual[code] == expected, code


# --- Dynamic probing ---


def test_f1_counts_every_probe_with_a_depth():
    # DPH!H ("Completed") is =IF(C2>0,1,0), so every probe with a depth counts.
    assert _by_code(compute_section_f(build_section_f_site()), "F1").quantity == 3


def test_f6_standing_time_is_half_an_hour_per_probe():
    # 'Section F'!D16: =D11/2
    assert _by_code(compute_section_f(build_section_f_site()), "F6").quantity == pytest.approx(1.5)


@pytest.mark.parametrize(
    ("depth", "bands"),
    [
        (4.0, (4.0, 0.0, 0.0)),
        (5.0, (5.0, 0.0, 0.0)),  # exactly on the 5 m boundary
        (7.5, (5.0, 2.5, 0.0)),
        (10.0, (5.0, 5.0, 0.0)),  # exactly on the 10 m boundary
        (12.0, (5.0, 5.0, 2.0)),
        (15.0, (5.0, 5.0, 5.0)),
        (17.0, (5.0, 5.0, 5.0)),  # metres below 15 m are not measured
    ],
)
def test_dph_depth_bands(depth: float, bands: tuple[float, float, float]):
    project = _project_with(dynamic_probes=[DynamicProbe(probe_number="DP01", depth_m=depth)])
    items = compute_section_f(project)
    actual = tuple(_by_code(items, code).quantity for code in ("F3", "F4", "F5"))
    assert actual == pytest.approx(bands)


# --- Cone penetration testing ---


def test_f8_counts_every_cpt_including_piezocone():
    # CPT!K ("Completed") is =IF(D2>0,1,0); the Piezocone column is not read by any formula.
    assert _by_code(compute_section_f(build_section_f_site()), "F8").quantity == 5


def test_f9_is_cpts_on_a_slope():
    # 'Section F'!D20: =COUNTIF(CPT!$B$2:$B91,"YES")
    assert _by_code(compute_section_f(build_section_f_site()), "F9").quantity == 2


def test_f18_standing_time_is_half_an_hour_per_cpt():
    # 'Section F'!D29: =D19/2
    assert _by_code(compute_section_f(build_section_f_site()), "F18").quantity == pytest.approx(2.5)


@pytest.mark.parametrize(
    ("depth", "bands"),
    [
        (8.0, (8.0, 0.0, 0.0, 0.0)),
        (10.0, (10.0, 0.0, 0.0, 0.0)),  # exactly on the 10 m boundary
        (15.0, (10.0, 5.0, 0.0, 0.0)),
        (22.0, (10.0, 10.0, 2.0, 0.0)),
        (40.0, (10.0, 10.0, 10.0, 10.0)),
        (45.0, (10.0, 10.0, 10.0, 10.0)),  # metres below 40 m are not measured
    ],
)
def test_cpt_depth_bands(depth: float, bands: tuple[float, float, float, float]):
    project = _project_with(cpts=[CPT(cpt_number="CPT01", depth_m=depth)])
    items = compute_section_f(project)
    actual = tuple(_by_code(items, code).quantity for code in ("F10", "F11", "F12", "F13"))
    assert actual == pytest.approx(bands)


# --- Structure ---


def test_empty_project_produces_zero_quantities():
    items = compute_section_f(_empty_project())
    computed = ("F1", "F2", "F3", "F4", "F5", "F6", "F8", "F9", "F10", "F11", "F12", "F13", "F18")
    for code in computed:
        assert _by_code(items, code).quantity == 0, code


def test_subheadings_sit_on_first_item_of_each_group():
    subheadings = {
        i.code: i.subheading for i in compute_section_f(_empty_project()) if i.subheading
    }
    assert subheadings == {
        "F1": "Dynamic probing (DPH)",
        "F8": "Cone penetration testing",
    }


def test_models_have_no_completed_flag():
    # "Completed" is derived from depth in the Log Tracker, so it is not a model input.
    assert "completed" not in DynamicProbe.model_fields
    assert "completed" not in CPT.model_fields
