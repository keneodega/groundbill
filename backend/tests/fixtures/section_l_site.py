"""Fixture: a project designed to exercise Section L computed items.

Reuses the same EV-test structure as Section E to produce the same E12 value.

Hole mix
--------
- BH01: tests={EV} → ev_count += 1
- TP01: in_situ_tests={EV} → ev_count += 1
- TR01: in_situ_tests={EV} → ev_count += 1
- IP01: in_situ_tests={EV} → ev_count += 1
- DS01: tests={EV} → ev_count += 1

Expected totals
---------------
- ev_count = 5
- L.1 = 5 / 5 = 1.0
- L.5 = 1.0
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


def build_section_l_site() -> Project:
    return Project(
        name="Section L Test Site",
        site_address="12 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            Borehole(
                hole_number="BH01",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0)],
                total_schedule_depth_m=10.0,
                tests={PSEVTest.EV},
            ),
        ],
        trial_pits=[
            TrialPit(
                trial_pit_number="TP01",
                schedule_depth_m=3.0,
                depth_m=3.0,
                in_situ_tests={InSituTest.EV},
            ),
        ],
        trenches=[
            Trench(
                trench_number="TR01",
                in_situ_tests={InSituTest.EV},
            ),
        ],
        inspection_pits=[
            InspectionPit(
                inspection_pit_number="IP01",
                scheduled_depth_m=1.5,
                recorded_depth_m=1.5,
                in_situ_tests={InSituTest.EV},
            ),
        ],
        dynamic_samples=[
            DynamicSample(
                sample_number="DS01",
                depth_m=5.0,
                tests={PSEVTest.EV},
            ),
        ],
    )
