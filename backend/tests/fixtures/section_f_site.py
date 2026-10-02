"""Fixture: a project designed to exercise every Section F formula.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Dynamic probes (DPH sheet)
--------------------------
Band columns: D = IF(C>5,5,C); E = IF(C>10,5,MAX(0,C-5)); F = IF(C>15,5,MAX(0,C-10)).

======  =====  =====  =======  ========  =========
Probe   Depth  Slope  D (0-5)  E (5-10)  F (10-15)
======  =====  =====  =======  ========  =========
DP01     4 m   no        4        0         0
DP02    12 m   YES       5        5         2
DP03    17 m   no        5        5         5
======  =====  =====  =======  ========  =========
Totals                  14       10         7

DP03 runs to 17 m; the 2 m below 15 m falls outside every band, as in the
workbook.

- F1 =DPH!H122                   = 3 probes
- F2 =COUNTIF(DPH!B,"YES")       = 1   (DP02)
- F3 =DPH!D122                   = 4 + 5 + 5 = 14
- F4 =DPH!E122                   = 0 + 5 + 5 = 10
- F5 =DPH!F122                   = 0 + 2 + 5 = 7
- F6 =D11/2                      = 3 / 2 = 1.5

Cone penetration tests (CPT sheet)
----------------------------------
Band columns: F = IF(D>10,10,D); G = IF(D>20,10,MAX(0,D-10));
H = IF(D>30,10,MAX(0,D-20)); I = IF(D>40,10,MAX(0,D-30)).

=====  =====  =====  =========  ========  =========  =========  =========
CPT    Depth  Slope  Piezocone  F (0-10)  G (10-20)  H (20-30)  I (30-40)
=====  =====  =====  =========  ========  =========  =========  =========
CPT01   8 m   no     no            8         0          0          0
CPT02  22 m   YES    no           10        10          2          0
CPT03  15 m   no     YES          10         5          0          0
CPT04  45 m   YES    no           10        10         10         10
CPT05   5 m   no     no            5         0          0          0
=====  =====  =====  =========  ========  =========  =========  =========
Totals                            43        25         12         10

CPT04 runs to 45 m; the 5 m below 40 m falls outside every band. CPT03 is a
piezocone test, which no Calculator formula reads, so it is counted like any
other CPT.

- F8  =CPT!K92                   = 5 CPTs
- F9  =COUNTIF(CPT!B,"YES")      = 2   (CPT02, CPT04)
- F10 =CPT!F92                   = 8 + 10 + 10 + 10 + 5 = 43
- F11 =CPT!G92                   = 0 + 10 + 5 + 10 + 0  = 25
- F12 =CPT!H92                   = 0 + 2 + 0 + 10 + 0   = 12
- F13 =CPT!I92                   = 0 + 0 + 0 + 10 + 0   = 10
- F18 =D19/2                     = 5 / 2 = 2.5

F7, F14-F17 and F19-F22 are "Not Required".
"""

from groundbill.models import (
    CPT,
    ContractRoute,
    DynamicProbe,
    Project,
    SiteCategory,
)

EXPECTED_F = {
    "F1": 3,
    "F2": 1,
    "F3": 14.0,
    "F4": 10.0,
    "F5": 7.0,
    "F6": 1.5,
    "F7": "Not Required",
    "F8": 5,
    "F9": 2,
    "F10": 43.0,
    "F11": 25.0,
    "F12": 12.0,
    "F13": 10.0,
    "F14": "Not Required",
    "F15": "Not Required",
    "F16": "Not Required",
    "F17": "Not Required",
    "F18": 2.5,
    "F19": "Not Required",
    "F20": "Not Required",
    "F21": "Not Required",
    "F22": "Not Required",
}


def build_section_f_site() -> Project:
    return Project(
        name="Section F Test Site",
        site_address="6 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        dynamic_probes=[
            DynamicProbe(probe_number="DP01", depth_m=4.0),
            DynamicProbe(probe_number="DP02", depth_m=12.0, slope_over_20pct=True),
            DynamicProbe(probe_number="DP03", depth_m=17.0),
        ],
        cpts=[
            CPT(cpt_number="CPT01", depth_m=8.0),
            CPT(cpt_number="CPT02", depth_m=22.0, slope_over_20pct=True),
            CPT(cpt_number="CPT03", depth_m=15.0, piezocone=True),
            CPT(cpt_number="CPT04", depth_m=45.0, slope_over_20pct=True),
            CPT(cpt_number="CPT05", depth_m=5.0),
        ],
    )
