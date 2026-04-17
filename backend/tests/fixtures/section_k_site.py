"""Fixture: a project designed to exercise Section K computed items.

Reuses the same hole structure as Section E to produce the same E2 value.

Hole mix
--------
- BH01: 12 m CP
- BH02: 8 m CP + 5 m rotary
- TP01: depth=3.0m
- TP02: depth=2.0m
- IP01: recorded_depth=1.5m
- IP02: recorded_depth=None (contributes 0)
- DS01: depth=6.0m
- DS02: depth=4.0m

Expected totals
---------------
- total_cp_depth = 12 + 8 = 20
- tp_depth_sum = 3 + 2 = 5
- ip_depth_sum = 1.5
- ds_depth_sum = 6 + 4 = 10

- K1.1 (= E2) = 20 + 5 + 1.5 + 10 = 36.5
- K1.2 = 0.5 × 36.5 = 18.25
- K1.9 = 0.25 × 36.5 = 9.125
- K1.12 = 0.25 × 36.5 = 9.125
"""

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    InspectionPit,
    Project,
    SiteCategory,
    TrialPit,
)


def build_section_k_site() -> Project:
    return Project(
        name="Section K Test Site",
        site_address="11 Test Road, Dublin",
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
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=8.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=5.0),
                ],
                total_schedule_depth_m=13.0,
            ),
        ],
        trial_pits=[
            TrialPit(trial_pit_number="TP01", schedule_depth_m=3.0, depth_m=3.0),
            TrialPit(trial_pit_number="TP02", schedule_depth_m=2.0, depth_m=2.0),
        ],
        inspection_pits=[
            InspectionPit(
                inspection_pit_number="IP01",
                scheduled_depth_m=1.5,
                recorded_depth_m=1.5,
            ),
            InspectionPit(
                inspection_pit_number="IP02",
                scheduled_depth_m=2.0,
            ),
        ],
        dynamic_samples=[
            DynamicSample(sample_number="DS01", depth_m=6.0),
            DynamicSample(sample_number="DS02", depth_m=4.0),
        ],
    )
