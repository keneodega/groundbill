"""Fixture: a project designed to exercise every Section B branch.

Borehole mix
------------
- 2 × CP-only, no barrier, no slope       → B1.1.1 contributes 2
- 1 × CP-only, over barrier, no slope     → B1.1.2 contributes 1
- 1 × CP/RC,   no barrier,  slope > 20%   → B1.2.1 contributes 1, B2.2 contributes 1
- 1 × CP/RC,   over barrier, slope > 20%  → B1.2.2 contributes 1, B2.2 contributes 1
- 1 × CP-only, slope > 20%                → B1.1.1 contributes 1, B2.1 contributes 1

Expected counts: B1.1.1=3, B1.1.2=1, B1.2.1=1, B1.2.2=1, total BH=6.
B2.1=1 (one CP-only on slope), B2.2=2 (both CP/RC on slope).

Depth distribution for B4-B7
----------------------------
- The two plain CP-only boreholes have a single 12 m CP phase each ⇒
  0-10 contributes 10 m × 2 = 20 m, 10-20 contributes 2 m × 2 = 4 m.
- The barrier CP-only borehole is 8 m CP ⇒ 0-10 contributes 8 m.
- The slope CP-only borehole is 35 m CP ⇒ 0-10: 10, 10-20: 10, 20-30: 10, 30-40: 5.
- The plain CP/RC borehole has 6 m CP + 4 m RC ⇒ 0-10 contributes 6 m.
- The barrier/slope CP/RC borehole has 15 m CP + 10 m RC ⇒ 0-10: 10, 10-20: 5.

Totals: B4 = 20+8+10+6+10 = 54 m; B5 = 4+10+5 = 19 m; B6 = 10 m; B7 = 5 m.

Dynamic sampling mix
--------------------
- DS01: 3 m depth, no slope       → band 0-5: 3, 5-10: 0, >10: 0
- DS02: 8 m depth, slope > 20%    → band 0-5: 5, 5-10: 3, >10: 0
- DS03: 14 m depth, no slope      → band 0-5: 5, 5-10: 5, >10: 4

Totals: B17 = 13 m, B18 = 8 m, B19 = 4 m; B13 = 3; B14 = 1; B20 = 1.5 h.
"""

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    Project,
    SiteCategory,
)


def build_section_b_site() -> Project:
    return Project(
        name="Section B Test Site",
        site_address="2 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=12.0)],
                total_schedule_depth_m=12.0,
            ),
            Borehole(
                hole_number="BH02",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=12.0)],
                total_schedule_depth_m=12.0,
            ),
            Borehole(
                hole_number="BH03",
                over_barrier_wall_fence=True,
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=8.0)],
                total_schedule_depth_m=8.0,
            ),
            Borehole(
                hole_number="BH04",
                slope_over_20pct=True,
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=35.0)],
                total_schedule_depth_m=35.0,
            ),
            Borehole(
                hole_number="BH05",
                slope_over_20pct=True,
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=6.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=4.0),
                ],
                total_schedule_depth_m=10.0,
            ),
            Borehole(
                hole_number="BH06",
                over_barrier_wall_fence=True,
                slope_over_20pct=True,
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=15.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_NO_CORE_HARD, depth_m=10.0),
                ],
                total_schedule_depth_m=25.0,
            ),
        ],
        dynamic_samples=[
            DynamicSample(sample_number="DS01", depth_m=3.0),
            DynamicSample(sample_number="DS02", depth_m=8.0, slope_over_20pct=True),
            DynamicSample(sample_number="DS03", depth_m=14.0),
        ],
    )
