"""Section C — Rotary Drilling.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section C'
(with cross-references to the Log Tracker workbook's `Boreholes` sheet).

Borehole classification for Section C
--------------------------------------
- ``"CP/RC"`` — has at least one CP phase AND at least one rotary phase.
- ``"RC"``    — has at least one rotary phase AND no CP phase.
- Boreholes with only CP phases do not appear in Section C.

Depth-band distribution
-----------------------
Items C21–C24, C27–C30, C34–C37, C41–C44 split rotary metreage by method
into 10 m bands (0-10, 10-20, 20-30, 30-40). Each rotary method occupies a
contiguous segment starting after all preceding phases. The segment [start,
end] is clipped against each band exactly as Section B does for CP phases.

Open items for review (by Havilah)
----------------------------------
- C18 ("Break out obstructions...") uses the same
  ``COUNTIF(Boreholes!$BH$2:$BH91, "YES") * 0.125`` formula as B3.1.
  Column BH is the free-text 'ROAD' column. Translated literally pending
  confirmation of the intended source column.
"""

from groundbill.models import Borehole, DrillingMethod, Project

from .boq_items import BoqItem

_CP = DrillingMethod.CABLE_PERCUSSION
_ROTARY_METHODS = {
    DrillingMethod.ROTARY_CORE_HARD,
    DrillingMethod.ROTARY_NO_CORE_HARD,
    DrillingMethod.ROTARY_CORE_SOFT,
    DrillingMethod.ROTARY_NO_CORE_SOFT,
}

_DEPTH_BANDS_10M = ((0.0, 10.0), (10.0, 20.0), (20.0, 30.0), (30.0, 40.0))


def compute_section_c(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section C BOQ items for the given project."""

    cp_rc = [b for b in project.boreholes if _drilling_type(b) == "CP/RC"]
    rc_only = [b for b in project.boreholes if _drilling_type(b) == "RC"]
    all_rotary = cp_rc + rc_only

    # C15.1.1: CP/RC boreholes, no barrier
    c15_1_1 = sum(1 for b in cp_rc if not b.over_barrier_wall_fence)
    # C15.1.2: CP/RC boreholes, with barrier
    c15_1_2 = sum(1 for b in cp_rc if b.over_barrier_wall_fence)
    # C15.2.1: RC-only boreholes, no barrier
    c15_2_1 = sum(1 for b in rc_only if not b.over_barrier_wall_fence)
    # C15.2.2: RC-only boreholes, with barrier
    c15_2_2 = sum(1 for b in rc_only if b.over_barrier_wall_fence)
    # C15.3: Count of RC-only boreholes (for CAT scan)
    c15_3 = len(rc_only)
    # C16: All rotary boreholes on slopes
    c16 = sum(1 for b in all_rotary if b.slope_over_20pct)
    # C18: Same B3.1 formula — road column literal check (flagged for review)
    c18 = sum(1 for b in project.boreholes if b.road == "YES") * 0.125
    # C19: Standing time = total rotary borehole count
    c19 = c15_1_1 + c15_1_2 + c15_2_1 + c15_2_2

    # Depth-band distributions per rotary method
    # C21-C24: RC_NO_CORE_SOFT (soft, no core) across 4 bands
    soft_no_core = _sum_rotary_bands(project.boreholes, DrillingMethod.ROTARY_NO_CORE_SOFT)
    # C27-C30: RC_NO_CORE_HARD (hard, no core) across 4 bands
    hard_no_core = _sum_rotary_bands(project.boreholes, DrillingMethod.ROTARY_NO_CORE_HARD)
    # C34-C37: RC_CORE_SOFT (soft, with core) across 4 bands
    soft_core = _sum_rotary_bands(project.boreholes, DrillingMethod.ROTARY_CORE_SOFT)
    # C41-C44: RC_CORE_HARD (hard, with core) across 4 bands
    hard_core = _sum_rotary_bands(project.boreholes, DrillingMethod.ROTARY_CORE_HARD)

    return [
        # C1-C6: Hand augering — Not Required
        BoqItem(
            code="C1",
            description="Move hand auger equipment to each location and set up",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="C2",
            description="Extra over Item C1 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="C3",
            description="Advance hand auger borehole between existing ground level and 5 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C4",
            description="Standing time for hand augering equipment and crew",
            unit="h",
            quantity="Not Required",
        ),
        BoqItem(
            code="C5",
            description=(
                "Backfill hand auger borehole with cement/bentonite grout or " "bentonite pellets"
            ),
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="C6",
            description="Reinstatement of grass areas after hand augering",
            unit="m²",
            quantity="Not Required",
        ),
        # C7-C14: Mechanical augering — Not Required
        BoqItem(
            code="C7",
            description="Move mechanical auger equipment to each location and set up",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="C8",
            description=(
                "Extra over Item C7 for setting up on a slope of gradient " "greater than 20%"
            ),
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="C9",
            description=(
                "Advance mechanical auger borehole between existing ground " "level and 10 m depth"
            ),
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C10",
            description="As Item C9 but between 10 m and 20 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C11",
            description="As Item C9 but between 20 m and 30 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C12",
            description="Advance mechanical auger borehole through hard stratum or obstruction",
            unit="h",
            quantity="Not Required",
        ),
        BoqItem(
            code="C13",
            description="Standing time for mechanical augering equipment and crew",
            unit="h",
            quantity="Not Required",
        ),
        BoqItem(
            code="C14",
            description=(
                "Backfill mechanical auger borehole with cement/bentonite grout "
                "or bentonite pellets"
            ),
            unit="m³",
            quantity="Not Required",
        ),
        # C15 — Rotary drilling move and set up
        BoqItem(
            code="C15",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory hole and set up"
            ),
            unit="Refer to items C15.1 to C15.3",
            quantity="Refer to items C15.1 to C15.3",
        ),
        BoqItem(
            code="C15.1.1",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory hole, set up, dismantle on completion and reinstate "
                "(where borehole is preceded by cable percussion)"
            ),
            unit="nr",
            quantity=c15_1_1,
        ),
        BoqItem(
            code="C15.1.2",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory hole over safety barrier or other fence or wall, "
                "set up, dismantle on completion and reinstate (where borehole "
                "is preceded by cable percussion)"
            ),
            unit="nr",
            quantity=c15_1_2,
        ),
        BoqItem(
            code="C15.2.1",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory hole, set up, dismantle on completion and reinstate "
                "(rotary only)"
            ),
            unit="nr",
            quantity=c15_2_1,
        ),
        BoqItem(
            code="C15.2.2",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory hole over safety barrier or other fence or wall, "
                "set up, dismantle on completion and reinstate (rotary only)"
            ),
            unit="nr",
            quantity=c15_2_2,
        ),
        BoqItem(
            code="C15.3",
            description=(
                "Hand digging and CAT scan at rotary-only borehole location to "
                "confirm absence of utility ducts (maximum depth of 1.2m)"
            ),
            unit="nr",
            quantity=c15_3,
        ),
        # C16: Extra for slope
        BoqItem(
            code="C16",
            description=(
                "Extra over Item C15 for setting up on a slope of gradient " "greater than 20%"
            ),
            unit="nr",
            quantity=c16,
        ),
        # C17: Aquifer protection — included
        BoqItem(
            code="C17",
            description=(
                "Provide aquifer protection measures at a single "
                "aquiclude/aquifer boundary or cross-contamination control "
                "measures at a single soil boundary in a borehole"
            ),
            unit="nr",
            quantity="Included in C15 to C15.2.2",
        ),
        # C18: Break out obstructions (road flag — flagged for review)
        BoqItem(
            code="C18",
            description=(
                "Break out obstructions where present when hand digging at "
                "exploratory hole location for Item C15.3"
            ),
            unit="m3",
            quantity=c18,
        ),
        # C19: Standing time
        BoqItem(
            code="C19",
            description="Standing time for rotary drilling plant, equipment and crew",
            unit="h",
            quantity=c19,
        ),
        # C20: Hard stratum — included
        BoqItem(
            code="C20",
            description="Advance borehole through hard stratum or obstruction",
            unit="h",
            quantity="Included in C15 to C15.2.2",
        ),
        # C21-C24: Rotary open hole, soft formation (RC_NO_CORE_SOFT), 4 bands
        BoqItem(
            code="C21",
            description=(
                "Advance rotary borehole in soft formation without core recovery "
                "between existing ground level and 10 m depth"
            ),
            unit="m",
            quantity=soft_no_core[0],
        ),
        BoqItem(
            code="C22",
            description="As Item C21 but between 10 m and 20 m depth",
            unit="m",
            quantity=soft_no_core[1],
        ),
        BoqItem(
            code="C23",
            description="As Item C21 but between 20 m and 30 m depth",
            unit="m",
            quantity=soft_no_core[2],
        ),
        BoqItem(
            code="C24",
            description="As Item C21 but between 30 m and 40 m depth",
            unit="m",
            quantity=soft_no_core[3],
        ),
        # C25-C26: 40-50m and >50m soft no core — Not Required
        BoqItem(
            code="C25",
            description="As Item C21 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C26",
            description="As Item C21 but greater than 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        # C27-C30: Rotary open hole, hard formation (RC_NO_CORE_HARD), 4 bands
        BoqItem(
            code="C27",
            description=(
                "Advance rotary borehole in hard formation without core recovery "
                "between existing ground level and 10 m depth"
            ),
            unit="m",
            quantity=hard_no_core[0],
        ),
        BoqItem(
            code="C28",
            description="As Item C27 but between 10 m and 20 m depth",
            unit="m",
            quantity=hard_no_core[1],
        ),
        BoqItem(
            code="C29",
            description="As Item C27 but between 20 m and 30 m depth",
            unit="m",
            quantity=hard_no_core[2],
        ),
        BoqItem(
            code="C30",
            description="As Item C27 but between 30 m and 40 m depth",
            unit="m",
            quantity=hard_no_core[3],
        ),
        # C31-C32: 40-50m and >50m hard no core — Not Required
        BoqItem(
            code="C31",
            description="As Item C27 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C32",
            description="As Item C27 but greater than 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        # C33: Flush — included
        BoqItem(
            code="C33",
            description=(
                "Supply and use of special drilling flush (polymer or foam) as "
                "instructed by the Investigation Supervisor"
            ),
            unit="m",
            quantity="Included in C21 to C32",
        ),
        # C34-C37: Rotary coring, soft formation (RC_CORE_SOFT), 4 bands
        BoqItem(
            code="C34",
            description=(
                "Advance rotary borehole in soft formation with core recovery "
                "between existing ground level and 10 m depth"
            ),
            unit="m",
            quantity=soft_core[0],
        ),
        BoqItem(
            code="C35",
            description="As Item C34 but between 10 m and 20 m depth",
            unit="m",
            quantity=soft_core[1],
        ),
        BoqItem(
            code="C36",
            description="As Item C34 but between 20 m and 30 m depth",
            unit="m",
            quantity=soft_core[2],
        ),
        BoqItem(
            code="C37",
            description="As Item C34 but between 30 m and 40 m depth",
            unit="m",
            quantity=soft_core[3],
        ),
        # C38-C40: 40-50m, >50m soft core, special flush — Not Required / Included
        BoqItem(
            code="C38",
            description="As Item C34 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C39",
            description="As Item C34 but greater than 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C40",
            description=(
                "Supply and use of special drilling flush (polymer or foam) as "
                "instructed by the Investigation Supervisor"
            ),
            unit="m",
            quantity="Included in C34 to C39",
        ),
        # C41-C44: Rotary coring, hard formation (RC_CORE_HARD), 4 bands
        BoqItem(
            code="C41",
            description=(
                "Advance rotary borehole in hard formation with core recovery "
                "between existing ground level and 10 m depth"
            ),
            unit="m",
            quantity=hard_core[0],
        ),
        BoqItem(
            code="C42",
            description="As Item C41 but between 10 m and 20 m depth",
            unit="m",
            quantity=hard_core[1],
        ),
        BoqItem(
            code="C43",
            description="As Item C41 but between 20 m and 30 m depth",
            unit="m",
            quantity=hard_core[2],
        ),
        BoqItem(
            code="C44",
            description="As Item C41 but between 30 m and 40 m depth",
            unit="m",
            quantity=hard_core[3],
        ),
        # C45-C47: 40-50m, >50m hard core, special flush — Not Required / Included
        BoqItem(
            code="C45",
            description="As Item C41 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C46",
            description="As Item C41 but greater than 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C47",
            description=(
                "Supply and use of special drilling flush (polymer or foam) as "
                "instructed by the Investigation Supervisor"
            ),
            unit="m",
            quantity="Included in C41 to C46",
        ),
        # C48-C85: Remaining items — various Not Required / Included placeholders
        BoqItem(
            code="C48",
            description="Core boxes — supply and deliver to site",
            unit="nr",
            quantity="Included in C34 to C46",
        ),
        BoqItem(
            code="C49",
            description=("Core boxes — label, pack and transport to laboratory or store"),
            unit="nr",
            quantity="Included in C34 to C46",
        ),
        BoqItem(
            code="C50",
            description="Water supply for rotary drilling — supply tanker and water",
            unit="nr",
            quantity="Included in C15 to C15.2.2",
        ),
        BoqItem(
            code="C51",
            description=(
                "Backfill rotary borehole with cement/bentonite grout or "
                "bentonite pellets (where standpipe piezometer is not installed)"
            ),
            unit="m³",
            quantity="Included in C15 to C15.2.2",
        ),
        BoqItem(
            code="C52",
            description="Reinstatement of gravel hardstanding",
            unit="m²",
            quantity="Included in C15 to C15.2.2",
        ),
        BoqItem(
            code="C53",
            description="Reinstatement of asphalt / bituminous pavement",
            unit="m²",
            quantity="Included in D53",
        ),
        BoqItem(
            code="C54",
            description="Reinstatement of grass areas",
            unit="m²",
            quantity="Included in C15 to C15.2.2",
        ),
        BoqItem(
            code="C55",
            description="Provision of stock proof fencing to borehole work area",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="C56",
            description="Disposal of excess or surplus inert arisings from rotary drilling",
            unit="m³",
            quantity="Included in C15 to C15.2.2",
        ),
        BoqItem(
            code="C57",
            description="Rotary percussive drilling (down-the-hole hammer) 0-10 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C58",
            description="As Item C57 but between 10 m and 20 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C59",
            description="As Item C57 but between 20 m and 30 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C60",
            description="As Item C57 but between 30 m and 40 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C61",
            description="As Item C57 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C62",
            description="As Item C57 but greater than 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C63",
            description="Sonic drilling 0-10 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C64",
            description="As Item C63 but between 10 m and 20 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C65",
            description="As Item C63 but between 20 m and 30 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C66",
            description="As Item C63 but between 30 m and 40 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C67",
            description="As Item C63 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C68",
            description="As Item C63 but greater than 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C69",
            description="Resonant sonic drilling 0-10 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C70",
            description="As Item C69 but between 10 m and 20 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C71",
            description="As Item C69 but between 20 m and 30 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C72",
            description="As Item C69 but between 30 m and 40 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C73",
            description="As Item C69 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C74",
            description="As Item C69 but greater than 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C75",
            description="Windowless sampling 0-5 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C76",
            description="As Item C75 but between 5 m and 10 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C77",
            description="Window sampling 0-5 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C78",
            description="As Item C77 but between 5 m and 10 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="C79",
            description=(
                "Core boxes — supply, label, pack and transport to laboratory "
                "or store (sonic / resonant sonic)"
            ),
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="C80",
            description="Water supply for sonic / resonant sonic drilling",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="C81",
            description=(
                "Backfill sonic / resonant sonic borehole with "
                "cement/bentonite grout or bentonite pellets"
            ),
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="C82",
            description="Reinstatement of gravel hardstanding (sonic / resonant sonic)",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="C83",
            description="Reinstatement of asphalt / bituminous pavement (sonic / resonant sonic)",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="C84",
            description="Reinstatement of grass areas (sonic / resonant sonic)",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="C85",
            description=(
                "Disposal of excess or surplus inert arisings from "
                "sonic / resonant sonic drilling"
            ),
            unit="m³",
            quantity="Not Required",
        ),
    ]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _drilling_type(borehole: Borehole) -> str | None:
    """Return 'CP/RC', 'RC', or None.

    - ``"CP/RC"`` — at least one CP phase AND at least one rotary phase.
    - ``"RC"``    — at least one rotary phase AND no CP phase.
    - ``None``    — no rotary phases (CP-only or empty) → not in Section C.
    """
    methods = {p.method for p in borehole.phases}
    has_cp = _CP in methods
    has_rotary = bool(methods & _ROTARY_METHODS)
    if not has_rotary:
        return None
    if has_cp and has_rotary:
        return "CP/RC"
    return "RC"


def _rotary_band_distribution(borehole: Borehole, method: DrillingMethod) -> list[float]:
    """Return metreage for *method* split across 0-10/10-20/20-30/30-40 bands.

    Phases are assumed to run sequentially from the surface. The rotary
    segment's start is the sum of all phases before the first occurrence of
    *method*; its total depth is the sum of all *method* phases (which may
    not be contiguous, but the Excel model treats them as one run).
    """
    offset = 0.0
    found = False
    total = 0.0
    for phase in borehole.phases:
        if phase.method is method:
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


def _sum_rotary_bands(boreholes: list[Borehole], method: DrillingMethod) -> list[float]:
    """Sum the band distribution for *method* across all boreholes."""
    bands = [0.0, 0.0, 0.0, 0.0]
    for bh in boreholes:
        for i, metres in enumerate(_rotary_band_distribution(bh, method)):
            bands[i] += metres
    return bands
