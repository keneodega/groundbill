"""Section A — General items, provisional services and additional items.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section A'.
The Calculator holds the authoritative item inventory. Only two live formulas
exist in the source: cell D35 (item A8, set-out points) and D36 (item A8.1,
which is simply ``=D35``). All other item quantities are static placeholders
entered manually at tender time.

Site-category handling:
- GREEN sites emit A1, A2 and A2.1-A2.9 only (no A3/A4/A5 extras).
- YELLOW sites additionally emit A3.1, A4.1, A5.1.
- RED sites additionally emit A3.2, A4.2, A5.2.

"Scheduled" is treated as list membership: each hole present in the project is
considered scheduled, which matches the Log Tracker's own ``=IF(A="","",1)``
convention and resolves the Excel's scheduled-vs-completed inconsistency in
favour of a single consistent rule.
"""

from groundbill.models import Project, SiteCategory

from .boq_items import BoqItem

_CATEGORY_LABEL = {
    SiteCategory.GREEN: "Green",
    SiteCategory.YELLOW: "Yellow",
    SiteCategory.RED: "Red",
}


def compute_section_a(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section A BOQ items for the given project."""

    cat = _CATEGORY_LABEL[project.site_category]
    a8_count = _count_set_out_points(project)

    items: list[BoqItem] = [
        BoqItem(
            code="A1",
            description="Offices and stores for the Contractor",
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2",
            description=(
                f"Establish on site all plant, equipment and services " f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.1",
            description=(
                f"Establish on site cable percussion ('shell & auger') boring plant "
                f"and equipment for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.2",
            description=(
                f"Establish on site rotary drilling plant and equipment "
                f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.3",
            description=(
                f"Establish on site Geobor S rotary drilling plant and equipment "
                f"for a {cat} Category site (PROVISIONAL)"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.4",
            description=(
                f"Establish on site trial pitting and trenching plant and equipment "
                f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.5",
            description=(
                f"Establish on site in situ test and sampling equipment "
                f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.6",
            description=(
                f"Establish on site cone penetration testing (CPT) plant and equipment "
                f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.7",
            description=(
                f"Establish on site dynamic sampling and probing plant and equipment "
                f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.8",
            description=(
                f"Establish on site geophysical survey equipment " f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
        BoqItem(
            code="A2.9",
            description=(
                f"Establish on site instrumentation equipment as required "
                f"for a {cat} Category site"
            ),
            unit="sum",
            quantity="Not Required",
        ),
    ]

    if project.site_category is SiteCategory.YELLOW:
        items.extend(
            [
                BoqItem(
                    code="A3.1",
                    description="Extra over item A2.1 - A2.9 for a Yellow Category site (Provisional)",
                    unit="provisional sum",
                    quantity="Not Required",
                ),
                BoqItem(
                    code="A4.1",
                    description="Maintain on site all site safety equipment for a Yellow Category site (PROVISIONAL)",
                    unit="provisional sum",
                    quantity="Not Required",
                ),
                BoqItem(
                    code="A5.1",
                    description="Decontamination of equipment during and at end of intrusive investigation for a Yellow Category site (PROVISIONAL)",
                    unit="provisional sum",
                    quantity="Not Required",
                ),
            ]
        )
    elif project.site_category is SiteCategory.RED:
        items.extend(
            [
                BoqItem(
                    code="A3.2",
                    description="Extra over item A2.1 - A2.9 for a Red Category site (Provisional)",
                    unit="provisional sum",
                    quantity="Not Required",
                ),
                BoqItem(
                    code="A4.2",
                    description="Maintain on site all site safety equipment for a Red Category site",
                    unit="provisional sum",
                    quantity="Not Required",
                ),
                BoqItem(
                    code="A5.2",
                    description="Decontamination of equipment during and at end of intrusive investigation for a Red Category site",
                    unit="provisional sum",
                    quantity="Not Required",
                ),
            ]
        )

    items.extend(
        [
            BoqItem(
                code="A6",
                description=(
                    "Appropriate storage, transport and off-site disposal of excess "
                    "contaminated arising's from borehole, trial pit or slit trench"
                ),
                unit="provisional sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A6.1",
                description="Contractor's uplift on Item A6",
                unit="%",
                quantity="Not Required",
            ),
            BoqItem(
                code="A7",
                description="Provide professional attendance to meet the contract requirements",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A7.1",
                description="Provide Technician",
                unit="per day",
                quantity="Included in A7",
            ),
            BoqItem(
                code="A7.2",
                description="Provide Engineer / Geologist (as per item 2.3 of Specification)",
                unit="per day",
                quantity="Included in A7",
            ),
            BoqItem(
                code="A7.3",
                description="Provide Chartered Engineer / Professional Geologist (as item 2.3 of Specification)",
                unit="per day",
                quantity="Included in A7",
            ),
            BoqItem(
                code="A7.4",
                description="Provide Chartered Engineer / Professional Geologist (+10 years experience post charter)",
                unit="per day",
                quantity="Included in A7",
            ),
            BoqItem(
                code="A7.5",
                description="Provide Chartered Engineer / Professional Geologist (+20 years experience post charter)",
                unit="per day",
                quantity="Included in A7",
            ),
            # --- A8: the only computed item in Section A ---
            # Calculator!D35 =
            #   Boreholes!E92              (SUM of 'Scheduled' column)
            # + 'Trial Pits'!G92           (SUM of 'Scheduled' column)
            # + 2 * Trenches!K93           (SUM of 'completed' column, × 2 for endpoints)
            # + 'Inspection pit'!H92       (SUM of 'Completed' column)
            # + DPH!H122                   (SUM of 'Completed' column)
            # + CPT!K92                    (SUM of 'Completed' column)
            # + 'Dynamic Sampling'!H92     (SUM of 'Completed' column)
            # + 'Soakaway (BRE)'!E52       (SUM of 'Completed' column)
            BoqItem(
                code="A8",
                description="Set out the location at each exploratory hole or point",
                unit="Nr",
                quantity=a8_count,
            ),
            # Calculator!D36 = D35 (same count as A8)
            BoqItem(
                code="A8.1",
                description=(
                    "Establish the location and elevation (X, Y, Z) of the ground "
                    "at each 'as-built' exploratory hole or point"
                ),
                unit="nr",
                quantity=a8_count,
            ),
            BoqItem(
                code="A9",
                description="Preparation of Health and Safety documentation and Safety Risk Assessment",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A10",
                description="Facilities for the Investigation Supervisor",
                unit="per week",
                quantity="Not Required",
            ),
            BoqItem(
                code="A11",
                description="Vehicle(s) for the Investigation Supervisor",
                unit="vehicle wk",
                quantity="Not Required",
            ),
            BoqItem(
                code="A11.1",
                description="Provision of fuel and tolls for A11 (to be reimbursed under the contract)",
                unit="provisional sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A11.2",
                description="Contractor's uplift on item A11 and A11.1",
                unit="% uplift",
                quantity="Not Required",
            ),
            BoqItem(
                code="A12",
                description="Provision of phone and internet for the Investigation Supervisor (to be reimbursed under the contract)",
                unit="provisional sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A12.1",
                description="Contractor's uplift on item A12",
                unit="% uplift",
                quantity="Not Required",
            ),
            BoqItem(
                code="A13",
                description="Deliver selected cores and samples to specified Client address (address to be advised)",
                unit="provisional sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A14",
                description="Special additional testing and sampling required by Investigation Supervisor",
                unit="provisional sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A15",
                description=(
                    "Traffic safety and management to include preparation of traffic "
                    "management drawings for investigations on roads or paths"
                ),
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A16",
                description="Provision of road opening licences and road damage bonds",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A17",
                description="Contractor's uplift on items A15 and A16",
                unit="% uplift",
                quantity="Not Required",
            ),
            BoqItem(
                code="A18",
                description="One master copy of Desk Study Report",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A18.1",
                description="Additional hard copy of Desk Study Report",
                unit="nr",
                quantity="Not Required",
            ),
            BoqItem(
                code="A18.2",
                description="Electronic copy of Desk Study Report (PDF)",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A19",
                description="One master copy of the Ground Investigation Report (Factual)",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A19.1",
                description="Additional copy of the Ground Investigation Report (Factual)",
                unit="nr",
                quantity="Not Required",
            ),
            BoqItem(
                code="A19.2",
                description="Electronic copy of Ground Investigation Report",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A20",
                description="One master copy of Geophysical Report",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A20.1",
                description="Additional hard copy of Geophysical Report",
                unit="nr",
                quantity="Not Required",
            ),
            BoqItem(
                code="A20.2",
                description="Electronic copy of Geophysical Report (PDF)",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A21",
                description="One master copy of Geotechnical Interpretive Report",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A21.1",
                description="Additional copy of Geotechnical Interpretive Report",
                unit="nr",
                quantity="Not Required",
            ),
            BoqItem(
                code="A21.2",
                description="Electronic copy of Geotechnical Interpretive Report",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A22",
                description="Digital field / engineering logs in AGS transfer format",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A23",
                description="Digital laboratory test data in AGS transfer files",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A24",
                description="Digital copy of trial pit, slit trench or core photographs as per Specification",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A25",
                description="Storage of all samples following completion of fieldworks",
                unit="wk",
                quantity="Not Required",
            ),
            BoqItem(
                code="A26",
                description="Storage of core boxes following completion of fieldworks",
                unit="wk",
                quantity=None,
            ),
            BoqItem(
                code="A27",
                description="Provision of water supply for the fieldworks",
                unit="sum",
                quantity="included in A2",
            ),
            BoqItem(
                code="A28",
                description="Provision of Insurances",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A29",
                description="Provision of Performance Bond",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A30",
                description="Perform the role of PSCS",
                unit="sum",
                quantity="Not Required",
            ),
            BoqItem(
                code="A31",
                description=(
                    "Contractor liaison with external bodies to obtain road opening "
                    "licence, foreshore licence for marine investigations etc."
                ),
                unit="sum",
                quantity="Not Required",
            ),
        ]
    )

    return items


def _count_set_out_points(project: Project) -> int:
    """A8 quantity — total number of exploratory points to set out.

    Each hole listed in the project is treated as scheduled. Trenches count
    twice because a slit trench has two endpoints requiring set-out.
    """
    return (
        len(project.boreholes)
        + len(project.trial_pits)
        + 2 * len(project.trenches)
        + len(project.inspection_pits)
        + len(project.dynamic_probes)
        + len(project.cpts)
        + len(project.dynamic_samples)
        + len(project.soakaways)
    )
