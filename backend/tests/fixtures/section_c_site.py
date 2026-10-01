"""Fixture: a project designed to exercise every Section C formula.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Boreholes
---------
=====  ======  =======  =====  ====  ==========================================
Hole   Type    Barrier  Slope  ROAD  Phases (from the surface down)
=====  ======  =======  =====  ====  ==========================================
BH01   CP/RC   no       no     YES   10 m CP, then 8 m with core, hard (10-18)
BH02   CP/RC   YES      YES    -     5 m CP, then 12 m no core, soft (5-17)
BH03   RC      no       no     -     15 m with core, soft (0-15)
BH04   RC      YES      YES    -     25 m no core, hard (0-25)
BH05   CP      no       no     YES   10 m CP only
BH06   CP/RC   no       no     -     12 m CP, then 6 m with core, soft (12-18),
                                     then 17 m with core, hard (18-35)
=====  ======  =======  =====  ====  ==========================================

"Type" is the Boreholes!B value the engine derives from the phases.

Set-ups
-------
- C15.1.1 CP/RC, barrier "NO"   = 2   (BH01, BH06)
- C15.1.2 CP/RC, barrier "YES"  = 1   (BH02)
- C15.2.1 RC, barrier "NO"      = 1   (BH03)
- C15.2.2 RC, barrier "YES"     = 1   (BH04)
- C15.3   RC                    = 2   (BH03, BH04)
- C16     RC on slope + CP/RC on slope = 1 + 1 = 2   (BH04, BH02)
- C18     ROAD = "YES" × 0.125  = 2 × 0.125 = 0.25   (BH01 and BH05 — the
  formula counts every borehole, including the CP-only BH05)
- C19     =D32+D31+D30+D29      = 1 + 1 + 1 + 2 = 5

Drilling metres by band (0-10 / 10-20 / 20-30 / 30-40 m)
-------------------------------------------------------
WITHOUT CORE in SOFT strata (C21-C24, Boreholes BA:BD)
    BH02  5-17 m    →  5,  7,  0,  0
    Total              5,  7,  0,  0

WITHOUT CORE in HARD strata (C27-C30, Boreholes AG:AJ)
    BH04  0-25 m    → 10, 10,  5,  0
    Total             10, 10,  5,  0

WITH CORE in SOFT strata (C34-C37, Boreholes AQ:AT)
    BH03  0-15 m    → 10,  5,  0,  0
    BH06  12-18 m   →  0,  6,  0,  0
    Total             10, 11,  0,  0

WITH CORE in HARD strata (C41-C44, Boreholes W:Z)
    BH01  10-18 m   →  0,  8,  0,  0
    BH06  18-35 m   →  0,  2, 10,  5
    Total              0, 10, 10,  5

All other Section C items are text: "Not Required", "Refer to ..." or
"Included in ...".
"""

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    Project,
    SiteCategory,
)

# Computed (numeric) items only; every other item is a text placeholder.
EXPECTED_C_COMPUTED = {
    "C15.1.1": 2,
    "C15.1.2": 1,
    "C15.2.1": 1,
    "C15.2.2": 1,
    "C15.3": 2,
    "C16": 2,
    "C18": 0.25,
    "C19": 5,
    "C21": 5.0,
    "C22": 7.0,
    "C23": 0.0,
    "C24": 0.0,
    "C27": 10.0,
    "C28": 10.0,
    "C29": 5.0,
    "C30": 0.0,
    "C34": 10.0,
    "C35": 11.0,
    "C36": 0.0,
    "C37": 0.0,
    "C41": 0.0,
    "C42": 10.0,
    "C43": 10.0,
    "C44": 5.0,
}

EXPECTED_C_TEXT = {
    "C15": "Refer to C15.1.1 to C15.2.2 & C15.3",
    "C33": "Included in C15 to C15.2",
    "C48": "Included in C15 to C15.2",
    "C81": "Included in C15 to C15.2",
    "C82": "Included in D53",
    "C83": "Included in C15 to C15.2",
    "C85": "Included in C15 to C15.2",
}


def build_section_c_site() -> Project:
    return Project(
        name="Section C Test Site",
        site_address="3 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            # BH01: CP/RC, no barrier, no slope, ROAD = "YES"
            Borehole(
                hole_number="BH01",
                on_road=True,
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=8.0),
                ],
                total_schedule_depth_m=18.0,
            ),
            # BH02: CP/RC, over barrier, slope > 20%
            Borehole(
                hole_number="BH02",
                over_barrier_wall_fence=True,
                slope_over_20pct=True,
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=5.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_NO_CORE_SOFT, depth_m=12.0),
                ],
                total_schedule_depth_m=17.0,
            ),
            # BH03: RC only, no barrier, no slope
            Borehole(
                hole_number="BH03",
                phases=[
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_SOFT, depth_m=15.0),
                ],
                total_schedule_depth_m=15.0,
            ),
            # BH04: RC only, over barrier, slope > 20%
            Borehole(
                hole_number="BH04",
                over_barrier_wall_fence=True,
                slope_over_20pct=True,
                phases=[
                    DrillingPhase(method=DrillingMethod.ROTARY_NO_CORE_HARD, depth_m=25.0),
                ],
                total_schedule_depth_m=25.0,
            ),
            # BH05: CP only, ROAD = "YES" — counted by C18 but by no other Section C item
            Borehole(
                hole_number="BH05",
                on_road=True,
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0),
                ],
                total_schedule_depth_m=10.0,
            ),
            # BH06: CP/RC with two rotary methods, the second crossing three bands
            Borehole(
                hole_number="BH06",
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=12.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_SOFT, depth_m=6.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=17.0),
                ],
                total_schedule_depth_m=35.0,
            ),
        ],
    )
