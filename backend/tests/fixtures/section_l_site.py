"""Fixture: a project designed to exercise Section L computed items.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Hole mix and the "EV" count (Section E item E12)
------------------------------------------------
'Section E'!D25 counts holes whose test selection contains "EV":

- Trial pits       TP01 {DCP, EV} → 1    TP02 {DCP} → 0
- Inspection pits  IP01 {EV}      → 1
- Trenches         TR01 {EV}      → 1
- Boreholes        BH01 {EV}      → 1    BH02 {P}   → 0
- Dynamic samples  DS01 {EV}      → 1    DS02 {S, EV} → 1

E12 = 1 + 1 + 1 + 1 + 2 = 6
E16 = E12 = 6                      ('Section E'!D29: =D25)

Expected Section L quantities
-----------------------------
- L.1 = E12 / 5 = 6 / 5 = 1.2      ('Section L'!D11: ='Section E'!D25/5)
- L.5 = E16 / 5 = 6 / 5 = 1.2      ('Section L'!D15: ='Section E'!D29/5)
- L.2, L.3, L.4, L.6 = "Not Required"

TP02 and BH02 have tests selected but no "EV", to show they are not counted.
TP01 and DS02 combine "EV" with another selection, to show they count once.
The total (6) is deliberately not a multiple of 5, to show the result is not
rounded.
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

EXPECTED_L = {
    "L.1": 1.2,
    "L.2": "Not Required",
    "L.3": "Not Required",
    "L.4": "Not Required",
    "L.5": 1.2,
    "L.6": "Not Required",
}


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
            Borehole(
                hole_number="BH02",
                phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0)],
                total_schedule_depth_m=10.0,
                tests={PSEVTest.P},
            ),
        ],
        trial_pits=[
            TrialPit(
                trial_pit_number="TP01",
                schedule_depth_m=3.0,
                depth_m=3.0,
                in_situ_tests={InSituTest.DCP, InSituTest.EV},
            ),
            TrialPit(
                trial_pit_number="TP02",
                schedule_depth_m=3.0,
                depth_m=3.0,
                in_situ_tests={InSituTest.DCP},
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
            DynamicSample(
                sample_number="DS02",
                depth_m=5.0,
                tests={PSEVTest.S, PSEVTest.EV},
            ),
        ],
    )
