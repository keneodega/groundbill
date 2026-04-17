"""Section K — Geotechnical Laboratory Testing.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section K'
(with cross-references to the Log Tracker workbook's `Boreholes`, `Trial Pits`,
`Inspection pit`, and `Dynamic Sampling` sheets).

Key formulas
============
K1.1  = E2 (tub sample count = total CP depth + TP depths + IP depths + DS depths)
K1.2  = 0.5 × K1.1
K1.9  = 0.25 × K1.1
K1.12 = 0.25 × K1.1

E2 is computed inline to avoid circular dependency with Section E.

Static items: all other K items are "Not Required" or None.
"""

from groundbill.models import DrillingMethod, Project

from .boq_items import BoqItem

_CP = DrillingMethod.CABLE_PERCUSSION


def compute_section_k(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section K BOQ items for the given project."""

    # Compute E2 inline (tub sample count)
    total_cp_depth = sum(
        phase.depth_m for bh in project.boreholes for phase in bh.phases if phase.method is _CP
    )
    tp_depth_sum = sum(tp.depth_m or 0.0 for tp in project.trial_pits)
    # Trenches!N93 is None in spreadsheet → 0
    ip_depth_sum = sum(ip.recorded_depth_m or 0.0 for ip in project.inspection_pits)
    ds_depth_sum = sum(ds.depth_m for ds in project.dynamic_samples)

    k1_1 = total_cp_depth + tp_depth_sum + ip_depth_sum + ds_depth_sum
    k1_2 = 0.5 * k1_1
    k1_9 = 0.25 * k1_1
    k1_12 = 0.25 * k1_1

    return [
        BoqItem(
            code="K1.1",
            description="Moisture content determination",
            unit="nr",
            quantity=k1_1,
        ),
        BoqItem(
            code="K1.2",
            description="Atterberg limits (liquid and plastic limit)",
            unit="nr",
            quantity=k1_2,
        ),
        BoqItem(
            code="K1.3",
            description="Particle size distribution (wet sieving)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.4",
            description="Particle size distribution (dry sieving)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.5",
            description="Particle size distribution (hydrometer / sedimentation)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.6",
            description="Particle density (specific gravity)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.7",
            description="Organic matter content (loss on ignition)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.8",
            description="pH value",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.9",
            description="Bulk density",
            unit="nr",
            quantity=k1_9,
        ),
        BoqItem(
            code="K1.10",
            description="Dry density",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.11",
            description="Hand penetrometer and hand vane on U100 sample",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.12",
            description="Unconsolidated undrained triaxial compression test (single stage)",
            unit="nr",
            quantity=k1_12,
        ),
        BoqItem(
            code="K1.13",
            description="Consolidated undrained triaxial compression test (multi-stage)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.14",
            description="Consolidated drained triaxial compression test (multi-stage)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.15",
            description="Direct shear test (small shear box)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.16",
            description="Direct shear test (large shear box)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.17",
            description="Residual shear test (ring shear)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.18",
            description="One-dimensional consolidation (oedometer) test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.19",
            description="Permeability test (constant head, triaxial cell)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.20",
            description="Permeability test (falling head, triaxial cell)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.21",
            description="Standard Proctor compaction test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.22",
            description="Modified Proctor compaction test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.23",
            description="California bearing ratio (CBR) test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.24",
            description="Frost heave susceptibility test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.25",
            description="Unconfined compressive strength (UCS) test on rock core",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.26",
            description="Point load strength index test on rock core",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.27",
            description="Brazilian tensile strength test on rock core",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.28",
            description="Slake durability test on rock core",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.29",
            description="Methylene blue absorption test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.30",
            description="Los Angeles abrasion test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.31",
            description="Aggregate impact value",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.32",
            description="Aggregate crushing value",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.33",
            description="Ten percent fines value",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.34",
            description="Flakiness index",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.35",
            description="Elongation index",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.36",
            description="Water absorption test on aggregate",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.37",
            description="Magnesium sulfate soundness test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.38",
            description="Petrographic description of rock core",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.39",
            description="Thin section petrography",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.40",
            description="X-ray diffraction (XRD) analysis",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.41",
            description="Thermal conductivity test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.42",
            description="Electrical resistivity test on soil sample",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.43",
            description="Sulphate content (2:1 water/soil extract, gravimetric)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.44",
            description="Sulphate content (total sulphate, acid extract)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.45",
            description="Chloride content",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.46",
            description="Carbonate content",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.47",
            description="Total sulfur content",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.48",
            description="Oxidisable sulfide content",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.49",
            description="Acid soluble sulfate",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.50",
            description="Water soluble sulfate",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.51",
            description="pH and aggressive CO₂ (BRE SD1)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.52",
            description="BRE special digest 1 — full suite",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.53",
            description="Organic content by dichromate oxidation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.54",
            description="Total organic carbon (TOC)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.55",
            description="Electrical resistivity of soil (saturated paste)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.56",
            description="Redox potential",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.57",
            description="Swelling pressure (oedometer)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.58",
            description="Free swell index",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.59",
            description="Linear shrinkage",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.60",
            description="Shrinkage limit",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.61",
            description="Dispersibility (pinhole test)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.62",
            description="Dispersibility (crumb test)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.63",
            description="Dispersibility (SCS double hydrometer test)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.64",
            description="Vane shear test on U100 sample",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.65",
            description="Fall cone test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.66",
            description="Consolidation test (Rowe cell)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.67",
            description="Compressibility index from oedometer test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.68",
            description="Coefficient of volume compressibility",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.69",
            description="Secondary compression index",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.70",
            description="Stress path triaxial test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.71",
            description="Cyclic triaxial test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.72",
            description="Bender element test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.73",
            description="Resonant column test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.74",
            description="Simple shear test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.75",
            description="Constant rate of strain (CRS) consolidation test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.76",
            description="Collapse potential test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.77",
            description="Soil suction measurement",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.78",
            description="Soil-water characteristic curve (SWCC)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.79",
            description="Minimum and maximum density (vibrating table)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.80",
            description="Relative density determination",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.81",
            description="Cone penetrometer test on U100 sample",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.82",
            description="Undrained shear strength from vane on U100",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.83",
            description="Pocket penetrometer on U100",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.84",
            description="Water content by oven drying (peat)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.85",
            description="Von Post classification of peat",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.86",
            description="Fibre content of peat",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.87",
            description="Ash content of peat",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.88",
            description="Decomposition degree of peat",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.89",
            description="Tensile strength of intact rock",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="K1.90",
            description="Additional geotechnical laboratory test (to be specified)",
            unit="nr",
            quantity="Not Required",
        ),
    ]
