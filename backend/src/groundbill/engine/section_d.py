"""Section D — Pitting and Trenching.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section D'
(with cross-references to the Log Tracker workbook's `Trial Pits`, `Trenches`,
and `Inspection pit` sheets).

Trial pit depth bands (derived columns in Log Tracker)
------------------------------------------------------
- Col O: 0-3 m  = ``min(depth, 3)``
- Col P: 3-4.5 m = ``min(1.5, max(0, depth - 3))``
- Col Q: 0-1.2 m = ``min(depth, 1.2)``
- Col R: 1.2-3 m = ``min(1.8, max(0, depth - 1.2))``
- Col T: Perimeter = ``2 * width + 2 * length``
- Col U: Area = ``width * length``
- Col V: Vol hard material = ``width * length * depth_of_hard_material``
- Col X: Vol 804 Rural = ``width * length * (depth - 0.1)`` if road = "RURAL"
- Col Y: Vol 804 National = ``(depth - 0.45) * width * length`` if road = "NATIONAL"
- Col AA: Asphalt Rural = ``(width + 0.2) * (length + 0.2)`` if road = "RURAL"
- Col AB: Asphalt National = ``width * length`` if road = "NATIONAL"

Trench derived columns (paved section)
---------------------------------------
- Paved 0-1.2 m = ``min(paved_depth, 1.2)``
- Paved 1.2-3 m = ``min(1.8, max(0, paved_depth - 1.2))``
- S: Paved vol 0-1.2 m = ``paved_length * paved_width * paved_0_1.2``
- T: Paved vol 1.2-3 m = ``paved_length * paved_width * paved_1.2_3``

Trench derived columns (non-paved section)
-------------------------------------------
- Non-paved 0-3 m = ``min(non_paved_depth, 3)``
- Non-paved 3-4.5 m = ``min(1.5, max(0, non_paved_depth - 3))``
- AD: Non-paved vol 0-3 m = ``non_paved_length * non_paved_width * non_paved_0_3``
- AE: Non-paved vol 3-4.5 m = ``non_paved_length * non_paved_width * non_paved_3_4.5``

Road type handling
------------------
The ``road`` field on TrialPit and Trench is ``str | None``. Expected values
are ``"RURAL"`` and ``"NATIONAL"`` (matching the Excel Log Tracker). No enum
is used; we match strings directly.

Open items for review (by Havilah)
----------------------------------
- D55 (Disposal volumes): rows 96/97 in the Excel Trial Pits and Trenches
  sheets are None. Translated literally (produces 0). May match D51 in a
  populated workbook.
- D19 (Trenches!X93): col X is unused in the formula row. Computed from the
  paved 1.2-3 m volume formula directly.
"""

from groundbill.models import InspectionPit, Project, Trench, TrialPit

from .boq_items import BoqItem


def compute_section_d(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section D BOQ items for the given project."""

    tps = project.trial_pits
    trenches = project.trenches
    ips = project.inspection_pits

    # --- D1: Inspection pit completed count ---
    d1 = sum(1 for ip in ips if ip.completed)

    # --- D2: Volume of hard surface obstruction for inspection pits ---
    d2 = sum(_ip_hard_surface_volume(ip) for ip in ips)

    # --- D3: Non-paved trial pits + trenches ---
    tp_non_paved = [tp for tp in tps if not tp.paved]
    tr_non_paved = [t for t in trenches if not t.paved]
    d3 = len(tp_non_paved) + len(tr_non_paved)

    # --- D3.1: Non-paved with barrier ---
    d3_1 = sum(1 for tp in tp_non_paved if tp.barrier) + sum(1 for t in tr_non_paved if t.barrier)

    # --- D4: Non-paved on slopes ---
    d4 = sum(1 for tp in tp_non_paved if tp.slope_over_20pct) + sum(
        1 for t in tr_non_paved if t.slope_over_20pct
    )

    # --- D6: Sum of non-paved TP 0-3 m band ---
    d6 = sum(_tp_band_0_3(tp) for tp in tp_non_paved)

    # --- D7: Sum of non-paved TP 3-4.5 m band ---
    d7 = sum(_tp_band_3_4_5(tp) for tp in tp_non_paved)

    # --- D9: Non-paved trench volume 0-3 m ---
    d9 = sum(_trench_non_paved_vol_0_3(t) for t in tr_non_paved)

    # --- D10: Non-paved trench volume 3-4.5 m ---
    d10 = sum(_trench_non_paved_vol_3_4_5(t) for t in tr_non_paved)

    # --- D12: TPs with traffic management ---
    d12 = sum(1 for tp in tps if tp.traffic_management)

    # --- D13: Trenches with traffic management ---
    d13 = sum(1 for t in trenches if t.traffic_management)

    # --- Paved items ---
    tp_paved = [tp for tp in tps if tp.paved]
    tr_paved = [t for t in trenches if t.paved]

    # --- D14: Perimeter of paved TPs + trenches ---
    d14 = sum(_tp_perimeter(tp) for tp in tp_paved) + sum(
        _trench_paved_perimeter(t) for t in tr_paved
    )

    # --- D15: Volume of hard material from TPs + trenches ---
    d15 = sum(_tp_hard_material_vol(tp) for tp in tps) + sum(
        _trench_hard_material_vol(t) for t in trenches
    )

    # --- D16: TP hard material vol + trench paved 0-1.2 m band vol ---
    d16 = sum(_tp_hard_material_vol(tp) for tp in tps) + sum(
        _trench_paved_vol_0_1_2(t) for t in tr_paved
    )

    # --- D17: Paved TP depth band 1.2-3 m ---
    d17 = sum(_tp_band_1_2_3(tp) for tp in tp_paved)

    # --- D18: Paved trench volume 0-1.2 m ---
    d18 = sum(_trench_paved_vol_0_1_2(t) for t in tr_paved)

    # --- D19: Paved trench volume 1.2-3 m ---
    # Trenches!X93 is None in the spreadsheet. Compute from the formula directly.
    d19 = sum(_trench_paved_vol_1_2_3(t) for t in tr_paved)

    # --- D20: Standing time = D15 * 0.5 ---
    d20 = d15 * 0.5

    # --- D49: Backfill with arisings (completed - national) ---
    tp_completed = sum(1 for tp in tps if tp.completed)
    tr_completed = sum(1 for t in trenches if t.completed)
    tp_national = sum(1 for tp in tps if tp.road == "NATIONAL")
    tr_national = sum(1 for t in trenches if t.road == "NATIONAL")
    d49 = (tp_completed + tr_completed) - (tp_national + tr_national)

    # --- D51: Imported granular fill volumes (rural + national) ---
    d51 = (
        sum(_tp_vol_804_rural(tp) for tp in tps)
        + sum(_tp_vol_804_national(tp) for tp in tps)
        + sum(_trench_vol_804_rural(t) for t in trenches)
        + sum(_trench_vol_804_national(t) for t in trenches)
    )

    # --- D53: Asphalt reinstatement areas (rural + national) ---
    d53 = (
        sum(_tp_asphalt_rural(tp) for tp in tps)
        + sum(_tp_asphalt_national(tp) for tp in tps)
        + sum(_trench_asphalt_rural(t) for t in trenches)
        + sum(_trench_asphalt_national(t) for t in trenches)
    )

    # --- D55: Disposal volumes (rows 96/97 in Excel are None — produces 0) ---
    # Flagged for review: may match D51 in a populated workbook.
    d55 = 0

    return [
        BoqItem(
            code="D1",
            description="Inspection pits — completed count",
            unit="nr",
            quantity=d1,
        ),
        BoqItem(
            code="D2",
            description="Inspection pits — volume of hard surface obstruction",
            unit="m³",
            quantity=d2,
        ),
        BoqItem(
            code="D3",
            description=(
                "Move pitting / trenching plant and equipment to the site of "
                "each exploratory hole, set up, dismantle on completion and "
                "reinstate (non-paved)"
            ),
            unit="nr",
            quantity=d3,
        ),
        BoqItem(
            code="D3.1",
            description=(
                "Move pitting / trenching plant and equipment to the site of "
                "each exploratory hole over safety barrier or other fence or "
                "wall, set up, dismantle on completion and reinstate (non-paved)"
            ),
            unit="nr",
            quantity=d3_1,
        ),
        BoqItem(
            code="D4",
            description=(
                "Extra over Item D3 for setting up on a slope of gradient " "greater than 20%"
            ),
            unit="nr",
            quantity=d4,
        ),
        BoqItem(
            code="D5",
            description=(
                "Hand digging and CAT scan at trial pit / trench location to "
                "confirm absence of utility ducts"
            ),
            unit="nr",
            quantity="Included in D3",
        ),
        BoqItem(
            code="D6",
            description=(
                "Excavate trial pit in non-paved ground between existing "
                "ground level and 3 m depth"
            ),
            unit="m",
            quantity=d6,
        ),
        BoqItem(
            code="D7",
            description="As Item D6 but between 3 m and 4.5 m depth",
            unit="m",
            quantity=d7,
        ),
        BoqItem(
            code="D8",
            description="As Item D6 but between 4.5 m and 6 m depth",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="D9",
            description=(
                "Excavate trench in non-paved ground between existing ground " "level and 3 m depth"
            ),
            unit="m³",
            quantity=d9,
        ),
        BoqItem(
            code="D10",
            description="As Item D9 but between 3 m and 4.5 m depth",
            unit="m³",
            quantity=d10,
        ),
        BoqItem(
            code="D11",
            description="As Item D9 but between 4.5 m and 6 m depth",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D12",
            description=("Traffic management for trial pit locations"),
            unit="nr",
            quantity=d12,
        ),
        BoqItem(
            code="D13",
            description="Traffic management for trench locations",
            unit="nr",
            quantity=d13,
        ),
        BoqItem(
            code="D14",
            description=(
                "Break out hard surface (paved areas) — perimeter of paved "
                "trial pits and trenches"
            ),
            unit="m",
            quantity=d14,
        ),
        BoqItem(
            code="D15",
            description=(
                "Break out hard material — volume of hard material from " "trial pits and trenches"
            ),
            unit="m³",
            quantity=d15,
        ),
        BoqItem(
            code="D16",
            description=(
                "Excavate trial pit / trench in paved ground between existing "
                "ground level and 1.2 m depth"
            ),
            unit="m³",
            quantity=d16,
        ),
        BoqItem(
            code="D17",
            description=("Excavate paved trial pit between 1.2 m and 3 m depth"),
            unit="m",
            quantity=d17,
        ),
        BoqItem(
            code="D18",
            description=("Excavate paved trench between existing ground level and " "1.2 m depth"),
            unit="m³",
            quantity=d18,
        ),
        BoqItem(
            code="D19",
            description="Excavate paved trench between 1.2 m and 3 m depth",
            unit="m³",
            quantity=d19,
        ),
        BoqItem(
            code="D20",
            description="Standing time for pitting / trenching plant, equipment and crew",
            unit="h",
            quantity=d20,
        ),
        # D21-D35: Not Required / Included placeholders
        BoqItem(
            code="D21",
            description="Shoring to sides of trial pit or trench",
            unit="m²",
            quantity="Included in D3 and D14",
        ),
        BoqItem(
            code="D22",
            description="Pumping from trial pit or trench",
            unit="h",
            quantity="Included in D3 and D14",
        ),
        BoqItem(
            code="D23",
            description="Extra over excavation for working in contaminated ground",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D24",
            description="Soil nailing or anchoring to sides of trial pit or trench",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="D25",
            description="Geomembrane or geotextile lining to sides of trial pit",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="D26",
            description="Steel plate to cover trial pit or trench overnight",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D27",
            description="Concrete cap to trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D28",
            description="Inspection of trial pit or trench by engineer",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D29",
            description="Photographic record of trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D30",
            description="Disturbed sample from trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D31",
            description="Small disturbed sample from trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D32",
            description="Bulk disturbed sample from trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D33",
            description="Block sample from trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D34",
            description="Water sample from trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D35",
            description="Gas sample from trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        # D36-D48: Not Required placeholders
        BoqItem(
            code="D36",
            description="Hand-excavated trial pit 0-1.2 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="D37",
            description="Hand-excavated trial pit 1.2-3 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="D38",
            description="Hand-excavated trial pit 3-4.5 m",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="D39",
            description="Hand-excavated trench 0-1.2 m",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D40",
            description="Hand-excavated trench 1.2-3 m",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D41",
            description="Hand-excavated trench 3-4.5 m",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D42",
            description="Slit trench 0-1.2 m",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D43",
            description="Slit trench 1.2-3 m",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D44",
            description="Slit trench 3-4.5 m",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D45",
            description="Observation pit",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D46",
            description="Landscaping trial pit or trench reinstatement",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="D47",
            description="Provision of stock proof fencing to trial pit or trench",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="D48",
            description="Disposal of contaminated arisings from trial pit or trench",
            unit="m³",
            quantity="Not Required",
        ),
        # D49: Backfill with arisings
        BoqItem(
            code="D49",
            description=(
                "Backfill trial pit or trench with arisings (excluding " "national road sites)"
            ),
            unit="nr",
            quantity=d49,
        ),
        BoqItem(
            code="D50",
            description="Backfill trial pit or trench with imported inert fill",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="D50.2",
            description="Compaction of backfill in trial pit or trench",
            unit="m³",
            quantity="Not Required",
        ),
        # D51: Imported granular fill
        BoqItem(
            code="D51",
            description="Imported granular fill (Clause 804) for trial pits and trenches",
            unit="m³",
            quantity=d51,
        ),
        BoqItem(
            code="D52",
            description="Compaction of imported granular fill",
            unit="m³",
            quantity="Not Required",
        ),
        # D53: Asphalt reinstatement
        BoqItem(
            code="D53",
            description="Reinstatement of asphalt / bituminous pavement",
            unit="m²",
            quantity=d53,
        ),
        BoqItem(
            code="D54",
            description="Reinstatement of concrete pavement",
            unit="m²",
            quantity="Not Required",
        ),
        # D55: Disposal volumes (rows 96/97 are None — flagged for review)
        BoqItem(
            code="D55",
            description=(
                "Disposal of excess or surplus inert arisings from trial pits " "and trenches"
            ),
            unit="m³",
            quantity=d55,
        ),
    ]


# ---------------------------------------------------------------------------
# Trial pit helpers
# ---------------------------------------------------------------------------


def _tp_band_0_3(tp: TrialPit) -> float:
    """Col O: min(depth, 3)."""
    d = tp.depth_m or 0.0
    return min(d, 3.0)


def _tp_band_3_4_5(tp: TrialPit) -> float:
    """Col P: min(1.5, max(0, depth - 3))."""
    d = tp.depth_m or 0.0
    return min(1.5, max(0.0, d - 3.0))


def _tp_band_0_1_2(tp: TrialPit) -> float:
    """Col Q: min(depth, 1.2)."""
    d = tp.depth_m or 0.0
    return min(d, 1.2)


def _tp_band_1_2_3(tp: TrialPit) -> float:
    """Col R: min(1.8, max(0, depth - 1.2))."""
    d = tp.depth_m or 0.0
    return min(1.8, max(0.0, d - 1.2))


def _tp_perimeter(tp: TrialPit) -> float:
    """Col T: 2 * width + 2 * length."""
    w = tp.width_m or 0.0
    ln = tp.length_m or 0.0
    return 2 * w + 2 * ln


def _tp_hard_material_vol(tp: TrialPit) -> float:
    """Col V: width * length * depth_of_hard_material."""
    w = tp.width_m or 0.0
    ln = tp.length_m or 0.0
    dh = tp.depth_of_hard_material_m or 0.0
    return w * ln * dh


def _tp_vol_804_rural(tp: TrialPit) -> float:
    """Col X: width * length * (depth - 0.1) if road = RURAL, else 0."""
    if tp.road != "RURAL":
        return 0.0
    w = tp.width_m or 0.0
    ln = tp.length_m or 0.0
    d = tp.depth_m or 0.0
    return w * ln * max(0.0, d - 0.1)


def _tp_vol_804_national(tp: TrialPit) -> float:
    """Col Y: (depth - 0.45) * width * length if road = NATIONAL, else 0."""
    if tp.road != "NATIONAL":
        return 0.0
    w = tp.width_m or 0.0
    ln = tp.length_m or 0.0
    d = tp.depth_m or 0.0
    return max(0.0, d - 0.45) * w * ln


def _tp_asphalt_rural(tp: TrialPit) -> float:
    """Col AA: (width + 0.2) * (length + 0.2) if road = RURAL, else 0."""
    if tp.road != "RURAL":
        return 0.0
    w = tp.width_m or 0.0
    ln = tp.length_m or 0.0
    return (w + 0.2) * (ln + 0.2)


def _tp_asphalt_national(tp: TrialPit) -> float:
    """Col AB: width * length if road = NATIONAL, else 0."""
    if tp.road != "NATIONAL":
        return 0.0
    w = tp.width_m or 0.0
    ln = tp.length_m or 0.0
    return w * ln


def _ip_hard_surface_volume(ip: InspectionPit) -> float:
    """Inspection pit hard surface volume: depth_hard_surface * length * width."""
    dh = ip.depth_hard_surface_obstruction_m or 0.0
    ln = ip.scheduled_length_m or 0.0
    w = ip.scheduled_width_m or 0.0
    return dh * ln * w


# ---------------------------------------------------------------------------
# Trench helpers
# ---------------------------------------------------------------------------


def _trench_non_paved_vol_0_3(t: Trench) -> float:
    """Non-paved vol 0-3 m: length * width * min(depth, 3)."""
    ln = t.non_paved_length_m or 0.0
    w = t.non_paved_width_m or 0.0
    d = t.non_paved_depth_m or 0.0
    return ln * w * min(d, 3.0)


def _trench_non_paved_vol_3_4_5(t: Trench) -> float:
    """Non-paved vol 3-4.5 m: length * width * min(1.5, max(0, depth - 3))."""
    ln = t.non_paved_length_m or 0.0
    w = t.non_paved_width_m or 0.0
    d = t.non_paved_depth_m or 0.0
    return ln * w * min(1.5, max(0.0, d - 3.0))


def _trench_paved_perimeter(t: Trench) -> float:
    """Paved trench perimeter: 2 * width + 2 * length."""
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    return 2 * w + 2 * ln


def _trench_hard_material_vol(t: Trench) -> float:
    """Volume of hard material: paved_length * paved_width * paved_depth_hard_material."""
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    dh = t.paved_depth_hard_material_m or 0.0
    return ln * w * dh


def _trench_paved_vol_0_1_2(t: Trench) -> float:
    """Paved vol 0-1.2 m (col S): paved_length * paved_width * min(depth, 1.2)."""
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    d = t.paved_depth_m or 0.0
    return ln * w * min(d, 1.2)


def _trench_paved_vol_1_2_3(t: Trench) -> float:
    """Paved vol 1.2-3 m (col T): paved_length * paved_width * min(1.8, max(0, depth - 1.2))."""
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    d = t.paved_depth_m or 0.0
    return ln * w * min(1.8, max(0.0, d - 1.2))


def _trench_vol_804_rural(t: Trench) -> float:
    """Col AG: paved_length * paved_width * (paved_depth - 0.1) if road = RURAL."""
    if t.road != "RURAL":
        return 0.0
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    d = t.paved_depth_m or 0.0
    return ln * w * max(0.0, d - 0.1)


def _trench_vol_804_national(t: Trench) -> float:
    """Col AH: (paved_depth - 0.45) * paved_length * paved_width if road = NATIONAL."""
    if t.road != "NATIONAL":
        return 0.0
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    d = t.paved_depth_m or 0.0
    return max(0.0, d - 0.45) * ln * w


def _trench_asphalt_rural(t: Trench) -> float:
    """Col AI: (paved_length + 0.2) * (paved_width + 0.2) if road = RURAL."""
    if t.road != "RURAL":
        return 0.0
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    return (ln + 0.2) * (w + 0.2)


def _trench_asphalt_national(t: Trench) -> float:
    """Col AJ: paved_length * paved_width if road = NATIONAL."""
    if t.road != "NATIONAL":
        return 0.0
    ln = t.paved_length_m or 0.0
    w = t.paved_width_m or 0.0
    return ln * w
