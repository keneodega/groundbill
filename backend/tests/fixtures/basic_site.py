"""Fixture: a representative mixed-hole project for BOQ engine tests.

Counts: 3 boreholes + 2 trial pits + 1 trench + 1 CPT + 1 dynamic sample.
Expected A8 set-out points = 3 + 2 + (0 * 2) + 0 + 0 + 1 + 1 + 0 = 7.
The trench ST01 has no recorded depth, so Trenches!K (=IF(J3>0,1,0)) is 0
and it is not yet set out.
"""

from groundbill.models import (
    CPT,
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    InSituTest,
    Project,
    SiteCategory,
    Trench,
    TrialPit,
)


def build_basic_site() -> Project:
    return Project(
        name="Basic Test Site",
        site_address="1 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            Borehole(
                hole_number=f"BH0{i}",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0)],
                total_schedule_depth_m=10.0,
            )
            for i in range(1, 4)
        ],
        trial_pits=[
            TrialPit(
                trial_pit_number=f"TP0{i}",
                schedule_depth_m=3.0,
                in_situ_tests={InSituTest.DCP},
            )
            for i in range(1, 3)
        ],
        trenches=[
            Trench(trench_number="ST01"),
        ],
        cpts=[
            CPT(cpt_number="CPT01", depth_m=20.0),
        ],
        dynamic_samples=[
            DynamicSample(sample_number="DS01", depth_m=6.0),
        ],
    )
