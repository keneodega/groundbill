"""Section A — General items, provisional services and additional items.

Item codes, descriptions and units are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section A' (the issued
document); quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section A'. Only two live
formulas exist in the source: cell D35 (item A8, set-out points) and D36 (item
A8.1, which is simply ``=D35``). All other item quantities are static
placeholders entered manually at tender time.

Site category (decision of 2026-10-01)
--------------------------------------
Section A is the same for every site category, exactly as in the workbooks:

- A2-A2.9 always read "for a Green Category site". They are the base
  establishment items.
- A3.1-A5.2 (the Yellow and Red extra-overs, safety equipment and
  decontamination) are always listed, each "Not Required".

A3.1 is worded "Extra over item A2.1 - A2.9 for a yellow category site", so
the extra cost of a Yellow or Red site is priced through A3-A5 on top of the
Green base items. The engineer adjusts those rows on the bill for each job, as
in the Excel system (the Quantities workbook shows them edited by hand). The
project's ``site_category`` therefore does not change any Section A item.

Set-out points (A8)
-------------------
A8 adds one total from each Log Tracker sheet. Some sheets total a
"Scheduled" column and others a "Completed" column; all of those columns are
formulas, translated here as follows:

==========================  ===================  ==========================
Log Tracker cell            Column formula       Counts
==========================  ===================  ==========================
``Boreholes!E92``           ``IF(A2="","",1)``   every borehole listed
``'Trial Pits'!G92``        ``IF(H2>0,1,0)``     every trial pit listed (a
                                                 schedule depth is required)
``2*Trenches!K93``          ``IF(J3>0,1,0)``     trenches with a recorded
                                                 total depth, × 2 (two ends)
``'Inspection pit'!H92``    ``IF(E2>0,1,0)``     inspection pits with a
                                                 recorded depth
``DPH!H122``                ``IF(C2>0,1,0)``     every probe listed
``CPT!K92``                 ``IF(D2>0,1,0)``     every CPT listed
``'Dynamic Sampling'!H92``  ``IF(C2>0,1,0)``     every dynamic sample listed
``'Soakaway (BRE)'!E52``    ``IF(I2>0, 1, 0)``   soakaways with a recorded
                                                 depth
==========================  ===================  ==========================

The model requires a depth for probes, CPTs and dynamic samples and a
schedule depth for trial pits, so those always count. Trenches, inspection
pits and soakaways count only once their recorded depth has been entered.

Deliberate deviation (agreed 2026-10-01): ``'Inspection pit'!H92`` is
``=SUM(H65:H91)``; all inspection pits are counted, as in Sections D and E.
"""

from groundbill.models import InspectionPit, Project, Soakaway, Trench

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"


def compute_section_a(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section A BOQ items for the given project."""

    # 'Section A'!D35 — full formula quoted in _count_set_out_points
    a8 = _count_set_out_points(project)
    # 'Section A'!D36: =D35
    a8_1 = a8

    return [
        # 'Section A'!D10: Not Required
        BoqItem(
            code="A1",
            description="Offices and stores for the Contractor",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D11: Not Required
        BoqItem(
            code="A2",
            description=(
                "Establish on site all plant, equipment and services for a Green " "Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D12: Not Required
        BoqItem(
            code="A2.1",
            description=(
                "Establish on site cable percussion ('shell l auger') boring plant "
                "and equipment for a Green Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D13: Not Required
        BoqItem(
            code="A2.2",
            description=(
                "Establish on site rotary drilling plant and equipment for a Green " "Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D14: Not Required
        BoqItem(
            code="A2.3",
            description=(
                "Establish on site Geobor S rotary drilling plant and equipment for a"
                " Green Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D15: Not Required
        BoqItem(
            code="A2.4",
            description=(
                "Establish on site trial pitting and trenching plant and equipment "
                "for a Green Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D16: Not Required
        BoqItem(
            code="A2.5",
            description=(
                "Establish on site in situ test and sampling equipment for a Green " "Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D17: Not Required
        BoqItem(
            code="A2.6",
            description=(
                "Establish on site cone penetration testing (CPT) plant and equipment"
                " for a Green Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D18: Not Required
        BoqItem(
            code="A2.7",
            description=(
                "Establish on site dynamic sampling and probing plant and equipment "
                "for a Green Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D19: Not Required
        BoqItem(
            code="A2.8",
            description="Establish on site geophysical survey equipment for a Green Category site",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D20: Not Required
        BoqItem(
            code="A2.9",
            description=(
                "Establish on site instrumentation equipment as required for a Green "
                "Category site"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D21: Not Required
        BoqItem(
            code="A3.1",
            description="Extra over item A2.1 - A2.9 for a yellow category site",
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D22: Not Required
        BoqItem(
            code="A3.2",
            description="As Item A3.1 but for a Red Category site",
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D23: Not Required
        BoqItem(
            code="A4.1",
            description="Maintain on site all site safety equipment for a Yellow Category site",
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D24: Not Required
        BoqItem(
            code="A4.2",
            description="Maintain on site all site safety equipment for a Red Category site",
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D25: Not Required
        BoqItem(
            code="A5.1",
            description=(
                "Decontamination of equipment during and at end of intrusive "
                "investigation for a Yellow Category site"
            ),
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D26: Not Required
        BoqItem(
            code="A5.2",
            description=(
                "Decontamination of equipment during and at end of intrusive "
                "investigation for a Red Category site"
            ),
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D27: Not Required
        BoqItem(
            code="A6",
            description=(
                "Appropriate storage, transport and off-site disposal of excess "
                "contaminated arising’s from borehole, trial pit or slit trench to "
                "EPA regulated landfill site (includes any PPE equipment but excludes"
                " laboratory testing on suspected contaminated materials). Note item "
                "to be remeasured with delivery dockets and records maintained by the"
                " Contractor."
            ),
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D28: Not Required
        BoqItem(
            code="A6.1",
            description="Contractor's uplift on Item A6",
            unit="%",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D29: Not Required
        BoqItem(
            code="A7",
            description="Provide professional attendance to meet the contract requirements",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D30: Included in A7
        BoqItem(
            code="A7.1",
            description="Provide Technician",
            unit="per day",
            quantity="Included in A7",
        ),
        # 'Section A'!D31: Included in A7
        BoqItem(
            code="A7.2",
            description="Provide Engineer / Geologist (as per item 2.3 of Specification)",
            unit="per day",
            quantity="Included in A7",
        ),
        # 'Section A'!D32: Included in A7
        BoqItem(
            code="A7.3",
            description=(
                "Provide Chartered Engineer / Professional Geologist (as item 2.3 of "
                "Specification)"
            ),
            unit="per day",
            quantity="Included in A7",
        ),
        # 'Section A'!D33: Included in A7
        BoqItem(
            code="A7.4",
            description=(
                "Provide Chartered Engineer / Professional Geologist (+10 years "
                "experience post charter)"
            ),
            unit="per day",
            quantity="Included in A7",
        ),
        # 'Section A'!D34: Included in A7
        BoqItem(
            code="A7.5",
            description=(
                "Provide Chartered Engineer / Professional Geologist (+20 years "
                "experience post charter)"
            ),
            unit="per day",
            quantity="Included in A7",
        ),
        # --- A8: the only computed item in Section A ---
        # 'Section A'!D35 =
        #   Boreholes!E92              (SUM of 'Scheduled' column)
        # + 'Trial Pits'!G92           (SUM of 'Scheduled' column)
        # + 2 * Trenches!K93           (SUM of 'completed' column, x 2 for endpoints)
        # + 'Inspection pit'!H92       (SUM of 'Completed' column)
        # + DPH!H122                   (SUM of 'Completed' column)
        # + CPT!K92                    (SUM of 'Completed' column)
        # + 'Dynamic Sampling'!H92     (SUM of 'Completed' column)
        # + 'Soakaway (BRE)'!E52       (SUM of 'Completed' column)
        BoqItem(
            code="A8",
            description="Set out the location at each exploratory hole or point",
            unit="Nr",
            quantity=a8,
        ),
        # 'Section A'!D36: =D35
        BoqItem(
            code="A8.1",
            description=(
                "Establish the location and elevation (X, Y, Z) of the ground at each"
                " 'as-built' exploratory hole or point"
            ),
            unit="nr",
            quantity=a8_1,
        ),
        # 'Section A'!D37: Not Required
        BoqItem(
            code="A9",
            description="Preparation of Health and Safety documentation and Safety Risk Assessment",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D38: Not Required
        BoqItem(
            code="A10",
            description="Facilities for the Investigation Supervisor",
            unit="per week",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D39: Not Required
        BoqItem(
            code="A11",
            description="Vehicle(s) for the Investigation Supervisor",
            unit="vehicle wk",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D40: Not Required
        BoqItem(
            code="A11.1",
            description="Provision of fuel and tolls for A11 (to be reimbursed under the contract)",
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D41: Not Required
        BoqItem(
            code="A11.2",
            description="Contractors uplift on item A11 and A11.1",
            unit="% uplift",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D42: Not Required
        BoqItem(
            code="A12",
            description=(
                "Provision of phone and internet for the Investigation Supervisor (to"
                " be reimbursed under the contract)"
            ),
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D43: Not Required
        BoqItem(
            code="A12.1",
            description="Contractors Uplift on item A12",
            unit="% uplift",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D44: Not Required
        BoqItem(
            code="A13",
            description=(
                "Deliver selected cores and samples specified Client address (address"
                " to be advised)"
            ),
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D45: Not Required
        BoqItem(
            code="A14",
            description=(
                "Special additional testing and sampling required by Investigation " "Supervisor"
            ),
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D46: Not Required
        BoqItem(
            code="A15",
            description=(
                "Traffic safety and management to include preparation of traffic "
                "management drawings for investigations on roads or pavement areas"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D47: Not Required
        BoqItem(
            code="A16",
            description="Provision of road opening licences and road damage bonds",
            unit="provisional sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D48: Not Required
        BoqItem(
            code="A17",
            description="Contractors uplift on items A15 and A16",
            unit="% uplift",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D49: Not Required
        BoqItem(
            code="A18",
            description="One master copy of Desk Study Report",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D50: Not Required
        BoqItem(
            code="A18.1",
            description="Additional hard copy of Desk Study Report",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D51: Not Required
        BoqItem(
            code="A18.2",
            description="Electronic copy of Desk Study Report (PDF)",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D52: Not Required
        BoqItem(
            code="A19",
            description="One master copy of the Ground Investigation Report (Factual)",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D53: Not Required
        BoqItem(
            code="A19.1",
            description="Additional copy of the Ground Investigation Report (Factual)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D54: Not Required
        BoqItem(
            code="A19.2",
            description="Electronic copy of Ground Investigation Report",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D55: Not Required
        BoqItem(
            code="A20",
            description="One master copy of Geophysical Report",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D56: Not Required
        BoqItem(
            code="A20.1",
            description="Additional hard copy of Geophysical Report",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D57: Not Required
        BoqItem(
            code="A20.2",
            description="Electronic copy of Geophysical Report (PDF)",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D58: Not Required
        BoqItem(
            code="A21",
            description="One master copy of Geotechnical Interpretive Report",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D59: Not Required
        BoqItem(
            code="A21.1",
            description="Additional copy of Geotechnical Interpretive Report",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D60: Not Required
        BoqItem(
            code="A21.2",
            description="Electronic copy of Geotechnical Interpretive Report",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D61: Not Required
        BoqItem(
            code="A22",
            description="Digital field/engineering logs in AGS transfer format",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D62: Not Required
        BoqItem(
            code="A23",
            description="Digital laboratory test data in AGS transfer files",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D63: Not Required
        BoqItem(
            code="A24",
            description=(
                "Digital copy of trial pit, slit trench or core photographs as per " "Specification"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D64: Not Required
        BoqItem(
            code="A25",
            description="Storage of all samples following completion of fieldworks",
            unit="wk",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D65: (blank)
        BoqItem(
            code="A26",
            description="Storage of core boxes following completion of fieldworks",
            unit="wk",
            quantity=None,
        ),
        # 'Section A'!D66: included in A2
        BoqItem(
            code="A27",
            description="Provision of water supply for the fieldworks",
            unit="sum",
            quantity="included in A2",
        ),
        # 'Section A'!D67: Not Required
        BoqItem(
            code="A28",
            description="Provision of Insurances",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D68: Not Required
        BoqItem(
            code="A29",
            description="Provision of Performance Bond",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D69: Not Required
        BoqItem(
            code="A30",
            description="Perform the role of PSCS",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section A'!D70: Not Required
        BoqItem(
            code="A31",
            description=(
                "Contractor liaison with external bodies to obtain road opening "
                "licence, foreshore licence for marine investigations etc. (specify)"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
    ]


def _count_set_out_points(project: Project) -> int:
    """A8 quantity — total number of exploratory points to set out.

    'Section A'!D35:
    =[1]Boreholes!$E92+'[1]Trial Pits'!$G92+(2*([1]Trenches!$K93))
     +'[1]Inspection pit'!$H92+[1]DPH!$H122+[1]CPT!$K92
     +'[1]Dynamic Sampling'!$H92+'[1]Soakaway (BRE)'!$E$52

    Trenches count twice because a slit trench has two endpoints to set out.
    See the module docstring for what each column counts.
    """
    # Boreholes!E: =IF(A2= "","",1) — every borehole listed
    boreholes_e92 = len(project.boreholes)
    # 'Trial Pits'!G: =IF(H2>0,1,0) — schedule depth is required (> 0) on the model
    trial_pits_g92 = sum(1 for tp in project.trial_pits if tp.schedule_depth_m > 0)
    # Trenches!K: =IF(J3>0,1,0)
    trenches_k93 = sum(_trench_k_completed(t) for t in project.trenches)
    # 'Inspection pit'!H: =IF(E2>0,1,0); totals row =SUM(H65:H91) — all pits counted (deviation)
    inspection_pit_h92 = sum(_inspection_pit_h_completed(ip) for ip in project.inspection_pits)
    # DPH!H: =IF(C2>0,1,0) — depth is required (> 0) on the model
    dph_h122 = sum(1 for dp in project.dynamic_probes if dp.depth_m > 0)
    # CPT!K: =IF(D2>0,1,0) — depth is required (> 0) on the model
    cpt_k92 = sum(1 for c in project.cpts if c.depth_m > 0)
    # 'Dynamic Sampling'!H: =IF(C2>0,1,0) — depth is required (> 0) on the model
    dynamic_sampling_h92 = sum(1 for ds in project.dynamic_samples if ds.depth_m > 0)
    # 'Soakaway (BRE)'!E: =IF(I2>0, 1, 0)
    soakaway_e52 = sum(_soakaway_e_completed(s) for s in project.soakaways)

    return (
        boreholes_e92
        + trial_pits_g92
        + 2 * trenches_k93
        + inspection_pit_h92
        + dph_h122
        + cpt_k92
        + dynamic_sampling_h92
        + soakaway_e52
    )


def _trench_k_completed(trench: Trench) -> int:
    """Trenches!K: =IF(J3>0,1,0) — J = 'Recorded Total Depth'."""
    return 1 if (trench.overall_total_depth_m or 0.0) > 0 else 0


def _inspection_pit_h_completed(pit: InspectionPit) -> int:
    """'Inspection pit'!H: =IF(E2>0,1,0) — E = 'Recorded Depth'."""
    return 1 if (pit.recorded_depth_m or 0.0) > 0 else 0


def _soakaway_e_completed(soakaway: Soakaway) -> int:
    """'Soakaway (BRE)'!E: =IF(I2>0, 1, 0) — I = 'Depth' (recorded)."""
    return 1 if (soakaway.depth_m or 0.0) > 0 else 0
