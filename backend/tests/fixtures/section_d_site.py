"""Fixture: a project designed to exercise every Section D branch.

Trial pit mix
-------------
- TP01: non-paved, no barrier, no slope, no traffic, depth=2.5m, w=1.0, l=2.0
        completed, road=None, hard_material=0.3m
        → D3 contributes 1, D6 += 2.5, D7 += 0
- TP02: non-paved, barrier, slope, traffic, depth=4.0m, w=1.2, l=2.5
        completed, road=None, hard_material=0.0m
        → D3 += 1, D3.1 += 1, D4 += 1, D6 += 3.0, D7 += 1.0, D12 += 1
- TP03: paved, no barrier, no slope, traffic, depth=2.0m, w=1.0, l=1.5
        completed, road="RURAL", hard_material=0.4m
        → D12 += 1, D14 += 2*1.0+2*1.5 = 5.0
        → D15 += 1.0*1.5*0.4 = 0.6, D16 += 0.6 (hard vol)
        → D17 += min(1.8, max(0, 2.0-1.2)) = 0.8
        → D49 += 1 (completed, not national)
        → D51 += 1.0*1.5*(2.0-0.1) = 2.85
        → D53 += (1.0+0.2)*(1.5+0.2) = 1.2*1.7 = 2.04
- TP04: paved, no barrier, no slope, no traffic, depth=1.5m, w=0.8, l=1.2
        completed, road="NATIONAL", hard_material=0.2m
        → D14 += 2*0.8+2*1.2 = 4.0
        → D15 += 0.8*1.2*0.2 = 0.192, D16 += 0.192
        → D17 += min(1.8, max(0, 1.5-1.2)) = 0.3
        → D49: completed but national → excluded from non-national count
        → D51 += (1.5-0.45)*0.8*1.2 = 1.05*0.96 = 1.008
        → D53 += 0.8*1.2 = 0.96

Trench mix
----------
- TR01: non-paved, no barrier, no slope, traffic, np_l=5.0, np_w=0.6, np_d=2.5
        completed, road=None
        → D3 += 1, D9 += 5.0*0.6*2.5 = 7.5, D10 += 0, D13 += 1
- TR02: paved, barrier, slope, no traffic, p_l=4.0, p_w=0.5, p_d=2.0, p_hard=0.3
        completed, road="RURAL"
        → D14 += 2*0.5+2*4.0 = 9.0
        → D15 += 4.0*0.5*0.3 = 0.6, D16 += 4.0*0.5*min(2.0,1.2) = 2.4
        → D18 += 4.0*0.5*1.2 = 2.4
        → D19 += 4.0*0.5*min(1.8,max(0,2.0-1.2)) = 4.0*0.5*0.8 = 1.6
        → D51 += 4.0*0.5*(2.0-0.1) = 3.8
        → D53 += (4.0+0.2)*(0.5+0.2) = 4.2*0.7 = 2.94

Inspection pits
---------------
- IP01: completed, scheduled_depth=1.0, scheduled_length=0.5, scheduled_width=0.5,
        depth_hard_surface=0.2 → D1=1, D2=0.2*0.5*0.5=0.05
- IP02: not completed, scheduled_depth=1.5 → D1 not counted

Expected totals
---------------
- D1  = 1
- D2  = 0.05
- D3  = 3  (TP01 + TP02 + TR01 — all non-paved)
- D3.1 = 1  (TP02 — non-paved with barrier)
- D4  = 1  (TP02 — non-paved on slope)
- D6  = 5.5 (TP01: 2.5 + TP02: 3.0)
- D7  = 1.0 (TP02: min(1.5, max(0, 4.0-3)) = 1.0)
- D9  = 7.5
- D10 = 0
- D12 = 2  (TP02 + TP03)
- D13 = 1  (TR01)
- D14 = 5.0 + 4.0 + 9.0 = 18.0
- D15 = 0.6 + 0.192 + 0.6 = 1.392
- D16 = 0.6 + 0.192 + 2.4 = 3.192
- D17 = 0.8 + 0.3 = 1.1
- D18 = 2.4
- D19 = 1.6
- D20 = 1.392 * 0.5 = 0.696
- D49 = (4 completed TPs + 2 completed trenches) - (1 national TP + 0 national trenches) = 5
- D51 = 2.85 + 1.008 + 3.8 + 0 = 7.658
- D53 = 2.04 + 0.96 + 2.94 + 0 = 5.94
- D55 = 0
"""

from groundbill.models import (
    ContractRoute,
    InspectionPit,
    Project,
    SiteCategory,
    Trench,
    TrialPit,
)


def build_section_d_site() -> Project:
    return Project(
        name="Section D Test Site",
        site_address="4 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        trial_pits=[
            # TP01: non-paved, basic
            TrialPit(
                trial_pit_number="TP01",
                paved=False,
                schedule_depth_m=3.0,
                completed=True,
                width_m=1.0,
                length_m=2.0,
                depth_m=2.5,
                depth_of_hard_material_m=0.3,
            ),
            # TP02: non-paved, barrier, slope, traffic
            TrialPit(
                trial_pit_number="TP02",
                barrier=True,
                paved=False,
                slope_over_20pct=True,
                traffic_management=True,
                schedule_depth_m=4.5,
                completed=True,
                width_m=1.2,
                length_m=2.5,
                depth_m=4.0,
                depth_of_hard_material_m=0.0,
            ),
            # TP03: paved, traffic, RURAL road
            TrialPit(
                trial_pit_number="TP03",
                paved=True,
                traffic_management=True,
                road="RURAL",
                schedule_depth_m=2.0,
                completed=True,
                width_m=1.0,
                length_m=1.5,
                depth_m=2.0,
                depth_of_hard_material_m=0.4,
            ),
            # TP04: paved, NATIONAL road
            TrialPit(
                trial_pit_number="TP04",
                paved=True,
                road="NATIONAL",
                schedule_depth_m=1.5,
                completed=True,
                width_m=0.8,
                length_m=1.2,
                depth_m=1.5,
                depth_of_hard_material_m=0.2,
            ),
        ],
        trenches=[
            # TR01: non-paved, traffic
            Trench(
                trench_number="TR01",
                paved=False,
                traffic_management=True,
                completed=True,
                non_paved_length_m=5.0,
                non_paved_width_m=0.6,
                non_paved_depth_m=2.5,
            ),
            # TR02: paved, barrier, slope, RURAL road
            Trench(
                trench_number="TR02",
                paved=True,
                barrier=True,
                slope_over_20pct=True,
                road="RURAL",
                completed=True,
                paved_length_m=4.0,
                paved_width_m=0.5,
                paved_depth_m=2.0,
                paved_depth_hard_material_m=0.3,
            ),
        ],
        inspection_pits=[
            # IP01: completed with hard surface obstruction
            InspectionPit(
                inspection_pit_number="IP01",
                scheduled_depth_m=1.0,
                scheduled_length_m=0.5,
                scheduled_width_m=0.5,
                completed=True,
                depth_hard_surface_obstruction_m=0.2,
            ),
            # IP02: not completed
            InspectionPit(
                inspection_pit_number="IP02",
                scheduled_depth_m=1.5,
                completed=False,
            ),
        ],
    )
