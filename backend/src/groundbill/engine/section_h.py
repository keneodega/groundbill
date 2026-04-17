"""Section H — In-situ Testing.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section H'
(with cross-references to the Log Tracker workbook's `Boreholes`, `Trial Pits`,
`Trenches`, `Inspection pit`, `Dynamic Sampling`, and `Soakaway (BRE)` sheets).

Key formulas
============
H1.1–H1.4  SPT counts from CP depth bands (ROUNDUP(band / 1) per 10 m band)
H2.1–H2.4  Rotary SPT counts from RC_CORE_SOFT + RC_NO_CORE_SOFT bands
            (ROUNDUP(band / 1.5) per 10 m band)
H3.1       Dynamic sampling depth sum
H6         DCP test count across TPs, IPs, trenches, soakaways
H9         Hand vane count across TPs, IPs, trenches (× 4 per hole)
H19        BRE soakaway test count across TPs, IPs, trenches, soakaways
H30        Permeability test count across TPs, IPs, trenches, soakaways
H34        Factual/interpretive report: 1 if project has any holes, else 0

CP SPT computation
------------------
Reuses the same CP-band clipping logic as Section B: sum across all boreholes'
CP phases, clip into 10 m bands, then ROUNDUP(band ÷ 1).

Rotary SPT computation
----------------------
Sums RC_CORE_SOFT + RC_NO_CORE_SOFT band depths per 10 m band, then
ROUNDUP(band ÷ 1.5).
"""

import math

from groundbill.models import DrillingMethod, InSituTest, Project

from .boq_items import BoqItem

_CP = DrillingMethod.CABLE_PERCUSSION
_SOFT_ROTARY = {DrillingMethod.ROTARY_CORE_SOFT, DrillingMethod.ROTARY_NO_CORE_SOFT}
_DEPTH_BANDS_10M = ((0.0, 10.0), (10.0, 20.0), (20.0, 30.0), (30.0, 40.0))


def compute_section_h(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section H BOQ items for the given project."""

    # --- CP SPT bands (H1.1–H1.4) ---
    cp_bands = [0.0, 0.0, 0.0, 0.0]
    for bh in project.boreholes:
        for i, metres in enumerate(_phase_band_distribution(bh, {_CP})):
            cp_bands[i] += metres
    h1_1 = math.ceil(cp_bands[0]) if cp_bands[0] > 0 else 0
    h1_2 = math.ceil(cp_bands[1]) if cp_bands[1] > 0 else 0
    h1_3 = math.ceil(cp_bands[2]) if cp_bands[2] > 0 else 0
    h1_4 = math.ceil(cp_bands[3]) if cp_bands[3] > 0 else 0

    # --- Rotary SPT bands (H2.1–H2.4) ---
    # Sum RC_CORE_SOFT and RC_NO_CORE_SOFT across all boreholes
    rc_soft_bands = [0.0, 0.0, 0.0, 0.0]
    for bh in project.boreholes:
        for i, metres in enumerate(_phase_band_distribution(bh, _SOFT_ROTARY)):
            rc_soft_bands[i] += metres
    h2_1 = math.ceil(rc_soft_bands[0] / 1.5) if rc_soft_bands[0] > 0 else 0
    h2_2 = math.ceil(rc_soft_bands[1] / 1.5) if rc_soft_bands[1] > 0 else 0
    h2_3 = math.ceil(rc_soft_bands[2] / 1.5) if rc_soft_bands[2] > 0 else 0
    h2_4 = math.ceil(rc_soft_bands[3] / 1.5) if rc_soft_bands[3] > 0 else 0

    # --- H3.1: DS depth sum ---
    h3_1 = sum(ds.depth_m for ds in project.dynamic_samples)

    # --- In-situ test counting helpers ---
    tp_tests = [tp.in_situ_tests for tp in project.trial_pits]
    ip_tests = [ip.in_situ_tests for ip in project.inspection_pits]
    tr_tests = [t.in_situ_tests for t in project.trenches]
    sk_tests = [s.in_situ_tests for s in project.soakaways]

    # H6: DCP count (TPs + IPs + trenches + soakaways)
    h6 = (
        sum(1 for ts in tp_tests if InSituTest.DCP in ts)
        + sum(1 for ts in ip_tests if InSituTest.DCP in ts)
        + sum(1 for ts in tr_tests if InSituTest.DCP in ts)
        + sum(1 for ts in sk_tests if InSituTest.DCP in ts)
    )

    # H9: Hand vane count (TPs + IPs + trenches) × 4 per hole
    h9 = (
        sum(1 for ts in tp_tests if InSituTest.HV in ts)
        + sum(1 for ts in ip_tests if InSituTest.HV in ts)
        + sum(1 for ts in tr_tests if InSituTest.HV in ts)
    ) * 4

    # H19: BRE soakaway test (TPs + IPs + trenches + soakaways)
    h19 = (
        sum(1 for ts in tp_tests if InSituTest.BRE in ts)
        + sum(1 for ts in ip_tests if InSituTest.BRE in ts)
        + sum(1 for ts in tr_tests if InSituTest.BRE in ts)
        + sum(1 for ts in sk_tests if InSituTest.BRE in ts)
    )

    # H30: Permeability test (TPs + IPs + trenches + soakaways)
    h30 = (
        sum(1 for ts in tp_tests if InSituTest.PT in ts)
        + sum(1 for ts in ip_tests if InSituTest.PT in ts)
        + sum(1 for ts in tr_tests if InSituTest.PT in ts)
        + sum(1 for ts in sk_tests if InSituTest.PT in ts)
    )

    # H34: Factual/interpretive report — 1 if project has any holes
    has_holes = bool(
        project.boreholes
        or project.trial_pits
        or project.trenches
        or project.inspection_pits
        or project.dynamic_samples
        or project.soakaways
        or project.dynamic_probes
        or project.cpts
    )
    h34 = 1 if has_holes else 0

    return [
        BoqItem(
            code="H1.1",
            description="Standard penetration test (SPT) in cable percussion borehole 0–10 m",
            unit="nr",
            quantity=h1_1,
        ),
        BoqItem(
            code="H1.2",
            description="As Item H1.1 but between 10 m and 20 m depth",
            unit="nr",
            quantity=h1_2,
        ),
        BoqItem(
            code="H1.3",
            description="As Item H1.1 but between 20 m and 30 m depth",
            unit="nr",
            quantity=h1_3,
        ),
        BoqItem(
            code="H1.4",
            description="As Item H1.1 but between 30 m and 40 m depth",
            unit="nr",
            quantity=h1_4,
        ),
        BoqItem(
            code="H2.1",
            description="Standard penetration test (SPT) in rotary borehole 0–10 m",
            unit="nr",
            quantity=h2_1,
        ),
        BoqItem(
            code="H2.2",
            description="As Item H2.1 but between 10 m and 20 m depth",
            unit="nr",
            quantity=h2_2,
        ),
        BoqItem(
            code="H2.3",
            description="As Item H2.1 but between 20 m and 30 m depth",
            unit="nr",
            quantity=h2_3,
        ),
        BoqItem(
            code="H2.4",
            description="As Item H2.1 but between 30 m and 40 m depth",
            unit="nr",
            quantity=h2_4,
        ),
        BoqItem(
            code="H3.1",
            description="Dynamic sampling — depth of sampling",
            unit="m",
            quantity=h3_1,
        ),
        BoqItem(
            code="H4",
            description="Plate loading test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H5",
            description="California bearing ratio (CBR) test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H6",
            description="Dynamic cone penetrometer (DCP) test",
            unit="nr",
            quantity=h6,
        ),
        BoqItem(
            code="H7",
            description="Mackintosh probe",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H8",
            description="Pocket penetrometer test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H9",
            description="Hand vane test",
            unit="nr",
            quantity=h9,
        ),
        BoqItem(
            code="H10",
            description="In-situ density test (sand replacement)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H11",
            description="In-situ density test (nuclear gauge)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H12",
            description="In-situ redox potential test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H13",
            description="In-situ resistivity test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H14",
            description="In-situ pH test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H15",
            description="Pressuremeter test (self-boring)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H16",
            description="Pressuremeter test (high pressure dilatometer)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H17",
            description="Pressuremeter test (Ménard type)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H18",
            description="Flat dilatometer test (DMT)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H19",
            description="BRE soakaway test",
            unit="nr",
            quantity=h19,
        ),
        BoqItem(
            code="H20",
            description="Falling head permeability test in borehole",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H21",
            description="Rising head permeability test in borehole",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H22",
            description="Packer (Lugeon) test in borehole",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H23",
            description="Pumping test — exploratory well",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H24",
            description="Pumping test — observation well",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H25",
            description="Pumping test — constant rate",
            unit="h",
            quantity="Not Required",
        ),
        BoqItem(
            code="H26",
            description="Pumping test — step drawdown",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H27",
            description="Pumping test — recovery",
            unit="h",
            quantity="Not Required",
        ),
        BoqItem(
            code="H28",
            description="Pumping test — water disposal",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="H29",
            description="Pumping test — factual report",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H30",
            description="Permeability test in trial pit or trench",
            unit="nr",
            quantity=h30,
        ),
        BoqItem(
            code="H31",
            description="Infiltration test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H32",
            description="Variable head permeability test in standpipe piezometer",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H33",
            description="Borehole geophysical logging",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H34",
            description="Factual and interpretive in-situ testing report",
            unit="nr",
            quantity=h34,
        ),
        BoqItem(
            code="H35",
            description="CCTV survey of borehole",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H36",
            description="Inclinometer survey",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H37",
            description="Extensometer reading",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H38",
            description="Vibrating wire piezometer reading",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H39",
            description="Settlement gauge reading",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="H40",
            description="Additional in-situ test (to be specified)",
            unit="nr",
            quantity="Not Required",
        ),
    ]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _phase_band_distribution(borehole, methods: set) -> list[float]:
    """Return total metreage for *methods* split across 0-10/10-20/20-30/30-40 bands.

    Phases are assumed to run sequentially from the surface. The segment's
    start offset is the sum of all phases before the first occurrence of any
    method in *methods*; total depth is the sum of all matching phases.
    """
    offset = 0.0
    found = False
    total = 0.0
    for phase in borehole.phases:
        if phase.method in methods:
            found = True
            total += phase.depth_m
        elif not found:
            offset += phase.depth_m
    if total == 0.0:
        return [0.0, 0.0, 0.0, 0.0]
    end = offset + total
    return [
        max(0.0, min(end, band_end) - max(offset, band_start))
        for band_start, band_end in _DEPTH_BANDS_10M
    ]
