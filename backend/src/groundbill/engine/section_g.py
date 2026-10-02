"""Section G — Geophysical testing.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section G' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section G'.

Every quantity cell in the Calculator (D11:D15, D17:D19, D21:D22) holds the
static text ``Not Required`` — there are no formulas in this section and
nothing is read from the Log Tracker.

Descriptions are verbatim, including the workbook's own typos ("[rocess" in
G5, lower-case "conduct" in G10), so that the output matches the reference
row for row.

Rows deliberately not translated
--------------------------------
- Row 23 ("Contract specific additional bill items") is a trailing label in
  column A with no items beneath it.
- Calculator row 24 holds a unit ("day") and "Not Required" with no item code
  or description; it does not appear in the Contractor workbook.
"""

from groundbill.models import Project

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"


def compute_section_g(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section G BOQ items for the given project."""

    return [
        # 'Section G'!D11: Not Required
        BoqItem(
            code="G1",
            description=(
                "Conduct and process Ground Penetrating Radar (GPR) profiles to "
                "PAS 128 QL B1P as per the specification"
            ),
            unit="m²",
            quantity=_NOT_REQUIRED,
            subheading="Land-based mapping techniques",
        ),
        # 'Section G'!D12: Not Required
        BoqItem(
            code="G2",
            description="Conduct and process electro magnetic conductivity (EMC) profiles",
            unit="ln m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section G'!D13: Not Required
        BoqItem(
            code="G3",
            description="Conduct and process electrical resistivity tomography (ERT) profiles",
            unit="ln m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section G'!D14: Not Required
        BoqItem(
            code="G4",
            description="Conduct and process seismic refraction spreads (P or S wave)",
            unit="ln m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section G'!D15: Not Required
        BoqItem(
            code="G5",
            description="Conduct and [rocess surface wave spreads (1D or 2D MASW)",
            unit="ln m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section G'!D17: Not Required
        BoqItem(
            code="G6",
            description=(
                "Establish down-hole geophysical logging equipment and personnel to "
                "the site of each exploratory hole and set up at each location"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
            subheading="Borehole geophysical surveying",
        ),
        # 'Section G'!D18: Not Required
        BoqItem(
            code="G7",
            description=(
                "Conduct and process down the hole calliper, natural gamma, "
                "resistivity, sonic, fluid, temperature, conductivity, and fluid "
                "flow logging"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section G'!D19: Not Required
        BoqItem(
            code="G8",
            description="Conduct and process cross-hole seismic readings at specified intervals",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section G'!D21: Not Required
        BoqItem(
            code="G9",
            description=(
                "Establish geophysical personnel and field equipment and "
                "demobilisation on completion"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
            subheading="Marine (overwater) geophysical surveying",
        ),
        # 'Section G'!D22: Not Required
        BoqItem(
            code="G10",
            description=(
                "conduct and process echo sounding, side scan sonar, magnetic, "
                "sub-bottom profile surveying"
            ),
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
    ]
