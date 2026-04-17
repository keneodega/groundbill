"""Section F — Probing and Cone Penetration Testing (CPT).

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section F'
(with cross-references to the Log Tracker workbook's `DPH` and `CPT` sheets).

Key formulas
============
F1  = count of completed dynamic probes
F2  = count of dynamic probes on slopes (slope_over_20pct = True)
F3  = DPH depth band 0–5 m: sum min(dp.depth_m, 5) for completed probes
F4  = DPH depth band 5–10 m: sum min(5, max(0, dp.depth_m - 5))
F5  = DPH depth band 10–15 m: sum min(5, max(0, dp.depth_m - 10))
F6  = standing time = F1 count
F8  = count of completed CPTs (non-piezocone)
F9  = count of completed piezocone CPTs
F10 = count of CPTs on slopes
F11 = CPT depth band 0–10 m: sum min(depth, 10) for completed CPTs
F12 = CPT depth band 10–20 m: sum min(10, max(0, depth - 10))
F13 = CPT depth band 20–30 m: sum min(10, max(0, depth - 20))
F14 = CPT depth band 30–40 m: sum min(10, max(0, depth - 30))
F15 = standing time = F8 + F9

Static items: F7, F16–F22 — "Not Required".
"""

from groundbill.models import Project

from .boq_items import BoqItem


def compute_section_f(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section F BOQ items for the given project."""

    completed_dps = [dp for dp in project.dynamic_probes if dp.completed]

    f1 = len(completed_dps)
    f2 = sum(1 for dp in completed_dps if dp.slope_over_20pct)

    # DPH depth bands (5 m bands: 0-5, 5-10, 10-15)
    f3 = sum(min(dp.depth_m, 5.0) for dp in completed_dps)
    f4 = sum(min(5.0, max(0.0, dp.depth_m - 5.0)) for dp in completed_dps)
    f5 = sum(min(5.0, max(0.0, dp.depth_m - 10.0)) for dp in completed_dps)

    # F6: Standing time = number of completed probes
    f6 = f1

    # CPT counts
    completed_cpts = [c for c in project.cpts if c.completed]
    f8 = sum(1 for c in completed_cpts if not c.piezocone)
    f9 = sum(1 for c in completed_cpts if c.piezocone)
    f10 = sum(1 for c in completed_cpts if c.slope_over_20pct)

    # CPT depth bands (10 m bands: 0-10, 10-20, 20-30, 30-40)
    f11 = sum(min(c.depth_m, 10.0) for c in completed_cpts)
    f12 = sum(min(10.0, max(0.0, c.depth_m - 10.0)) for c in completed_cpts)
    f13 = sum(min(10.0, max(0.0, c.depth_m - 20.0)) for c in completed_cpts)
    f14 = sum(min(10.0, max(0.0, c.depth_m - 30.0)) for c in completed_cpts)

    # F15: Standing time = total CPT count
    f15 = f8 + f9

    return [
        BoqItem(
            code="F1",
            description=(
                "Move dynamic probing equipment to the site of each "
                "exploratory hole, set up, dismantle on completion and reinstate"
            ),
            unit="nr",
            quantity=f1,
        ),
        BoqItem(
            code="F2",
            description=(
                "Extra over Item F1 for setting up on a slope of gradient " "greater than 20%"
            ),
            unit="nr",
            quantity=f2,
        ),
        BoqItem(
            code="F3",
            description="Advance dynamic probe between existing ground level and 5 m depth",
            unit="m",
            quantity=f3,
        ),
        BoqItem(
            code="F4",
            description="As Item F3 but between 5 m and 10 m depth",
            unit="m",
            quantity=f4,
        ),
        BoqItem(
            code="F5",
            description="As Item F3 but between 10 m and 15 m depth",
            unit="m",
            quantity=f5,
        ),
        BoqItem(
            code="F6",
            description="Standing time for dynamic probing equipment and crew",
            unit="h",
            quantity=f6,
        ),
        BoqItem(
            code="F7",
            description="Backfill dynamic probe hole",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="F8",
            description=(
                "Move CPT equipment to the site of each exploratory hole, "
                "set up, dismantle on completion and reinstate (standard cone)"
            ),
            unit="nr",
            quantity=f8,
        ),
        BoqItem(
            code="F9",
            description=(
                "Move CPT equipment to the site of each exploratory hole, "
                "set up, dismantle on completion and reinstate (piezocone)"
            ),
            unit="nr",
            quantity=f9,
        ),
        BoqItem(
            code="F10",
            description=(
                "Extra over Items F8/F9 for setting up on a slope of gradient " "greater than 20%"
            ),
            unit="nr",
            quantity=f10,
        ),
        BoqItem(
            code="F11",
            description="Advance CPT between existing ground level and 10 m depth",
            unit="m",
            quantity=f11,
        ),
        BoqItem(
            code="F12",
            description="As Item F11 but between 10 m and 20 m depth",
            unit="m",
            quantity=f12,
        ),
        BoqItem(
            code="F13",
            description="As Item F11 but between 20 m and 30 m depth",
            unit="m",
            quantity=f13,
        ),
        BoqItem(
            code="F14",
            description="As Item F11 but between 30 m and 40 m depth",
            unit="m",
            quantity=f14,
        ),
        BoqItem(
            code="F15",
            description="Standing time for CPT equipment and crew",
            unit="h",
            quantity=f15,
        ),
        BoqItem(
            code="F16",
            description="Dissipation test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="F17",
            description="Seismic CPT",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="F18",
            description="Resistivity CPT",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="F19",
            description="Backfill CPT hole with cement/bentonite grout",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="F20",
            description="Reinstatement of gravel hardstanding",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="F21",
            description="Reinstatement of asphalt / bituminous pavement",
            unit="m²",
            quantity="Not Required",
        ),
        BoqItem(
            code="F22",
            description="Reinstatement of grass areas",
            unit="m²",
            quantity="Not Required",
        ),
    ]
