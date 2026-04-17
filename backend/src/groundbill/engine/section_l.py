"""Section L — Geoenvironmental Laboratory Testing.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section L'
(with cross-references to the Log Tracker workbook's `Boreholes`, `Trial Pits`,
`Trenches`, `Inspection pit`, and `Dynamic Sampling` sheets).

Key formulas
============
L.1 = E12 / 5  (EV test count ÷ 5)
L.5 = E16 / 5  (same as L.1, since E16 = E12)

E12 (EV test count) is computed inline to avoid circular dependency with
Section E.

Static items: L.2–L.4, L.6, L.7 — "Not Required".
"""

from groundbill.models import InSituTest, Project, PSEVTest

from .boq_items import BoqItem


def compute_section_l(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section L BOQ items for the given project."""

    # Compute E12 inline (count of holes with EV test selection)
    ev_count = 0
    ev_count += sum(1 for tp in project.trial_pits if InSituTest.EV in tp.in_situ_tests)
    ev_count += sum(1 for ip in project.inspection_pits if InSituTest.EV in ip.in_situ_tests)
    ev_count += sum(1 for t in project.trenches if InSituTest.EV in t.in_situ_tests)
    ev_count += sum(1 for bh in project.boreholes if PSEVTest.EV in bh.tests)
    ev_count += sum(1 for ds in project.dynamic_samples if PSEVTest.EV in ds.tests)

    l_1 = ev_count / 5 if ev_count else 0
    l_5 = l_1  # E16 = E12

    return [
        BoqItem(
            code="L.1",
            description="Suite A — chemical testing of soil samples",
            unit="nr",
            quantity=l_1,
        ),
        BoqItem(
            code="L.2",
            description="Suite B — waste acceptance criteria (WAC) testing",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="L.3",
            description="Suite C — asbestos in soil screening",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="L.4",
            description="Suite D — additional chemical testing",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="L.5",
            description="Suite E — groundwater chemical analysis",
            unit="nr",
            quantity=l_5,
        ),
        BoqItem(
            code="L.6",
            description="Suite F — leachate testing",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="L.7",
            description="Additional geoenvironmental laboratory test (to be specified)",
            unit="nr",
            quantity="Not Required",
        ),
    ]
