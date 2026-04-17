"""Fixture: a project designed to exercise every Section E branch.

Hole mix for sampling computations
-----------------------------------
- BH01: 12 m CP phase → total_cp_depth = 12
- BH02: 8 m CP + 5 m rotary → CP depth = 8, tests={EV}
- TP01: depth=3.0m, in_situ_tests={EV}
- TP02: depth=2.0m, in_situ_tests={}
- TR01: in_situ_tests={EV}  (Trenches!N93 is None → contributes 0 to E2)
- IP01: recorded_depth=1.5m, in_situ_tests={EV}
- IP02: recorded_depth=None (contributes 0)
- DS01: depth=6.0m, tests={EV}
- DS02: depth=4.0m, tests={}

Expected totals
---------------
- total_cp_depth = 12 + 8 = 20
- tp_depth_sum = 3.0 + 2.0 = 5.0
- trench_tub_count = 0 (Trenches!N93 = None)
- ip_depth_sum = 1.5 + 0 = 1.5
- ds_depth_sum = 6.0 + 4.0 = 10.0

- E2  = 20 + 5 + 0 + 1.5 + 10 = 36.5
- E3  = 36.5
- E4  = 36.5 / 10 = 3.65
- E5  = 20 / 5 = 4.0
- E6  = 4.0
- E8.1 = 20 / 10 = 2.0
- E8.2 = 2.0
- E12 = 4  (BH02 + TP01 + TR01 + IP01 + DS01 = 5 — wait, let me recount)
         BH02: PSEVTest.EV → 1
         TP01: InSituTest.EV → 1
         TR01: InSituTest.EV → 1
         IP01: InSituTest.EV → 1
         DS01: PSEVTest.EV → 1
         Total = 5
- E16 = 5
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
    PSEVTest,
    SiteCategory,
    Trench,
    TrialPit,
)


def build_section_e_site() -> Project:
    return Project(
        name="Section E Test Site",
        site_address="5 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            # BH01: 12 m CP, no EV
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=12.0)],
                total_schedule_depth_m=12.0,
            ),
            # BH02: 8 m CP + 5 m rotary, with EV test
            Borehole(
                hole_number="BH02",
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=8.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=5.0),
                ],
                total_schedule_depth_m=13.0,
                tests={PSEVTest.EV},
            ),
        ],
        trial_pits=[
            # TP01: depth=3.0m, with EV
            TrialPit(
                trial_pit_number="TP01",
                schedule_depth_m=3.0,
                depth_m=3.0,
                in_situ_tests={InSituTest.EV},
            ),
            # TP02: depth=2.0m, no EV
            TrialPit(
                trial_pit_number="TP02",
                schedule_depth_m=2.0,
                depth_m=2.0,
            ),
        ],
        trenches=[
            # TR01: with EV
            Trench(
                trench_number="TR01",
                in_situ_tests={InSituTest.EV},
            ),
        ],
        inspection_pits=[
            # IP01: recorded_depth=1.5m, with EV
            InspectionPit(
                inspection_pit_number="IP01",
                scheduled_depth_m=1.5,
                recorded_depth_m=1.5,
                in_situ_tests={InSituTest.EV},
            ),
            # IP02: no recorded depth
            InspectionPit(
                inspection_pit_number="IP02",
                scheduled_depth_m=2.0,
            ),
        ],
        dynamic_samples=[
            # DS01: depth=6.0m, with EV
            DynamicSample(
                sample_number="DS01",
                depth_m=6.0,
                tests={PSEVTest.EV},
            ),
            # DS02: depth=4.0m, no EV
            DynamicSample(
                sample_number="DS02",
                depth_m=4.0,
            ),
        ],
    )
