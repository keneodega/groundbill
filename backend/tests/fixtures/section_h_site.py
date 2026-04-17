"""Fixture: a project designed to exercise every Section H branch.

Borehole mix (for SPT band tests)
----------------------------------
- BH01: 12 m CP → CP bands: 0-10: 10, 10-20: 2
- BH02: 8 m CP + 5 m RC_CORE_SOFT → CP bands: 0-10: 8; soft rotary bands: 0-10: 2(offset 8), 10-20: 3
  Actually: offset=8, soft start=8, end=13 → band 0-10: min(13,10)-max(8,0)=2, band 10-20: min(13,20)-max(8,10)=3
- BH03: 6 m CP + 9 m RC_NO_CORE_SOFT → CP bands: 0-10: 6; soft rotary: offset=6, end=15
  → band 0-10: min(15,10)-max(6,10)=0, wait: max(6,10)=10, min(15,10)=10 → 0.
  Actually: offset=6, total=9, end=15
  → band 0-10: max(0, min(15,10) - max(6,0)) = max(0, 10-6) = 4  WAIT no.

  The soft rotary offset is the sum of phases BEFORE the first soft rotary phase.
  BH03 phases: [CP 6m, RC_NO_CORE_SOFT 9m]
  Soft rotary methods = {RC_CORE_SOFT, RC_NO_CORE_SOFT}
  First soft rotary is RC_NO_CORE_SOFT at index 1. Offset = 6 (CP phase before it).
  Total soft = 9. End = 6 + 9 = 15.
  Band 0-10: max(0, min(15,10) - max(6,0)) = max(0, 10 - 6) = 4
  Band 10-20: max(0, min(15,20) - max(6,10)) = max(0, 15 - 10) = 5

Expected CP band totals (H1.x)
------------------------------
BH01: [10, 2, 0, 0]; BH02: [8, 0, 0, 0]; BH03: [6, 0, 0, 0]
Total CP: [24, 2, 0, 0]
H1.1 = ceil(24/1) = 24
H1.2 = ceil(2/1) = 2
H1.3 = 0, H1.4 = 0

Expected soft rotary band totals (H2.x)
----------------------------------------
BH02 soft: offset=8, end=13 → [2, 3, 0, 0]
BH03 soft: offset=6, end=15 → [4, 5, 0, 0]
Total soft: [6, 8, 0, 0]
H2.1 = ceil(6/1.5) = 4
H2.2 = ceil(8/1.5) = ceil(5.33) = 6
H2.3 = 0, H2.4 = 0

Dynamic samples (for H3.1)
---------------------------
- DS01: 6m, DS02: 4m → H3.1 = 10

In-situ test mix
-----------------
- TP01: in_situ_tests={DCP, HV}
- TP02: in_situ_tests={BRE}
- IP01: in_situ_tests={DCP}
- TR01: in_situ_tests={HV}
- SK01: in_situ_tests={BRE, PT, DCP}

Expected totals
-H6 (DCP): TP01 + IP01 + SK01 = 3
-H9 (HV × 4): (TP01 + TR01) × 4 = 2 × 4 = 8
-H19 (BRE): TP02 + SK01 = 2
-H30 (PT): SK01 = 1
-H34 = 1 (has holes)
"""

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    InSituTest,
    InspectionPit,
    Project,
    SiteCategory,
    Soakaway,
    Trench,
    TrialPit,
)


def build_section_h_site() -> Project:
    return Project(
        name="Section H Test Site",
        site_address="8 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            # BH01: 12 m CP only
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=12.0)],
                total_schedule_depth_m=12.0,
            ),
            # BH02: 8 m CP + 5 m RC_CORE_SOFT
            Borehole(
                hole_number="BH02",
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=8.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_SOFT, depth_m=5.0),
                ],
                total_schedule_depth_m=13.0,
            ),
            # BH03: 6 m CP + 9 m RC_NO_CORE_SOFT
            Borehole(
                hole_number="BH03",
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=6.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_NO_CORE_SOFT, depth_m=9.0),
                ],
                total_schedule_depth_m=15.0,
            ),
        ],
        trial_pits=[
            TrialPit(
                trial_pit_number="TP01",
                schedule_depth_m=3.0,
                depth_m=3.0,
                in_situ_tests={InSituTest.DCP, InSituTest.HV},
            ),
            TrialPit(
                trial_pit_number="TP02",
                schedule_depth_m=2.0,
                depth_m=2.0,
                in_situ_tests={InSituTest.BRE},
            ),
        ],
        trenches=[
            Trench(
                trench_number="TR01",
                in_situ_tests={InSituTest.HV},
            ),
        ],
        inspection_pits=[
            InspectionPit(
                inspection_pit_number="IP01",
                scheduled_depth_m=1.5,
                recorded_depth_m=1.5,
                in_situ_tests={InSituTest.DCP},
            ),
        ],
        dynamic_samples=[
            DynamicSample(sample_number="DS01", depth_m=6.0),
            DynamicSample(sample_number="DS02", depth_m=4.0),
        ],
        soakaways=[
            Soakaway(
                soakaway_id="SK01",
                schedule_depth_m=3.0,
                in_situ_tests={InSituTest.BRE, InSituTest.PT, InSituTest.DCP},
            ),
        ],
    )
