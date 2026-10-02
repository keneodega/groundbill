"""Fixture: a project designed to exercise every Section D formula.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Trial pits ('Trial Pits' sheet)
-------------------------------
=====  =========  =======  =====  ===  ========  =====  ======  =====  ====
Pit    C          Barrier  Slope  TM   Road      Width  Length  Depth  Hard
=====  =========  =======  =====  ===  ========  =====  ======  =====  ====
TP01   NON-PAVED  YES      -      -    -         1.0    3.0     2.5    -
TP02   NON-PAVED  -        YES    -    -         1.0    3.0     4.0    -
TP03   PAVED      -        -      YES  RURAL     0.6    2.0     1.5    0.3
TP04   PAVED      -        -      YES  NATIONAL  0.5    2.0     1.0    0.2
TP05   NON-PAVED  -        -      -    -         (scheduled only, not yet dug)
=====  =========  =======  =====  ===  ========  =====  ======  =====  ====

Derived columns:

- O (0-3 m)       TP01 2.5   TP02 3.0   TP05 0
- P (3-4.5 m)     TP01 0     TP02 1.0   TP05 0
- Q (0-1.2 m)     TP03 1.2   TP04 1.0
- R (1.2-3 m)     TP03 0.3   TP04 0
- T (perimeter)   TP03 2×0.6 + 2×2.0 = 5.2        TP04 2×0.5 + 2×2.0 = 5.0
- V (hard vol)    TP03 0.6×2.0×0.3 = 0.36         TP04 0.5×2.0×0.2 = 0.20
- X (804 rural)   TP03 0.6×2.0×(1.5−0.1) = 1.68
- Y (804 nat.)    TP04 (1.0−0.45)×0.5×2.0 = 0.55
- AA (asph. rur.) TP03 (0.6+0.2)×(2.0+0.2) = 1.76
- AB (asph. nat.) TP04 0.5×2.0 = 1.00
- I (completed)   TP01-TP04 = 1 each; TP05 = 0

Trenches ('Trenches' sheet)
---------------------------
=====  =========  =======  =====  ===  ========  ===================  =================
Trench C          Barrier  Slope  TM   Road      PAVED L × W × D      NON-PAVED L × W × D
=====  =========  =======  =====  ===  ========  ===================  =================
TR01   NON-PAVED  -        -      -    -         -                    10 × 0.8 × 3.5
TR02   PAVED      -        -      YES  RURAL     5 × 0.6 × 2.0        -
TR03   PAVED      -        -      YES  NATIONAL  3 × 0.6 × 1.0        5 × 0.6 × 1.5
TR04   NON-PAVED  YES      YES    -    -         (scheduled only, not yet dug)
=====  =========  =======  =====  ===  ========  ===================  =================

Depth of hard material: TR02 0.25 m, TR03 0.2 m. Recorded total depth
(column J): TR01 3.5, TR02 2.0, TR03 1.5, TR04 blank.

TR03 crosses both kinds of ground. It is marked PAVED in column C, but its
non-paved metres still count towards D9: the Calculator reads the trench
totals row without filtering on column C.

Derived columns:

- S (paved vol 0-1.2)    TR02 5×0.6×1.2 = 3.6      TR03 3×0.6×1.0 = 1.8
- T (paved vol 1.2-3)    TR02 5×0.6×0.8 = 2.4      TR03 0
- U (paved perimeter)    TR02 2×5 + 2×0.6 = 11.2   TR03 2×3 + 2×0.6 = 7.2
- V (hard vol)           TR02 5×0.6×0.25 = 0.75    TR03 3×0.6×0.2 = 0.36
- AD (non-paved 0-3)     TR01 10×0.8×3.0 = 24.0    TR03 5×0.6×1.5 = 4.5
- AE (non-paved 3-4.5)   TR01 10×0.8×0.5 = 4.0     TR03 0
- AG (804 rural)         TR02 5×0.6×(2.0−0.1) = 5.7
- AH (804 national)      TR03 (1.0−0.45)×3×0.6 = 0.99
- AI (asphalt rural)     TR02 (5+0.2)×(0.6+0.2) = 4.16
- AJ (asphalt national)  TR03 3×0.6 = 1.8
- K (completed)          TR01, TR02, TR03 = 1 each; TR04 = 0

Inspection pits ('Inspection pit' sheet)
----------------------------------------
- IP01  recorded 1.2 m deep, 0.5 × 0.5 m, 0.2 m hard surface → J = 0.5×0.5×0.2 = 0.05
- IP02  recorded 1.0 m deep, 0.6 × 0.5 m, 0.1 m hard surface → J = 0.6×0.5×0.1 = 0.03
- IP03  scheduled only                                       → H = 0, J = 0

Expected Section D quantities
-----------------------------
- D1   inspection pits dug                          = 2
- D2   0.05 + 0.03                                  = 0.08
- D3   NON-PAVED pits (TP01, TP02, TP05) + trenches (TR01, TR04) = 3 + 2 = 5
- D3.1 with barrier: TP01 + TR04                    = 2
- D4   on slope: TP02 + TR04                        = 2
- D6   O over NON-PAVED pits: 2.5 + 3.0 + 0         = 5.5
- D7   P over NON-PAVED pits: 0 + 1.0 + 0           = 1.0
- D9   AD93: 24.0 + 4.5                             = 28.5
- D10  AE93: 4.0 + 0                                = 4.0
- D12  pits with traffic management: TP03, TP04     = 2
- D13  trenches with traffic management: TR02, TR03 = 2
- D14  T over PAVED pits (5.2 + 5.0) + U93 (11.2 + 7.2) = 10.2 + 18.4 = 28.6
- D15  V92 (0.36 + 0.20) + V93 (0.75 + 0.36) = 0.56 + 1.11 = 1.67
- D16  Q over PAVED pits: 1.2 + 1.0                 = 2.2   (deliberate deviation)
- D17  R over PAVED pits: 0.3 + 0                   = 0.3
- D18  S93: 3.6 + 1.8                               = 5.4
- D19  T93: 2.4 + 0                                 = 2.4   (deliberate deviation)
- D20  D3 × 0.5 = 5 × 0.5                           = 2.5
- D49  (pits dug 4 + trenches dug 3) − (NATIONAL pits 1 + NATIONAL trenches 1) = 7 − 2 = 5
- D51  1.68 + 0.55 + 5.7 + 0.99                     = 8.92
- D53  1.76 + 1.00 + 4.16 + 1.8                     = 8.72
- D55  empty cells                                  = 0
"""

from groundbill.models import (
    ContractRoute,
    InspectionPit,
    Project,
    SiteCategory,
    Trench,
    TrialPit,
)

# Computed (numeric) items only; every other item is a text placeholder.
EXPECTED_D_COMPUTED = {
    "D1": 2,
    "D2": 0.08,
    "D3": 5,
    "D3.1": 2,
    "D4": 2,
    "D6": 5.5,
    "D7": 1.0,
    "D9": 28.5,
    "D10": 4.0,
    "D12": 2,
    "D13": 2,
    "D14": 28.6,
    "D15": 1.67,
    "D16": 2.2,
    "D17": 0.3,
    "D18": 5.4,
    "D19": 2.4,
    "D20": 2.5,
    "D49": 5,
    "D51": 8.92,
    "D53": 8.72,
    "D55": 0,
}

EXPECTED_D_TEXT = {
    "D36": "Included in A2, A2.4, D3 to D19",
    "D43": "To be included in item D13 to D15",
    "D50": "Included in Item D3 & D3.1",
    "D50.2": "Included in Item D3 & D3.1",
}


def build_section_d_site() -> Project:
    return Project(
        name="Section D Test Site",
        site_address="4 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        trial_pits=[
            TrialPit(
                trial_pit_number="TP01",
                barrier=True,
                schedule_depth_m=2.5,
                width_m=1.0,
                length_m=3.0,
                depth_m=2.5,
            ),
            TrialPit(
                trial_pit_number="TP02",
                slope_over_20pct=True,
                schedule_depth_m=4.0,
                width_m=1.0,
                length_m=3.0,
                depth_m=4.0,
            ),
            TrialPit(
                trial_pit_number="TP03",
                paved=True,
                traffic_management=True,
                road="RURAL",
                schedule_depth_m=1.5,
                width_m=0.6,
                length_m=2.0,
                depth_m=1.5,
                depth_of_hard_material_m=0.3,
            ),
            TrialPit(
                trial_pit_number="TP04",
                paved=True,
                traffic_management=True,
                road="NATIONAL",
                schedule_depth_m=1.0,
                width_m=0.5,
                length_m=2.0,
                depth_m=1.0,
                depth_of_hard_material_m=0.2,
            ),
            # TP05: scheduled but not yet dug — no recorded dimensions
            TrialPit(trial_pit_number="TP05", schedule_depth_m=3.0),
        ],
        trenches=[
            Trench(
                trench_number="TR01",
                overall_length_m=10.0,
                overall_width_m=0.8,
                overall_total_depth_m=3.5,
                non_paved_length_m=10.0,
                non_paved_width_m=0.8,
                non_paved_depth_m=3.5,
            ),
            Trench(
                trench_number="TR02",
                paved=True,
                traffic_management=True,
                road="RURAL",
                overall_length_m=5.0,
                overall_width_m=0.6,
                overall_total_depth_m=2.0,
                paved_length_m=5.0,
                paved_width_m=0.6,
                paved_depth_m=2.0,
                paved_depth_hard_material_m=0.25,
            ),
            # TR03: crosses paved and non-paved ground
            Trench(
                trench_number="TR03",
                paved=True,
                traffic_management=True,
                road="NATIONAL",
                overall_length_m=8.0,
                overall_width_m=0.6,
                overall_total_depth_m=1.5,
                paved_length_m=3.0,
                paved_width_m=0.6,
                paved_depth_m=1.0,
                paved_depth_hard_material_m=0.2,
                non_paved_length_m=5.0,
                non_paved_width_m=0.6,
                non_paved_depth_m=1.5,
            ),
            # TR04: scheduled but not yet dug
            Trench(trench_number="TR04", barrier=True, slope_over_20pct=True),
        ],
        inspection_pits=[
            InspectionPit(
                inspection_pit_number="IP01",
                scheduled_depth_m=1.2,
                recorded_depth_m=1.2,
                recorded_length_m=0.5,
                recorded_width_m=0.5,
                depth_hard_surface_obstruction_m=0.2,
            ),
            InspectionPit(
                inspection_pit_number="IP02",
                scheduled_depth_m=1.2,
                recorded_depth_m=1.0,
                recorded_length_m=0.6,
                recorded_width_m=0.5,
                depth_hard_surface_obstruction_m=0.1,
            ),
            # IP03: scheduled but not yet dug
            InspectionPit(inspection_pit_number="IP03", scheduled_depth_m=1.2),
        ],
    )
