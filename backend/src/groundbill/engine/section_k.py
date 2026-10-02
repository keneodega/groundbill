"""Section K — Geotechnical laboratory testing.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section K' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section K'.

Structure
---------
109 item rows in nine numbered groups. Unlike the other sections, the group
headings carry a code in column A, stored here as ``subheading_code``:

- K1  Classification
- K2  Chemical and electrochemical
- K3  Compaction related
- K4  Compressibility, permeability and durability
- K5  Consolidation and permeability in hydraulic cells (see note below)
- K6  Shear strength (total stress)
- K7  Shear strength (effective stress)
- K8  Rock testing
- K.9 Special tests on rock core or trial pit samples ... (written "K.9" in
  the Contractor workbook)

Formulas
--------
Only four cells are calculated; all four scale from the tub sample count
(Section E item E2, one sample per metre of hole):

- K1.1  ``='Section E'!D12``   moisture content: one per tub sample
  (Calculator note: "assumed 100% D samples are tested")
- K1.2  ``=0.5*(D11)``         liquid / plastic limit: half of K1.1
- K1.9  ``=0.25*(D11)``        wet sieving: a quarter of K1.1
- K1.12 ``=0.25*(D11)``        hydrometer: a quarter of K1.1

None of the results are rounded in the workbook, and none are rounded here.

Blank quantities
----------------
29 quantity cells are empty in the Calculator: K2.1, K2.3, K2.4, K2.5, K2.8,
K2.12, K3.1, K3.3, K3.6, K3.7, K3.9.1, K4.1, K4.2, K6.1-K6.10, K6.15, K6.17,
K7.1, K7.3, K8.14 and K8.18. They are emitted as ``None`` (decision of
2026-10-01): the engineer enters these by hand in the Excel system.

22 of those descriptions match test names on the Log Tracker's 'Lab
Schedules' sheet word for word, but no formula links the two, so
``Project.lab_schedule`` is not read here. Feeding these items from the lab
schedule would be a new rule rather than a translation.

All remaining items are the static text ``Not Required``.

Open items for review (by Havilah)
----------------------------------
Translated literally:

- **K1.2 factor.** The formula is ``=0.5*(D11)`` but the note beside it reads
  "assumed 25% D samples are tested". The formula (50%) is what is translated.
- **K5 is an item, not a heading.** Row 61 ("Consolidation and permeability
  in hydraulic cells") has a unit ("nr") and a quantity ("Not Required") in
  both workbooks, unlike the other group headings, so it is emitted as a BOQ
  item with code K5 and K5.1-K5.14 follow it without a sub-heading row.
- **K3.5 does not exist.** The numbering runs K3.4, K3.6.

Descriptions are verbatim, including the workbook's spacing and spellings
("K5. 1", "K6. 10", "individiual", "competant").
"""

from groundbill.models import Project

from .boq_items import BoqItem
from .section_e import e2_tub_sample_count

_NOT_REQUIRED = "Not Required"


def compute_section_k(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section K BOQ items for the given project."""

    # 'Section K'!D11: ='Section E'!D12
    k1_1 = e2_tub_sample_count(project)
    # 'Section K'!D12: =0.5*(D11)
    # Open item: the Calculator's note says 25%; the formula (50%) is translated.
    k1_2 = 0.5 * k1_1
    # 'Section K'!D19: =0.25*(D11)
    k1_9 = 0.25 * k1_1
    # 'Section K'!D22: =0.25*(D11)
    k1_12 = 0.25 * k1_1

    return [
        # 'Section K'!D11: ='Section E'!D12
        BoqItem(
            code="K1.1",
            description="Moisture content",
            unit="nr",
            quantity=k1_1,
            subheading="Classification",
            subheading_code="K1",
        ),
        # 'Section K'!D12: =0.5*(D11)
        BoqItem(
            code="K1.2",
            description="Liquid limit, plastic limit and plasticity index",
            unit="nr",
            quantity=k1_2,
        ),
        # 'Section K'!D13: Not Required
        BoqItem(
            code="K1.3",
            description="Volumetric shrinkage",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D14: Not Required
        BoqItem(
            code="K1.4",
            description="Linear shrinkage",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D15: Not Required
        BoqItem(
            code="K1.5",
            description="Density by linear measurement",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D16: Not Required
        BoqItem(
            code="K1.6",
            description="Density by immersion in water or water displacement",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D17: Not Required
        BoqItem(
            code="K1.7",
            description="Dry density and saturation moisture content for chalk",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D18: Not Required
        BoqItem(
            code="K1.8",
            description="Particle density by gas jar or pycnometer",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D19: =0.25*(D11)
        BoqItem(
            code="K1.9",
            description="Particle size distribution by wet sieving",
            unit="nr",
            quantity=k1_9,
        ),
        # 'Section K'!D20: Not Required
        BoqItem(
            code="K1.10",
            description="Particle size distribution by dry sieving",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D21: Not Required
        BoqItem(
            code="K1.11",
            description="Sedimentation by pipette",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D22: =0.25*(D11)
        BoqItem(
            code="K1.12",
            description="Sedimentation by hydrometer",
            unit="nr",
            quantity=k1_12,
        ),
        # 'Section K'!D24: (blank)
        BoqItem(
            code="K2.1",
            description="Organic matter content",
            unit="nr",
            quantity=None,
            subheading="Chemical and electrochemical",
            subheading_code="K2",
        ),
        # 'Section K'!D25: Not Required
        BoqItem(
            code="K2.2",
            description="Mass loss on ignition",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D26: (blank)
        BoqItem(
            code="K2.3",
            description="Sulphate content of acid extract from soil",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D27: (blank)
        BoqItem(
            code="K2.4",
            description="Sulphate content of water extract from soil",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D28: (blank)
        BoqItem(
            code="K2.5",
            description="Sulphate content of groundwater",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D29: Not Required
        BoqItem(
            code="K2.6",
            description="Carbonate content by rapid titration",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D30: Not Required
        BoqItem(
            code="K2.7",
            description="Carbonate content by gravimetric method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D31: (blank)
        BoqItem(
            code="K2.8",
            description="Water soluble chloride content",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D32: Not Required
        BoqItem(
            code="K2.9",
            description="Acid soluble chloride content",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D33: Not Required
        BoqItem(
            code="K2.10",
            description="Total sulphur content",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D34: Not Required
        BoqItem(
            code="K2.11",
            description="Total dissolved solids",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D35: (blank)
        BoqItem(
            code="K2.12",
            description="pH value",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D36: Not Required
        BoqItem(
            code="K2.13",
            description="Resistivity",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D37: Not Required
        BoqItem(
            code="K2.14",
            description="Redox potential",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D39: (blank)
        BoqItem(
            code="K3.1",
            description="Dry density/moisture content relationship using 2.5 kg rammer",
            unit="nr",
            quantity=None,
            subheading="Compaction related",
            subheading_code="K3",
        ),
        # 'Section K'!D40: Not Required
        BoqItem(
            code="K3.2",
            description="Dry density/moisture content relationship using 4.5 kg rammer",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D41: (blank)
        BoqItem(
            code="K3.3",
            description="Dry density/moisture content relationship using vibrating hammer",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D42: Not Required
        BoqItem(
            code="K3.4",
            description="Extra over Items K3.1, K3.2 and K3.3 for use of CBR mould",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D43: (blank)
        BoqItem(
            code="K3.6",
            description="Moisture Condition Value at natural moisture content",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D44: (blank)
        BoqItem(
            code="K3.7",
            description="Moisture Condition Value/moisture content relationship (five points)",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D45: Not Required
        BoqItem(
            code="K3.8",
            description="Chalk crushing value",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D46: Not Required
        BoqItem(
            code="K3.9",
            description="California Bearing Ratio on re-compacted disturbed sample",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D47: (blank)
        BoqItem(
            code="K3.9.1",
            description="Extra over for recompacting a soil sample to a specified moisture content",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D48: Not Required
        BoqItem(
            code="K3.10",
            description="Extra over Item K3.9 for soaking",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D50: (blank)
        BoqItem(
            code="K4.1",
            description="One-dimensional consolidation properties, test period 5 days",
            unit="nr",
            quantity=None,
            subheading="Compressibility, permeability and durability",
            subheading_code="K4",
        ),
        # 'Section K'!D51: (blank)
        BoqItem(
            code="K4.2",
            description="Extra over Item K4.1 for test period in excess of 5 days",
            unit="day",
            quantity=None,
        ),
        # 'Section K'!D52: Not Required
        BoqItem(
            code="K4.3",
            description="Measurements of swelling pressure, test period 2 days",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D53: Not Required
        BoqItem(
            code="K4.4",
            description="Measurement of swelling, test period 2 days",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D54: Not Required
        BoqItem(
            code="K4.5",
            description="Measurement of settlement on saturation, test period 1 day",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D55: Not Required
        BoqItem(
            code="K4.6",
            description="Extra over Items K4.3 to K4.5 for test period in excess of 2 or 1 day (s)",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D56: Not Required
        BoqItem(
            code="K4.7",
            description="Permeability by constant head method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D57: Not Required
        BoqItem(
            code="K4.8",
            description="Dispersibility by pinhole method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D58: Not Required
        BoqItem(
            code="K4.9",
            description="Dispersibility by crumb method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D59: Not Required
        BoqItem(
            code="K4.10",
            description="Dispersibility by dispersion method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D60: Not Required
        BoqItem(
            code="K4.11",
            description="Frost heave of soil",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D61: Not Required
        BoqItem(
            code="K5",
            description="Consolidation and permeability in hydraulic cells",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D62: Not Required
        BoqItem(
            code="K5.1",
            description=(
                "Consolidation properties of a 76mm diameter specimen using a "
                "hydraulic cell, test period 4 days"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D63: Not Required
        BoqItem(
            code="K5.2",
            description="As Item K5.1 but using a 100mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D64: Not Required
        BoqItem(
            code="K5.3",
            description="As Item K5.1 but using a 150mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D65: Not Required
        BoqItem(
            code="K5.4",
            description="As Item K5.1 but using a 250mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D66: Not Required
        BoqItem(
            code="K5.5",
            description="Extra over Items K5. 1 to K5.4 for test period in excess of 4 days",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D67: Not Required
        BoqItem(
            code="K5.6",
            description=(
                "Permeability of a 76mm diameter specimen in hydraulic consolidation "
                "cell, test period 4 days"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D68: Not Required
        BoqItem(
            code="K5.7",
            description="As Item K5.6 but using a 100mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D69: Not Required
        BoqItem(
            code="K5.8",
            description="As Item K5.6 but using a 150mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D70: Not Required
        BoqItem(
            code="K5.9",
            description="As Item K5.6 but using a 250mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D71: Not Required
        BoqItem(
            code="K5.10",
            description="Extra over Items K5.6 to K5.9 for test period in excess of 4 days",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D72: Not Required
        BoqItem(
            code="K5.11",
            description="Isotropic consolidation properties in a triaxial cell, test period 4 days",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D73: Not Required
        BoqItem(
            code="K5.12",
            description="Extra over Item K5.11 for test periods in excess of 4 days",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D74: Not Required
        BoqItem(
            code="K5.13",
            description="Permeability in a triaxial cell, test period 4 days",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D75: Not Required
        BoqItem(
            code="K5.14",
            description="Extra over Item K5.13 for test period in excess of 4 days",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D77: (blank)
        BoqItem(
            code="K6.1",
            description="Shear strength by the laboratory vane method (set of 3)",
            unit="nr",
            quantity=None,
            subheading="Shear strength (total stress)",
            subheading_code="K6",
        ),
        # 'Section K'!D78: (blank)
        BoqItem(
            code="K6.2",
            description="Shear strength by hand vane (set of 3)",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D79: (blank)
        BoqItem(
            code="K6.3",
            description="Shear strength by hand penetrometer (set of 3)",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D80: (blank)
        BoqItem(
            code="K6.4",
            description=(
                "Shear strength of a set of three 60mm × 60mm square specimens by "
                "direct shear, test duration not exceeding 1 day per specimen"
            ),
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D81: (blank)
        BoqItem(
            code="K6.5",
            description="Extra over Item K6.4 for test durations in excess of 1 day per specimen",
            unit="sp.day",
            quantity=None,
        ),
        # 'Section K'!D82: (blank)
        BoqItem(
            code="K6.6",
            description=(
                "Shear strength of a single 300mm × 300mm square specimen by direct "
                "shear, test duration not exceeding 1 day"
            ),
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D83: (blank)
        BoqItem(
            code="K6.7",
            description="Extra over Item K6.6 for test durations in excess of 1 day",
            unit="day",
            quantity=None,
        ),
        # 'Section K'!D84: (blank)
        BoqItem(
            code="K6.8",
            description=(
                "Residual shear strength of a set of three 60mm × 60mm square "
                "specimens by direct shear, test duration not exceeding 4 days per "
                "specimen"
            ),
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D85: (blank)
        BoqItem(
            code="K6.9",
            description="Extra over Item K6.8 for test durations in excess of 4 days per specimen",
            unit="sp.day",
            quantity=None,
        ),
        # 'Section K'!D86: (blank)
        BoqItem(
            code="K6.10",
            description=(
                "Residual shear strength of a 300mm square specimen by direct shear, "
                "test duration not exceeding 4 days"
            ),
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D87: Not Required
        BoqItem(
            code="K6.11",
            description="Extra over Item K6. 10 for test duration in excess day of 4 days",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D88: Not Required
        BoqItem(
            code="K6.12",
            description=(
                "Residual shear strength using the small ring shear apparatus at "
                "three normal pressures, test duration not exceeding 4 days"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D89: Not Required
        BoqItem(
            code="K6.13",
            description="Extra over Item K6.12 for test duration in excess of 4 days",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D90: Not Required
        BoqItem(
            code="K6.14",
            description="Unconfined compressive strength of 38mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D91: (blank)
        BoqItem(
            code="K6.15",
            description=(
                "Undrained shear strength of a set of three 38mm diameter specimens "
                "in triaxial compression without the measurement of pore pressure"
            ),
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D92: Not Required
        BoqItem(
            code="K6.16",
            description=(
                "Undrained strength of a single 100mm diameter specimen in triaxial "
                "compression without the measurement of pore pressure"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D93: (blank)
        BoqItem(
            code="K6.17",
            description=(
                "Undrained shear strength of a single 100mm diameter specimen in "
                "triaxial compression with multi-stage loading and without "
                "measurement of pore pressure"
            ),
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D95: (blank)
        BoqItem(
            code="K7.1",
            description=(
                "Consolidated undrained triaxial compression test with measurement of"
                " pore pressure (set of three 38mm specimens), test duration not "
                "exceeding 4 days per specimen"
            ),
            unit="nr",
            quantity=None,
            subheading="Shear strength (effective stress)",
            subheading_code="K7",
        ),
        # 'Section K'!D96: Not Required
        BoqItem(
            code="K7.2",
            description="As K7.1 but single-stage or multi-stage test using 100mm diameter specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D97: (blank)
        BoqItem(
            code="K7.3",
            description=(
                "Consolidated drained triaxial compression test with measurement of "
                "volume change (set of three 38mm specimens), test duration not "
                "exceeding 4 days per specimen"
            ),
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D98: Not Required
        BoqItem(
            code="K7.4",
            description=(
                "As Item K7.3 but single-stage or multi-stage test using 100mm "
                "diameter specimen, test duration not exceeding 4 days"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D99: Not Required
        BoqItem(
            code="K7.5",
            description=(
                "Extra over Items K7.1 and K7.3 for test duration in excess of 4 days"
                " per specimen"
            ),
            unit="sp.day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D100: Not Required
        BoqItem(
            code="K7.6",
            description="Extra over Items K7.2 and K7.4 for test duration in excess of 4 days",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D102: Not Required
        BoqItem(
            code="K8.1",
            description="Natural water content of rock sample",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Rock testing",
            subheading_code="K8",
        ),
        # 'Section K'!D103: Not Required
        BoqItem(
            code="K8.2",
            description="Porosity/density using saturation and calliper techniques",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D104: Not Required
        BoqItem(
            code="K8.3",
            description="Porosity/density using saturation and buoyancy",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D105: Not Required
        BoqItem(
            code="K8.4",
            description="Slake durability index",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D106: Not Required
        BoqItem(
            code="K8.5",
            description="Soundness by magnesium sulphate",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D107: Not Required
        BoqItem(
            code="K8.6",
            description="Magnesium sulphate test",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D108: Not Required
        BoqItem(
            code="K8.7",
            description="Shore scleroscope",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D109: Not Required
        BoqItem(
            code="K8.8",
            description="Schmidt rebound hardness",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D110: Not Required
        BoqItem(
            code="K8.9",
            description="Resistance to fragmentation",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D111: Not Required
        BoqItem(
            code="K8.10",
            description="Aggregate abrasion value",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D112: Not Required
        BoqItem(
            code="K8.11",
            description="Polished stone value",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D113: Not Required
        BoqItem(
            code="K8.12",
            description="Aggregate frost heave",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D114: Not Required
        BoqItem(
            code="K8.13",
            description="Resistance to freezing and thawing",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D115: (blank)
        BoqItem(
            code="K8.14",
            description="Uniaxial compressive strength",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D116: Not Required
        BoqItem(
            code="K8.15",
            description="Deformability in uniaxial compression",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D117: Not Required
        BoqItem(
            code="K8.16",
            description="Indirect tensile strength by Brazilian test",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D118: Not Required
        BoqItem(
            code="K8.17",
            description="Triaxial compression without measurements of porewater pressure",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D119: (blank)
        BoqItem(
            code="K8.18",
            description="Point Load Strength Index on rock core (axial or diametral)",
            unit="nr",
            quantity=None,
        ),
        # 'Section K'!D120: Not Required
        BoqItem(
            code="K8.19",
            description=(
                "Point load strength index on irregular lump sample (set of ten "
                "individiual determinations)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D121: Not Required
        BoqItem(
            code="K8.20",
            description="Swelling pressure test",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D122: Not Required
        BoqItem(
            code="K8.21",
            description="Direct shear strength of single specimen",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D124: Not Required
        BoqItem(
            code="K9.1",
            description=(
                "Geological classification / simplified petrography on rock core or "
                "bulk samples to IS EN 933 ( by Professional Geologist)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading=(
                "Special tests on rock core or trial pit samples to assess potential "
                "for pyrite induced expansion or swelling"
            ),
            subheading_code="K.9",
        ),
        # 'Section K'!D125: Not Required
        BoqItem(
            code="K9.2",
            description=(
                "Chemical analysis on rock core or bulk sample (test methods to TRL "
                "447 and test suite to include Total Sulphur, Acid Soluble Sulphate &"
                " Water Soluble Sulphate and derivation of Oxidisable Sulphide & "
                "Equivalent Pyrite Content)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section K'!D126: Not Required
        BoqItem(
            code="K9.3",
            description=(
                "Thin section petrography and XRD analysis on rock core or bulk "
                "sample. Analysis to be carried out by Professional Geologist or "
                "experienced Petrographer competant in evaluating potential for "
                "pyrite induced swelling. Note the rate should include for thin "
                "section preparation and XRD analysis on one lithology."
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
    ]
