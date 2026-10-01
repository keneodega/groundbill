"""Fixture: a project designed to exercise every Section H formula.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Boreholes — metres per 10 m band (0-10 / 10-20 / 20-30)
-------------------------------------------------------
=====  ==========================================  ==========  ============
Hole   Phases (from the surface down)              CP (N:P)    Soft rotary
=====  ==========================================  ==========  ============
BH01   12 m CP                                     10, 2, 0    -
BH02   8 m CP, then 5 m with core, soft (8-13)     8, 0, 0     AQ: 2, 3, 0
BH03   6 m CP, then 9 m no core, soft (6-15)       6, 0, 0     BA: 4, 5, 0
BH04   25 m CP, then 5 m with core, hard (25-30)   10, 10, 5   - (hard strata)
BH05   24 m no core, soft (0-24)                   -           BA: 10, 10, 4
=====  ==========================================  ==========  ============

- Boreholes!N92 = 10 + 8 + 6 + 10 = 34     O92 = 2 + 10 = 12     P92 = 5
- AQ92 + BA92 = 2 + (4 + 10) = 16          AR92 + BB92 = 3 + (5 + 10) = 18
  AS92 + BC92 = 0 + 4 = 4

Standard penetration tests:

- H1.1 =N92                       = 34
- H1.2 =O92                       = 12
- H1.3 =P92                       = 5
- H2.1 =ROUNDUP(16/1.5,0)         = ROUNDUP(10.67) = 11
- H2.2 =ROUNDUP(18/1.5,0)         = ROUNDUP(12.00) = 12
- H2.3 =ROUNDUP(4/1.5,0)          = ROUNDUP(2.67)  = 3
- H3.1 ='Dynamic Sampling'!C92    = 6 + 4 = 10   (DS01 6 m, DS02 4 m)

BH04's rotary coring is in hard strata, which no SPT formula reads.

In situ tests in pits and trenches
----------------------------------
=====  ==================
Hole   Tests selected
=====  ==================
TP01   DCP/HV
TP02   BRE
TP03   HV/PT
TP04   (none)
IP01   DCP
IP02   HV
TR01   HV
TR02   DCP/PT
SK01   DCP/BRE/PT
SK02   BRE
=====  ==================

- H6  "DCP": pits 1 (TP01) + inspection pits 1 (IP01) + trenches 1 (TR02) = 3
  (SK01 is not counted: the formula does not read the Soakaway sheet)
- H9  "HV":  pits 2 (TP01, TP03) × 4 + inspection pits 1 (IP02) + trenches 1 (TR01)
  = 8 + 1 + 1 = 10
- H19 "BRE": pits 1 (TP02) + inspection pits 0 + trenches 0 + soakaways 2 = 3
- H23 =D43 = 3;  H25 =D47 = 3;  H26 =D49 = 3
- H30 "PT":  pits 1 (TP03) + inspection pits 0 + trenches 1 (TR02) = 2
  (SK01 is not counted)
- H34 =IF(D56>0,1,"Not Required") = 1

All other Section H items are "Not Required".
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

# Computed items only; every other item is "Not Required".
EXPECTED_H_COMPUTED = {
    "H1.1": 34.0,
    "H1.2": 12.0,
    "H1.3": 5.0,
    "H2.1": 11,
    "H2.2": 12,
    "H2.3": 3,
    "H3.1": 10.0,
    "H6": 3,
    "H9": 10,
    "H19": 3,
    "H23": 3,
    "H25": 3,
    "H26": 3,
    "H30": 2,
    "H34": 1,
}

_CP = DrillingMethod.CABLE_PERCUSSION


def _borehole(number: str, *phases: tuple[DrillingMethod, float]) -> Borehole:
    return Borehole(
        hole_number=number,
        phases=[DrillingPhase(method=m, depth_m=d) for m, d in phases],
        total_schedule_depth_m=sum(d for _, d in phases),
    )


def build_section_h_site() -> Project:
    return Project(
        name="Section H Test Site",
        site_address="8 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            _borehole("BH01", (_CP, 12.0)),
            _borehole("BH02", (_CP, 8.0), (DrillingMethod.ROTARY_CORE_SOFT, 5.0)),
            _borehole("BH03", (_CP, 6.0), (DrillingMethod.ROTARY_NO_CORE_SOFT, 9.0)),
            _borehole("BH04", (_CP, 25.0), (DrillingMethod.ROTARY_CORE_HARD, 5.0)),
            _borehole("BH05", (DrillingMethod.ROTARY_NO_CORE_SOFT, 24.0)),
        ],
        dynamic_samples=[
            DynamicSample(sample_number="DS01", depth_m=6.0),
            DynamicSample(sample_number="DS02", depth_m=4.0),
        ],
        trial_pits=[
            TrialPit(
                trial_pit_number="TP01",
                schedule_depth_m=3.0,
                in_situ_tests={InSituTest.DCP, InSituTest.HV},
            ),
            TrialPit(trial_pit_number="TP02", schedule_depth_m=3.0, in_situ_tests={InSituTest.BRE}),
            TrialPit(
                trial_pit_number="TP03",
                schedule_depth_m=3.0,
                in_situ_tests={InSituTest.HV, InSituTest.PT},
            ),
            TrialPit(trial_pit_number="TP04", schedule_depth_m=3.0),
        ],
        inspection_pits=[
            InspectionPit(
                inspection_pit_number="IP01", scheduled_depth_m=1.2, in_situ_tests={InSituTest.DCP}
            ),
            InspectionPit(
                inspection_pit_number="IP02", scheduled_depth_m=1.2, in_situ_tests={InSituTest.HV}
            ),
        ],
        trenches=[
            Trench(trench_number="TR01", in_situ_tests={InSituTest.HV}),
            Trench(trench_number="TR02", in_situ_tests={InSituTest.DCP, InSituTest.PT}),
        ],
        soakaways=[
            Soakaway(
                soakaway_id="SK01",
                schedule_depth_m=2.0,
                in_situ_tests={InSituTest.DCP, InSituTest.BRE, InSituTest.PT},
            ),
            Soakaway(soakaway_id="SK02", schedule_depth_m=2.0, in_situ_tests={InSituTest.BRE}),
        ],
    )
