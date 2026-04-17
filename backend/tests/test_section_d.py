"""Tests for the Section D calculation engine."""

import pytest

from groundbill.engine import BoqItem, compute_section_d
from groundbill.models import (
    ContractRoute,
    Project,
)
from tests.fixtures.section_d_site import build_section_d_site


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


def test_d1_inspection_pit_completed_count():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D1").quantity == 1


def test_d2_inspection_pit_hard_surface_volume():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D2").quantity == pytest.approx(0.05)


def test_d3_non_paved_count():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D3").quantity == 3  # TP01 + TP02 + TR01


def test_d3_1_non_paved_with_barrier():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D3.1").quantity == 1  # TP02


def test_d4_non_paved_on_slopes():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D4").quantity == 1  # TP02


def test_d6_non_paved_tp_band_0_3():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D6").quantity == pytest.approx(5.5)  # 2.5 + 3.0


def test_d7_non_paved_tp_band_3_4_5():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D7").quantity == pytest.approx(1.0)  # TP02: min(1.5, 4.0-3) = 1.0


def test_d9_non_paved_trench_vol_0_3():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D9").quantity == pytest.approx(7.5)  # 5.0*0.6*2.5


def test_d10_non_paved_trench_vol_3_4_5():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D10").quantity == 0


def test_d12_tp_traffic_management():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D12").quantity == 2  # TP02 + TP03


def test_d13_trench_traffic_management():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D13").quantity == 1  # TR01


def test_d14_paved_perimeter():
    items = compute_section_d(build_section_d_site())
    # TP03: 2*1.0+2*1.5=5.0, TP04: 2*0.8+2*1.2=4.0, TR02: 2*0.5+2*4.0=9.0
    assert _by_code(items, "D14").quantity == pytest.approx(18.0)


def test_d15_hard_material_volume():
    items = compute_section_d(build_section_d_site())
    # TP01: 1.0*2.0*0.3=0.6, TP02: 0, TP03: 1.0*1.5*0.4=0.6, TP04: 0.8*1.2*0.2=0.192
    # TR02: 4.0*0.5*0.3=0.6, TR01: 0 (no paved dims)
    assert _by_code(items, "D15").quantity == pytest.approx(1.992)


def test_d16_paved_0_1_2_excavation():
    items = compute_section_d(build_section_d_site())
    # TP hard material: 0.6+0+0.6+0.192=1.392
    # TR02 paved 0-1.2: 4.0*0.5*min(2.0,1.2)=2.4
    assert _by_code(items, "D16").quantity == pytest.approx(3.792)


def test_d17_paved_tp_band_1_2_3():
    items = compute_section_d(build_section_d_site())
    # TP03: min(1.8, max(0, 2.0-1.2))=0.8, TP04: min(1.8, max(0, 1.5-1.2))=0.3
    assert _by_code(items, "D17").quantity == pytest.approx(1.1)


def test_d18_paved_trench_vol_0_1_2():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D18").quantity == pytest.approx(2.4)  # TR02: 4.0*0.5*1.2


def test_d19_paved_trench_vol_1_2_3():
    items = compute_section_d(build_section_d_site())
    # TR02: 4.0*0.5*min(1.8, max(0, 2.0-1.2))=4.0*0.5*0.8=1.6
    assert _by_code(items, "D19").quantity == pytest.approx(1.6)


def test_d20_standing_time():
    items = compute_section_d(build_section_d_site())
    d15 = _by_code(items, "D15").quantity
    assert _by_code(items, "D20").quantity == pytest.approx(d15 * 0.5)


def test_d49_backfill_excluding_national():
    items = compute_section_d(build_section_d_site())
    # 4 completed TPs + 2 completed trenches - 1 national TP - 0 national trenches = 5
    assert _by_code(items, "D49").quantity == 5


def test_d51_imported_granular_fill():
    items = compute_section_d(build_section_d_site())
    # TP03 RURAL: 1.0*1.5*(2.0-0.1)=2.85
    # TP04 NATIONAL: (1.5-0.45)*0.8*1.2=1.05*0.96=1.008
    # TR02 RURAL: 4.0*0.5*(2.0-0.1)=3.8
    assert _by_code(items, "D51").quantity == pytest.approx(7.658)


def test_d53_asphalt_reinstatement():
    items = compute_section_d(build_section_d_site())
    # TP03 RURAL: (1.0+0.2)*(1.5+0.2)=1.2*1.7=2.04
    # TP04 NATIONAL: 0.8*1.2=0.96
    # TR02 RURAL: (4.0+0.2)*(0.5+0.2)=4.2*0.7=2.94
    assert _by_code(items, "D53").quantity == pytest.approx(5.94)


def test_d55_disposal_is_zero():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D55").quantity == 0


def test_empty_project_produces_zero_quantities():
    items = compute_section_d(_empty_project())
    for code in (
        "D1",
        "D2",
        "D3",
        "D3.1",
        "D4",
        "D6",
        "D7",
        "D9",
        "D10",
        "D12",
        "D13",
        "D14",
        "D15",
        "D16",
        "D17",
        "D18",
        "D19",
        "D20",
        "D49",
        "D51",
        "D53",
        "D55",
    ):
        assert _by_code(items, code).quantity == 0, code


def test_placeholder_items():
    items = compute_section_d(build_section_d_site())
    assert _by_code(items, "D5").quantity == "Included in D3"
    assert _by_code(items, "D8").quantity == "Not Required"
    assert _by_code(items, "D11").quantity == "Not Required"


def test_item_codes_are_unique_within_section_d():
    codes = _codes(compute_section_d(build_section_d_site()))
    assert len(codes) == len(set(codes)), f"duplicate codes in Section D: {codes}"


def test_section_d_item_count_is_stable():
    assert len(compute_section_d(_empty_project())) == len(
        compute_section_d(build_section_d_site())
    )
