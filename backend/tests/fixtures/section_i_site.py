"""Fixture: a project designed to exercise every Section I formula.

Expected values are derived by hand from the Calculator formulas (the Log
Tracker in `reference/excel/` is an empty template, so there are no
Excel-calculated outputs to copy).

Boreholes
---------
=====  ====  ==========  =========  =========  =========  ==========  ==
Hole   ROAD  Piezometer  Plain      Standpipe  Plain      Slotted     BP
       (BH)  (BI)        (BJ)       (BL)       (BM)       (BN)
=====  ====  ==========  =========  =========  =========  ==========  ==
BH01   YES   YES         8.0        -          -          -           1
BH02   NO    -           -          YES        3.0        6.0         1
BH03   NO    YES         5.0        YES        2.0        4.0         1
BH04   YES   -           -          -          -          -           0
BH05   NO    -           -          -          1.5        -           0
=====  ====  ==========  =========  =========  =========  ==========  ==
Totals                   BJ92 13.0             BM92 6.5   BN92 10.0

BH03 has both a piezometer and a standpipe. BH04 is on a road but has no
installation. BH05 has a standpipe plain depth entered without the YES flag:
its metres are measured (totals row) and it counts in I9 (BM > 0), but it has
no cover because BP = 0.

Dynamic sampling holes
----------------------
=====  ========  =============  =========  ===========  =
Hole   ROAD (I)  Standpipe (K)  Plain (L)  Slotted (M)  O
=====  ========  =============  =========  ===========  =
DS01   YES       YES            1.0        3.0          1
DS02   NO        YES            1.5        2.5          1
DS03   NO        -              -          -            0
=====  ========  =============  =========  ===========  =
Totals                          L92 2.5    M92 5.5

Counts: piezometers (BI) = 2; borehole standpipes (BL) = 2; dynamic sampling
standpipes (K) = 2.

Expected Section I quantities
-----------------------------
- I1  =BJ92 + BM92 + L92          = 13.0 + 6.5 + 2.5 = 22.0
- I2  =COUNTIF(BI) + COUNTIF(K)   = 2 + 2 = 4
- I3  =D12                        = 4
- I4  =BJ92                       = 13.0
- I5  =COUNTIF(BI) × 1            = 2
- I6  =BN92 + M92                 = 10.0 + 5.5 = 15.5
- I7  =D16                        = 15.5
- I8  =BM92 + L92                 = 6.5 + 2.5 = 9.0
- I9  =COUNTIF(BM > 0) + COUNTIF(O > 0) = 3 (BH02, BH03, BH05) + 2 = 5
- I14 =(2 + 2 + 2) × 2            = 12
- I16 ROAD "YES" and complete     = 1 (BH01) + 1 (DS01) = 2
- I17 ROAD "NO" and complete      = 2 (BH02, BH03) + 1 (DS02) = 3
- I19 =D27                        = 3
- I20 =D27                        = 3

All other Section I items are "Not Required".
"""

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    DynamicSample,
    Project,
    SiteCategory,
)

# Computed items only; every other item is "Not Required".
EXPECTED_I_COMPUTED = {
    "I1": 22.0,
    "I2": 4,
    "I3": 4,
    "I4": 13.0,
    "I5": 2,
    "I6": 15.5,
    "I7": 15.5,
    "I8": 9.0,
    "I9": 5,
    "I14": 12,
    "I16": 2,
    "I17": 3,
    "I19": 3,
    "I20": 3,
}


def _borehole(number: str, **kwargs) -> Borehole:
    return Borehole(
        hole_number=number,
        phases=[DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0)],
        total_schedule_depth_m=10.0,
        **kwargs,
    )


def build_section_i_site() -> Project:
    return Project(
        name="Section I Test Site",
        site_address="9 Test Road, Dublin",
        contract_route=ContractRoute.PRIVATE,
        site_category=SiteCategory.GREEN,
        boreholes=[
            _borehole("BH01", on_road=True, piezometer=True, piezometer_plain_depth_m=8.0),
            _borehole(
                "BH02",
                standpipe=True,
                standpipe_plain_depth_m=3.0,
                standpipe_slotted_depth_m=6.0,
            ),
            _borehole(
                "BH03",
                piezometer=True,
                piezometer_plain_depth_m=5.0,
                standpipe=True,
                standpipe_plain_depth_m=2.0,
                standpipe_slotted_depth_m=4.0,
            ),
            _borehole("BH04", on_road=True),
            _borehole("BH05", standpipe_plain_depth_m=1.5),
        ],
        dynamic_samples=[
            DynamicSample(
                sample_number="DS01",
                depth_m=4.0,
                on_road=True,
                standpipe=True,
                plain_depth_m=1.0,
                slotted_depth_m=3.0,
            ),
            DynamicSample(
                sample_number="DS02",
                depth_m=4.0,
                standpipe=True,
                plain_depth_m=1.5,
                slotted_depth_m=2.5,
            ),
            DynamicSample(sample_number="DS03", depth_m=4.0),
        ],
    )
