"""Fixture: a project designed to exercise Section K's computed items.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Hole mix (the same depths as the Section E fixture, so E2 is the same)
----------------------------------------------------------------------
- BH01  12 m cable percussion
- BH02  8 m cable percussion + 5 m rotary coring
- TP01  recorded depth 3.0 m
- TP02  recorded depth 2.0 m
- IP01  recorded depth 1.5 m
- IP02  no recorded depth
- DS01  depth 6.0 m
- DS02  depth 4.0 m

Tub sample count (Section E item E2)
------------------------------------
'Section E'!D12 = CP metres + trial pit depths + trenches + inspection pit
depths + dynamic sampling depths
= (12 + 8) + (3.0 + 2.0) + 0 + 1.5 + (6.0 + 4.0) = 36.5

Expected Section K quantities
-----------------------------
- K1.1  ='Section E'!D12        = 36.5
- K1.2  =0.5*(D11)   = 0.5 × 36.5  = 18.25
- K1.9  =0.25*(D11)  = 0.25 × 36.5 = 9.125
- K1.12 =0.25*(D11)  = 0.25 × 36.5 = 9.125

29 items have a blank quantity (``None``); the remaining 76 are
"Not Required".
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

EXPECTED_K_COMPUTED = {
    "K1.1": 36.5,
    "K1.2": 18.25,
    "K1.9": 9.125,
    "K1.12": 9.125,
}

# Items whose quantity cell is empty in the Calculator.
EXPECTED_K_BLANK = (
    ["K2.1", "K2.3", "K2.4", "K2.5", "K2.8", "K2.12"]
    + ["K3.1", "K3.3", "K3.6", "K3.7", "K3.9.1"]
    + ["K4.1", "K4.2"]
    + [f"K6.{n}" for n in range(1, 11)]
    + ["K6.15", "K6.17"]
    + ["K7.1", "K7.3"]
    + ["K8.14", "K8.18"]
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
