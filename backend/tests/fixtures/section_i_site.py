"""Fixture: a project designed to exercise every Section I branch.

Borehole mix
------------
- BH01: piezometer, installation_complete, piezometer_plain_depth=10m, road=None
  → I1 += 1, I3 += 10, I10 += 1 (non-road)
- BH02: standpipe, installation_complete, standpipe_plain=8m, slotted=3m,
  diameter=50mm, road="RURAL"
  → I2 += 1, I4 += 8, I5 += 3, I6 += 1, I9 += 1 (rural)
- BH03: standpipe, installation_complete, standpipe_plain=5m, slotted=2m,
  diameter=19mm, road=None
  → I2 += 1, I4 += 5, I5 += 2, I7 += 1, I10 += 1 (non-road)
- BH04: no installation (piezometer_type=NONE) → excluded

Expected BH totals
------------------
- I1 = 1, I2 = 2, I3 = 10, I4 = 13, I5 = 5
- I6 = 1, I7 = 1, I8 = 3
- I9 = 1 (BH02 rural), I10 = 2 (BH01 + BH03 non-road)

Dynamic sample mix
------------------
- DS01: installation_complete, plain=4m, slotted=2m, diameter=50mm, road="RURAL"
  → I11 += 1, I12 += 4, I13 += 2, I14 += 1, I17 += 1
- DS02: installation_complete, plain=3m, slotted=1m, diameter=19mm, road=None
  → I11 += 1, I12 += 3, I13 += 1, I15 += 1, I18 += 1
- DS03: NOT installation_complete → excluded

Expected DS totals
------------------
- I11 = 2, I12 = 7, I13 = 3, I14 = 1, I15 = 1
- I16 = 2, I17 = 1, I18 = 1
"""

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    PiezometerType,
    Project,
    SiteCategory,
)


def build_section_i_site() -> Project:
    return Project(
        name="Section I Test Site",
        site_address="9 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            # BH01: piezometer, installed, non-road
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=15.0)],
                total_schedule_depth_m=15.0,
                piezometer_type=PiezometerType.PIEZOMETER,
                piezometer_plain_depth_m=10.0,
                installation_complete=True,
                road=None,
            ),
            # BH02: standpipe, installed, rural road, 50mm
            Borehole(
                hole_number="BH02",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=12.0)],
                total_schedule_depth_m=12.0,
                piezometer_type=PiezometerType.STANDPIPE,
                standpipe_plain_depth_m=8.0,
                standpipe_slotted_depth_m=3.0,
                standpipe_diameter_mm=50,
                installation_complete=True,
                road="RURAL",
            ),
            # BH03: standpipe, installed, non-road, 19mm
            Borehole(
                hole_number="BH03",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0)],
                total_schedule_depth_m=10.0,
                piezometer_type=PiezometerType.STANDPIPE,
                standpipe_plain_depth_m=5.0,
                standpipe_slotted_depth_m=2.0,
                standpipe_diameter_mm=19,
                installation_complete=True,
                road=None,
            ),
            # BH04: no instrumentation
            Borehole(
                hole_number="BH04",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=8.0)],
                total_schedule_depth_m=8.0,
            ),
        ],
        dynamic_samples=[
            # DS01: installed, rural, 50mm
            DynamicSample(
                sample_number="DS01",
                depth_m=6.0,
                installation_complete=True,
                plain_depth_m=4.0,
                slotted_depth_m=2.0,
                standpipe_diameter_mm=50,
                road="RURAL",
            ),
            # DS02: installed, non-road, 19mm
            DynamicSample(
                sample_number="DS02",
                depth_m=5.0,
                installation_complete=True,
                plain_depth_m=3.0,
                slotted_depth_m=1.0,
                standpipe_diameter_mm=19,
                road=None,
            ),
            # DS03: not installed
            DynamicSample(
                sample_number="DS03",
                depth_m=4.0,
                installation_complete=False,
            ),
        ],
    )
