"""Section B — Cable Percussion Boring and Dynamic Sampling.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section B'
(with cross-references to the Log Tracker workbook's `Boreholes` and
`Dynamic Sampling` sheets).

Borehole classification
-----------------------
The Log Tracker's column B ('Type of drilling') is a manually-entered string
with two values the Section B formulas recognise:

- ``"CP"``    — cable percussion only.
- ``"CP/RC"`` — cable percussion followed by rotary drilling.

In the Python model we derive the classification from the `Borehole.phases`
list: any borehole with at least one CP phase and no rotary phase is ``"CP"``;
any borehole with both CP and rotary phases is ``"CP/RC"``. Boreholes with
only rotary phases do not appear in Section B.

Depth-band distribution
-----------------------
Items B4-B7 need the total cable-percussion metreage split into the four
10 m bands 0-10, 10-20, 20-30, 30-40. The Log Tracker does this with the
per-row START/END columns (L/M) and nested IFs across N/O/P/Q. We compute
the equivalent by finding the CP segment's [start, end] and clipping it
against each band.

B8 ("As Item B4 but between 40 m and 50 m depth") is left as ``Not Required``
to match the Calculator workbook, which does not compute a 40-50 m band.

Dynamic sampling bands
----------------------
B17/B18/B19 come from the Dynamic Sampling sheet columns D/E/F:

- ``D = IF(C>5, 5, C)``                  — 0-5 m band
- ``E = IF(C>10, 5, MAX(0, C-5))``       — 5-10 m band
- ``F = IF(C>10, C-10, MAX(0, C-10))``   — >10 m band

ROAD column (resolved 2026-10-01)
--------------------------------
- B3.1 ("Break out obstructions...") is driven by
  ``COUNTIF(Boreholes!$BH$2:$BH91, "YES") * 0.125`` in the Calculator. Column
  BH is 'ROAD'; Sections C and I test the same column for "YES" / "NO", so it
  is a yes/no flag, stored on the model as ``Borehole.on_road``. The formula
  counts every borehole on a road, whatever its drilling type.
"""

from groundbill.models import Borehole, DrillingMethod, DynamicSample, Project

from .boq_items import BoqItem

_CP = DrillingMethod.CABLE_PERCUSSION
_ROTARY_METHODS = {
    DrillingMethod.ROTARY_CORE_HARD,
    DrillingMethod.ROTARY_NO_CORE_HARD,
    DrillingMethod.ROTARY_CORE_SOFT,
    DrillingMethod.ROTARY_NO_CORE_SOFT,
}

_DEPTH_BANDS_10M = ((0.0, 10.0), (10.0, 20.0), (20.0, 30.0), (30.0, 40.0))


def compute_section_b(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section B BOQ items for the given project."""

    cp_only = [b for b in project.boreholes if _drilling_type(b) == "CP"]
    cp_rc = [b for b in project.boreholes if _drilling_type(b) == "CP/RC"]

    b1_1_1 = sum(1 for b in cp_only if not b.over_barrier_wall_fence)
    b1_1_2 = sum(1 for b in cp_only if b.over_barrier_wall_fence)
    b1_2_1 = sum(1 for b in cp_rc if not b.over_barrier_wall_fence)
    b1_2_2 = sum(1 for b in cp_rc if b.over_barrier_wall_fence)

    b2_1 = sum(1 for b in cp_only if b.slope_over_20pct)
    b2_2 = sum(1 for b in cp_rc if b.slope_over_20pct)

    total_bh = b1_1_1 + b1_1_2 + b1_2_1 + b1_2_2

    # 'Section B'!D19: =(COUNTIF([1]Boreholes!$BH$2:$BH91,"YES"))*0.125
    b3_1 = sum(1 for b in project.boreholes if b.on_road) * 0.125

    cp_bands = [0.0, 0.0, 0.0, 0.0]
    for bh in project.boreholes:
        for i, metres in enumerate(cp_band_distribution(bh)):
            cp_bands[i] += metres
    b4, b5, b6, b7 = cp_bands

    ds = project.dynamic_samples
    ds_count = len(ds)
    b17 = sum(_ds_band_0_5(d) for d in ds)
    b18 = sum(_ds_band_5_10(d) for d in ds)
    b19 = sum(_ds_band_over_10(d) for d in ds)
    ds_slope = sum(1 for d in ds if d.slope_over_20pct)

    return [
        BoqItem(
            code="B1",
            description=(
                "Move boring plant and equipment to the site of each exploratory hole "
                "and set up (cable percussive only)"
            ),
            unit="Refer to items  B1.1 and B1.2 ",
            quantity="Refer to items  B1.1 and B1.2 ",
        ),
        BoqItem(
            code="B1.1.1",
            description=(
                "Move boring plant and equipment to the site of each exploratory hole, "
                "set up, dismantle on completion and reinstate (cable percussive only)"
            ),
            unit="nr",
            quantity=b1_1_1,
        ),
        BoqItem(
            code="B1.1.2",
            description=(
                "Move boring plant and equipment to the site of each exploratory hole "
                "over safety barrier or other fence or wall, set up, dismantle on "
                "completion and reinstate (cable percussive only)"
            ),
            unit="nr",
            quantity=b1_1_2,
        ),
        BoqItem(
            code="B1.2.1",
            description=(
                "Move boring plant and equipment to the site of each exploratory hole, "
                "set up, dismantle on completion and reinstate (where borehole is to "
                "be followed on with rotary drilling)"
            ),
            unit="nr",
            quantity=b1_2_1,
        ),
        BoqItem(
            code="B1.2.2",
            description=(
                "Move boring plant and equipment to the site of each exploratory hole "
                "over safety barrier or other fence or wall, set up, dismantle on "
                "completion and reinstate (where borehole is to be followed on with "
                "rotary drilling)"
            ),
            unit="nr",
            quantity=b1_2_2,
        ),
        BoqItem(
            code="B2",
            description="Extra over Item B1 for setting up on a slope of gradient greater than 20%",
            unit="Refer to items B2.1 and B2.2",
            quantity="Refer to items B2.1 and B2.2",
        ),
        BoqItem(
            code="B2.1",
            description="Extra over Item B1.1 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=b2_1,
        ),
        BoqItem(
            code="B2.2",
            description="Extra over Item B1.2 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=b2_2,
        ),
        # B3 = D11+D12+D13+D14 in the Calculator (sum of the four B1.x counts).
        BoqItem(
            code="B3",
            description=(
                "Hand digging and CAT scan at borehole location to confirm absence of "
                "utility ducts (maximum depth of 1.2m or lesser if ground is assessed "
                "as potentially unstable)"
            ),
            unit="nr",
            quantity=total_bh,
        ),
        BoqItem(
            code="B3.1",
            description=(
                "Break out obstructions where present when hand digging at exploratory "
                "hole location for Item B3."
            ),
            unit="m³",
            quantity=b3_1,
        ),
        BoqItem(
            code="B4",
            description="Advance borehole between existing ground level and 10 m depth",
            unit="m",
            quantity=b4,
        ),
        BoqItem(
            code="B5",
            description="As Item B4 but between 10 m and 20 m depth",
            unit="m",
            quantity=b5,
        ),
        BoqItem(
            code="B6",
            description="As Item B4 but between 20 m and 30 m depth",
            unit="m",
            quantity=b6,
        ),
        BoqItem(
            code="B7",
            description="As Item B4 but between 30 m and 40 m depth",
            unit="m",
            quantity=b7,
        ),
        BoqItem(
            code="B8",
            description="As Item B4 but between 40 m and 50 m depth",
            unit="m",
            quantity="Not Required",
        ),
        # B9 = B3 * 2 in the Calculator (total BH count × 2 hours).
        BoqItem(
            code="B9",
            description="Advance borehole through hard stratum or obstruction",
            unit="h",
            quantity=total_bh * 2,
        ),
        BoqItem(
            code="B10",
            description=(
                "Provide aquifer protection measures at a single aquiclude/aquifer "
                "boundary or cross-contamination control measures at a single soil "
                "boundary in a borehole"
            ),
            unit="nr",
            quantity="Included in B1 to B1.2.2",
        ),
        BoqItem(
            code="B11",
            description=(
                "Backfill borehole with cement/bentonite grout or bentonite pellets "
                "(where standpipe piezometer is not installed)"
            ),
            unit="m³",
            quantity="Included in B1 to B1.2.2",
        ),
        # B12 = D11+D12+D13+D14 (total BH count); see module note on unit reconciliation.
        BoqItem(
            code="B12",
            description="Standing time for borehole plant, equipment and crew",
            unit="h",
            quantity=total_bh,
        ),
        BoqItem(
            code="B13",
            description="Move dynamic sampling equipment to the site of each exploratory hole and set up",
            unit="nr",
            quantity=ds_count,
            subheading="Dynamic sampling (Window and Windowless Sampling)",
        ),
        BoqItem(
            code="B14",
            description="Extra over Item B13 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=ds_slope,
        ),
        # B15 = D30*1 — one hand-dig/CAT-scan per dynamic sample hole.
        BoqItem(
            code="B15",
            description=(
                "Hand digging and CAT scan at dynamic sampling location to confirm "
                "absence of utility ducts (maximum depth of 1.2m or lesser if ground "
                "is assessed as potentially unstable)"
            ),
            unit="nr",
            quantity=ds_count,
        ),
        # B16 = D30*1 — one hour of obstruction break-out per DS hole (template assumption).
        BoqItem(
            code="B16",
            description="Break out surface obstruction where present",
            unit="h",
            quantity=ds_count,
        ),
        BoqItem(
            code="B17",
            description="Advance dynamic sample hole between existing ground level and 5 m depth",
            unit="m",
            quantity=b17,
        ),
        BoqItem(
            code="B18",
            description="As Item B15 but between 5 and 10 m depth",
            unit="m",
            quantity=b18,
        ),
        BoqItem(
            code="B19",
            description="Dynamic sampling >10m as instructed by the Investigation Supervisor",
            unit="m",
            quantity=b19,
        ),
        # B20 = D30 * 0.5 — half an hour of standing time per DS hole.
        BoqItem(
            code="B20",
            description="Standing time for dynamic sampling equipment and crew",
            unit="hr",
            quantity=ds_count * 0.5,
        ),
        BoqItem(
            code="B21",
            description=(
                "Backfill dynamic sample borehole with cement/bentonite grout or "
                "bentonite pellets (where standpipe or piezometer is not installed)"
            ),
            unit="m³",
            quantity="Included in B13",
        ),
        BoqItem(
            code="B22",
            description="Reinstatement of gravel hardstanding",
            unit="m²",
            quantity="Included in B1.1 & B1.2",
            subheading="Reinstatement of Cable Percussive Borehole and Dynamic Sample Borehole",
        ),
        BoqItem(
            code="B23",
            description="Reinstatement of asphalt / bituminous pavement",
            unit="m²",
            quantity="Included in D53",
        ),
        BoqItem(
            code="B24",
            description="Reinstatement of grass areas",
            unit="m²",
            quantity="Included in B1.1, B1.2 & B13",
        ),
        BoqItem(
            code="B25",
            description="Provision of stock proof fencing to borehole or dynamic sample work area",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="B26",
            description=(
                "Disposal of excess or surplus inert arisings from cable percussion "
                "boring or dynamic sampling (where standpipe or piezometer is not "
                "installed)"
            ),
            unit="m³",
            quantity="Included in B1 to B1.2.2",
        ),
    ]


def _drilling_type(borehole: Borehole) -> str | None:
    """Return 'CP', 'CP/RC', or None.

    Mirrors the Log Tracker column B classifier used by the Section B
    COUNTIFS formulas.
    """
    methods = {p.method for p in borehole.phases}
    has_cp = _CP in methods
    has_rotary = bool(methods & _ROTARY_METHODS)
    if has_cp and has_rotary:
        return "CP/RC"
    if has_cp:
        return "CP"
    return None


def cp_band_distribution(borehole: Borehole) -> list[float]:
    """Return CP metreage split across the 0-10 / 10-20 / 20-30 / 30-40 bands.

    Equivalent to Boreholes columns N:Q for one borehole. Also read by
    Section H (SPT counts), as in the Calculator.
    """
    cp_start = 0.0
    seen_cp = False
    cp_total = 0.0
    for phase in borehole.phases:
        if phase.method is _CP:
            seen_cp = True
            cp_total += phase.depth_m
        elif not seen_cp:
            cp_start += phase.depth_m
    if cp_total == 0.0:
        return [0.0, 0.0, 0.0, 0.0]
    cp_end = cp_start + cp_total
    return [
        max(0.0, min(cp_end, band_end) - max(cp_start, band_start))
        for band_start, band_end in _DEPTH_BANDS_10M
    ]


def _ds_band_0_5(sample: DynamicSample) -> float:
    """Dynamic Sampling col D: =IF(C>5, 5, C)."""
    return 5.0 if sample.depth_m > 5 else sample.depth_m


def _ds_band_5_10(sample: DynamicSample) -> float:
    """Dynamic Sampling col E: =IF(C>10, 5, MAX(0, C-5))."""
    if sample.depth_m > 10:
        return 5.0
    return max(0.0, sample.depth_m - 5)


def _ds_band_over_10(sample: DynamicSample) -> float:
    """Dynamic Sampling col F: =IF(C>10, C-10, MAX(0, C-10))."""
    return max(0.0, sample.depth_m - 10)
