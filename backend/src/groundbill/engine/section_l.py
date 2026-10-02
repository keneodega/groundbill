"""Section L — Geoenvironmental laboratory testing.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section L' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section L'.

Formulas
--------
- L.1 (Tests Suite E) ``='Section E'!D25/5``
- L.5 (Tests Suite I) ``='Section E'!D29/5``
- L.2, L.3, L.4, L.6 are the static text ``Not Required``.

Both formulas point at Section E of the Calculator:

- 'Section E'!D25 is item E12, the number of exploratory holes whose test
  selection contains "EV" (environmental sampling), counted across trial pits,
  inspection pits, trenches, boreholes and dynamic sampling holes.
- 'Section E'!D29 is item E16, whose formula is simply ``=D25``.

So one laboratory suite is scheduled for every five environmental samples.
The result is not rounded in the workbook and is not rounded here (6 samples
give 1.2).

The E12 count is imported from the Section E module, mirroring the
Calculator's own cross-sheet reference, so the rule lives in one place.

Rows deliberately not translated
--------------------------------
- The Calculator has an extra row 17, "L.7 Tests Suite K", with a blank
  quantity. It does not appear in the Contractor workbook, so it is omitted.

Descriptions are verbatim, including the unbalanced bracket at the end of the
sub-heading.
"""

from groundbill.models import Project

from .boq_items import BoqItem
from .section_e import e12_environmental_sample_count

_NOT_REQUIRED = "Not Required"


def compute_section_l(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section L BOQ items for the given project."""

    # 'Section E'!D25 (E12): count of holes with "EV" selected
    e12 = e12_environmental_sample_count(project)
    # 'Section E'!D29 (E16): =D25
    e16 = e12

    # 'Section L'!D11: ='Section E'!D25/5
    l_1 = e12 / 5
    # 'Section L'!D15: ='Section E'!D29/5
    l_5 = e16 / 5

    return [
        # 'Section L'!D11: ='Section E'!D25/5
        BoqItem(
            code="L.1",
            description="Tests Suite E",
            unit="nr",
            quantity=l_1,
            subheading="Contamination testing of soil, groundwater, gas and fill material)",
        ),
        # 'Section L'!D12: Not Required
        BoqItem(
            code="L.2",
            description="Tests Suite F",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section L'!D13: Not Required
        BoqItem(
            code="L.3",
            description="Tests Suite G",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section L'!D14: Not Required
        BoqItem(
            code="L.4",
            description="Tests Suite H",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section L'!D15: ='Section E'!D29/5
        BoqItem(
            code="L.5",
            description="Tests Suite I",
            unit="nr",
            quantity=l_5,
        ),
        # 'Section L'!D16: Not Required
        BoqItem(
            code="L.6",
            description="Tests Suite J",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
    ]
