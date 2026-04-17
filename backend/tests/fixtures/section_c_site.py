"""Fixture: a project designed to exercise every Section C branch.

Borehole mix (rotary drilling)
------------------------------
- BH01: CP/RC, no barrier, no slope — 10 m CP + 8 m ROTARY_CORE_HARD
         → C15.1.1 contributes 1
         → RC_CORE_HARD bands: start=10, end=18 → 0-10: 0, 10-20: 8, 20-30: 0, 30-40: 0
- BH02: CP/RC, over barrier, slope — 5 m CP + 12 m ROTARY_NO_CORE_SOFT
         → C15.1.2 contributes 1, C16 contributes 1
         → RC_NO_CORE_SOFT bands: start=5, end=17 → 0-10: 5, 10-20: 7, 20-30: 0, 30-40: 0
- BH03: RC only, no barrier, no slope — 15 m ROTARY_CORE_SOFT
         → C15.2.1 contributes 1, C15.3 contributes 1
         → RC_CORE_SOFT bands: start=0, end=15 → 0-10: 10, 10-20: 5, 20-30: 0, 30-40: 0
- BH04: RC only, over barrier, slope — 25 m ROTARY_NO_CORE_HARD
         → C15.2.2 contributes 1, C15.3 contributes 1, C16 contributes 1
         → RC_NO_CORE_HARD bands: start=0, end=25 → 0-10: 10, 10-20: 10, 20-30: 5, 30-40: 0
- BH05: CP only, 10 m — NOT in Section C (no rotary phases)

Expected counts
---------------
- C15.1.1 = 1 (BH01)
- C15.1.2 = 1 (BH02)
- C15.2.1 = 1 (BH03)
- C15.2.2 = 1 (BH04)
- C15.3   = 2 (BH03, BH04 — RC-only)
- C16     = 2 (BH02, BH04 — on slopes)
- C19     = 4 (total rotary BH count: 1+1+1+1)

Depth-band totals
-----------------
- RC_CORE_HARD (C41-C44):    [0, 8, 0, 0]  (BH01)
- RC_NO_CORE_SOFT (C21-C24): [5, 7, 0, 0]  (BH02)
- RC_CORE_SOFT (C34-C37):    [10, 5, 0, 0] (BH03)
- RC_NO_CORE_HARD (C27-C30): [10, 10, 5, 0] (BH04)

C18 = 0 (no boreholes with road="YES")
"""

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    Project,
    SiteCategory,
)


def build_section_c_site() -> Project:
    return Project(
        name="Section C Test Site",
        site_address="3 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            # BH01: CP/RC, no barrier, no slope
            Borehole(
                hole_number="BH01",
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
            # BH05: CP only — excluded from Section C
            Borehole(
                hole_number="BH05",
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0),
                ],
                total_schedule_depth_m=10.0,
            ),
        ],
    )
