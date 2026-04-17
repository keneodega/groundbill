"""Fixture: a project designed to exercise every Section F branch.

Dynamic probe mix
-----------------
- DP01: depth=4m, completed, no slope
  → F3 band 0-5: 4, band 5-10: 0, band 10-15: 0
- DP02: depth=12m, completed, on slope
  → F3 band 0-5: 5, band 5-10: 5, band 10-15: 2
- DP03: depth=6m, NOT completed (should be excluded from all counts)

Expected DP totals
------------------
- F1 (completed count) = 2
- F2 (slope count) = 1
- F3 (band 0-5) = 4 + 5 = 9
- F4 (band 5-10) = 0 + 5 = 5
- F5 (band 10-15) = 0 + 2 = 2
- F6 (standing time) = 2

CPT mix
-------
- CPT01: depth=8m, completed, standard (not piezocone), no slope
  → F11 band 0-10: 8, bands 10-20/20-30/30-40: 0
- CPT02: depth=22m, completed, standard, on slope
  → F11 band 0-10: 10, band 10-20: 10, band 20-30: 2, band 30-40: 0
- CPT03: depth=15m, completed, piezocone, no slope
  → F11 band 0-10: 10, band 10-20: 5, band 20-30: 0, band 30-40: 0
- CPT04: depth=5m, NOT completed (should be excluded)

Expected CPT totals
-------------------
- F8 (standard completed) = 2
- F9 (piezocone completed) = 1
- F10 (slope count) = 1
- F11 (band 0-10) = 8 + 10 + 10 = 28
- F12 (band 10-20) = 0 + 10 + 5 = 15
- F13 (band 20-30) = 0 + 2 + 0 = 2
- F14 (band 30-40) = 0
- F15 (standing time) = 2 + 1 = 3
"""

from groundbill.models import (
    CPT,
    ContractRoute,
    DynamicProbe,
    Project,
    SiteCategory,
)


def build_section_f_site() -> Project:
    return Project(
        name="Section F Test Site",
        site_address="6 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        dynamic_probes=[
            DynamicProbe(
                probe_number="DP01",
                depth_m=4.0,
                completed=True,
            ),
            DynamicProbe(
                probe_number="DP02",
                depth_m=12.0,
                completed=True,
                slope_over_20pct=True,
            ),
            # DP03: not completed — excluded
            DynamicProbe(
                probe_number="DP03",
                depth_m=6.0,
                completed=False,
            ),
        ],
        cpts=[
            CPT(
                cpt_number="CPT01",
                depth_m=8.0,
                completed=True,
            ),
            CPT(
                cpt_number="CPT02",
                depth_m=22.0,
                completed=True,
                slope_over_20pct=True,
            ),
            CPT(
                cpt_number="CPT03",
                depth_m=15.0,
                completed=True,
                piezocone=True,
            ),
            # CPT04: not completed — excluded
            CPT(
                cpt_number="CPT04",
                depth_m=5.0,
                completed=False,
            ),
        ],
    )
