"""Fixture: a project designed to exercise every Section E formula.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Hole mix
--------
- BH01  12 m cable percussion                      tests: none
- BH02  8 m cable percussion + 5 m rotary coring   tests: EV
- TP01  recorded depth 3.0 m                       tests: EV
- TP02  recorded depth 2.0 m                       tests: none
- TR01  5.0 m x 0.6 m x 1.5 m deep (paved)         tests: EV
- IP01  recorded depth 1.5 m                       tests: EV
- IP02  no recorded depth                          tests: none
- DS01  depth 6.0 m                                tests: EV
- DS02  depth 4.0 m                                tests: none

Log Tracker totals
------------------
- Boreholes!K92 (CP drilling total depth)   = 12 + 8        = 20
  (BH02's 5 m of rotary drilling is not cable percussion, so not counted)
- 'Trial Pits'!M92 (depth)                  = 3.0 + 2.0     = 5.0
- Trenches!N93                              = 0
  (empty cell in the Log Tracker — open item; TR01 has real dimensions to
  show that trenches contribute nothing)
- 'Inspection pit'!E92 (recorded depth)     = 1.5 + blank   = 1.5
- 'Dynamic Sampling'!C92 (depth)            = 6.0 + 4.0     = 10.0

Expected Section E quantities
-----------------------------
- E2   =SUM(K92, M92, N93, E92) + C92 = 20 + 5.0 + 0 + 1.5 + 10.0 = 36.5
- E3   =D12                           = 36.5
- E4   =D12/10        = 36.5 / 10     = 3.65
- E5   =K92/5         = 20 / 5        = 4.0
- E6   =D15                           = 4.0
- E8.1 =K92/10        = 20 / 10       = 2.0
- E8.2 =K92/10        = 20 / 10       = 2.0
- E9   blank cell                     = None
- E12  holes with "EV": TP01, IP01, TR01, BH02, DS01 = 5
- E16  =D25                           = 5
- E1, E7, E8.3, E10, E11, E13, E14, E15, E17 = "Not Required"
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

EXPECTED_E = {
    "E1": "Not Required",
    "E2": 36.5,
    "E3": 36.5,
    "E4": 3.65,
    "E5": 4.0,
    "E6": 4.0,
    "E7": "Not Required",
    "E8.1": 2.0,
    "E8.2": 2.0,
    "E8.3": "Not Required",
    "E9": None,
    "E10": "Not Required",
    "E11": "Not Required",
    "E12": 5,
    "E13": "Not Required",
    "E14": "Not Required",
    "E15": "Not Required",
    "E16": 5,
    "E17": "Not Required",
}


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
            # TR01: with EV; real dimensions, which E2 nevertheless ignores (Trenches!N93 is empty)
            Trench(
                trench_number="TR01",
                paved=True,
                in_situ_tests={InSituTest.EV},
                overall_length_m=5.0,
                overall_width_m=0.6,
                overall_total_depth_m=1.5,
                paved_length_m=5.0,
                paved_width_m=0.6,
                paved_depth_m=1.5,
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
