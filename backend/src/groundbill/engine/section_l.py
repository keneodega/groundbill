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

The E12 count is computed locally by ``_e12_environmental_sample_count`` so
this module does not depend on Section E's module.

Rows deliberately not translated
--------------------------------
- The Calculator has an extra row 17, "L.7 Tests Suite K", with a blank
  quantity. It does not appear in the Contractor workbook, so it is omitted.

Descriptions are verbatim, including the unbalanced bracket at the end of the
sub-heading.
"""

from groundbill.models import InSituTest, Project, PSEVTest

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"


def compute_section_l(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section L BOQ items for the given project."""

    e12 = _e12_environmental_sample_count(project)
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


def _e12_environmental_sample_count(project: Project) -> int:
    """Count exploratory holes with "EV" in their test selection (Section E item E12).

    'Section E'!D25:
    =COUNTIF('[1]Trial Pits'!$J$2:$J91,"*EV*")
     +COUNTIF('[1]Inspection pit'!$K$2:$K91,"*EV*")
     +COUNTIF([1]Trenches!$G$3:$G92,"*EV*")
     +COUNTIF([1]Boreholes!$G$2:$G91,"*EV*")
     +COUNTIF('[1]Dynamic Sampling'!$J$2:$J91,"*EV*")

    The ``*EV*`` wildcard matches any cell containing "EV", so a combined
    selection such as "DCP/EV" still counts once. In the Python model each
    hole holds a set of tests, so the equivalent check is "EV is in the set".
    """
    return (
        sum(1 for tp in project.trial_pits if InSituTest.EV in tp.in_situ_tests)
        + sum(1 for ip in project.inspection_pits if InSituTest.EV in ip.in_situ_tests)
        + sum(1 for t in project.trenches if InSituTest.EV in t.in_situ_tests)
        + sum(1 for bh in project.boreholes if PSEVTest.EV in bh.tests)
        + sum(1 for ds in project.dynamic_samples if PSEVTest.EV in ds.tests)
    )
