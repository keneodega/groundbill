"""Section E — Sampling and monitoring during intrusive investigation.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section E' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section E', which reads
the totals rows of the Log Tracker (`reference/excel/1_BOQ_Log_Rev_A.xlsx`).

Formulas
--------
- E2   ``=SUM(Boreholes!$K92,'Trial Pits'!$M92,Trenches!$N93,'Inspection pit'!$E92)
  +'Dynamic Sampling'!$C$92`` — one tub sample per metre of hole.
- E3   ``=D12``      (same as E2)
- E4   ``=D12/10``   (E2 ÷ 10)
- E5   ``=Boreholes!$K92/5``
- E6   ``=D15``      (same as E5)
- E8.1 ``=Boreholes!$K92/10``
- E8.2 ``=Boreholes!$K92/10``
- E12  COUNTIF of ``"*EV*"`` across five Log Tracker sheets (see
  ``e12_environmental_sample_count``)
- E16  ``=D25``      (same as E12)
- E9 has a blank quantity cell in the Calculator; it is emitted as ``None``.
- All other items are the static text ``Not Required``.

None of the divisions are rounded in the workbook, and none are rounded here.

Log Tracker cells used
----------------------
- ``Boreholes!K92``         ``=SUM(K2:K91)``, K = "CP Drilling Total Depth".
  In the model this is the sum of every borehole's cable percussion phase
  depths; rotary metres are not included.
- ``'Trial Pits'!M92``      ``=SUM(M2:M91)``, M = "Depth" (recorded depth).
- ``'Dynamic Sampling'!C92`` ``=SUM(C2:C91)``, C = "Depth".
- ``'Inspection pit'!E92``  see the first open item below.
- ``Trenches!N93``          see the second open item below.

Open items for review (by Havilah)
----------------------------------
- **Inspection pit totals (deliberate deviation, agreed 2026-10-01).**
  ``'Inspection pit'!E92`` is ``=SUM(E65:E91)`` — it starts at row 65, so the
  first 63 inspection pits would contribute nothing. Every other totals row
  in the Log Tracker starts at the first data row, so this is treated as a
  slip for ``E2:E91`` and the recorded depths of *all* inspection pits are
  summed.
- **Trenches contribute nothing to E2 (translated literally).**
  ``Trenches!N93`` is an empty cell: column N is the paved "Recorded Width"
  and the totals row (93) has no formula in that column. The trench term of
  E2 is therefore always 0, whatever the trenches' dimensions. Translated
  literally pending confirmation of the intended source column.

Rows deliberately not translated
--------------------------------
- Row 32, "(Note sample rate includes provision of specialist containers)",
  is a footnote beneath the last item rather than a BOQ item or sub-heading.
  ``BoqItem`` has no way to carry a trailing note, so it is not emitted.

Descriptions are verbatim, including the workbook's spacing ("Open tube-
thick walled sample").
"""

from groundbill.models import DrillingMethod, InSituTest, Project, PSEVTest

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"
_CP = DrillingMethod.CABLE_PERCUSSION


def compute_section_e(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section E BOQ items for the given project."""

    boreholes_k92 = _boreholes_k92_cp_drilling_total_depth(project)

    # 'Section E'!D12:
    # =SUM([1]Boreholes!$K92,'[1]Trial Pits'!$M92,[1]Trenches!$N93,'[1]Inspection pit'!$E92)
    #  +'[1]Dynamic Sampling'!$C$92
    e2 = e2_tub_sample_count(project)
    # 'Section E'!D13: =D12
    e3 = e2
    # 'Section E'!D14: =D12/10
    e4 = e2 / 10
    # 'Section E'!D15: =[1]Boreholes!$K92/5
    e5 = boreholes_k92 / 5
    # 'Section E'!D16: =D15
    e6 = e5
    # 'Section E'!D18: =[1]Boreholes!$K92/10
    e8_1 = boreholes_k92 / 10
    # 'Section E'!D19: =[1]Boreholes!$K92/10
    e8_2 = boreholes_k92 / 10
    # 'Section E'!D25: COUNTIF of "*EV*" across five sheets — see helper for the full formula
    e12 = e12_environmental_sample_count(project)
    # 'Section E'!D29: =D25
    e16 = e12

    return [
        # 'Section E'!D11: Not Required
        BoqItem(
            code="E1",
            description="Jar sample",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Samples for geotechnical purposes",
        ),
        # 'Section E'!D12: =SUM(Boreholes!$K92, 'Trial Pits'!$M92, Trenches!$N93, 'Inspection pit'!$E92) + 'Dynamic Sampling'!$C$92
        BoqItem(
            code="E2",
            description="Tub sample",
            unit="nr",
            quantity=e2,
        ),
        # 'Section E'!D13: =D12
        BoqItem(
            code="E3",
            description="Bulk sample",
            unit="nr",
            quantity=e3,
        ),
        # 'Section E'!D14: =D12/10
        BoqItem(
            code="E4",
            description="Large bulk disturbed sample",
            unit="nr",
            quantity=e4,
        ),
        # 'Section E'!D15: =[1]Boreholes!$K92/5
        BoqItem(
            code="E5",
            description="Open tube- thick walled sample (0 to 10m depth)",
            unit="nr",
            quantity=e5,
        ),
        # 'Section E'!D16: =D15
        BoqItem(
            code="E6",
            description="Open tube- thin walled sample (0 to 10m depth)",
            unit="nr",
            quantity=e6,
        ),
        # 'Section E'!D17: Not Required
        BoqItem(
            code="E7",
            description="Piston sample (0 to 10m depth)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section E'!D18: =[1]Boreholes!$K92/10
        BoqItem(
            code="E8.1",
            description="Extra over rate for item E5 in depth range 10m to 20m",
            unit="nr",
            quantity=e8_1,
        ),
        # 'Section E'!D19: =[1]Boreholes!$K92/10
        BoqItem(
            code="E8.2",
            description="Extra over rate for item E6 in depth range 10m to 20m",
            unit="nr",
            quantity=e8_2,
        ),
        # 'Section E'!D20: Not Required
        BoqItem(
            code="E8.3",
            description="Extra over rate for item E7 in depth range 10m to 20m",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section E'!D21: (blank)
        BoqItem(
            code="E9",
            description="Groundwater sample",
            unit="nr",
            quantity=None,
        ),
        # 'Section E'!D22: Not Required
        BoqItem(
            code="E10",
            description="Ground Gas sample",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section E'!D23: Not Required
        BoqItem(
            code="E11",
            description="Cut, prepare and protect core sub-sample",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section E'!D25: COUNTIF of "*EV*" across five sheets — see e12_environmental_sample_count
        BoqItem(
            code="E12",
            description="Environmental / contamination sample for Suite E",
            unit="nr",
            quantity=e12,
            subheading="Samples for environmental / contamination analysis",
        ),
        # 'Section E'!D26: Not Required
        BoqItem(
            code="E13",
            description="Environmental / contamination sample for Suite F",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section E'!D27: Not Required
        BoqItem(
            code="E14",
            description="Ground gas sample for Suite G",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section E'!D28: Not Required
        BoqItem(
            code="E15",
            description="Environmental / contamination sample for Suite H",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section E'!D29: =D25
        BoqItem(
            code="E16",
            description="Environmental / contamination sample for Suite I",
            unit="nr",
            quantity=e16,
        ),
        # 'Section E'!D30: Not Required
        BoqItem(
            code="E17",
            description=(
                "Other specialist environmental / contamination sampling as specified"
                " by Investigation Supervisor (Suite J)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
    ]


def e2_tub_sample_count(project: Project) -> float:
    """Tub sample count (item E2). Also read by Section K, as in the Calculator.

    'Section E'!D12:
    =SUM([1]Boreholes!$K92,'[1]Trial Pits'!$M92,[1]Trenches!$N93,'[1]Inspection pit'!$E92)
     +'[1]Dynamic Sampling'!$C$92

    Each term is a total depth in metres, so the rule is one tub sample per
    metre of cable percussion borehole, trial pit, inspection pit and dynamic
    sampling hole. See the module docstring for the two open items (inspection
    pit range, empty trench cell).
    """
    # 'Trial Pits'!M92: =SUM(M2:M91) — M = "Depth"
    trial_pits_m92 = sum(tp.depth_m or 0.0 for tp in project.trial_pits)
    # Trenches!N93: empty cell in the Log Tracker → 0 (open item, translated literally)
    trenches_n93 = 0.0
    # 'Inspection pit'!E92: =SUM(E65:E91) — E = "Recorded Depth".
    # Deliberate deviation: summed over all inspection pits, not rows 65-91 only.
    inspection_pit_e92 = sum(ip.recorded_depth_m or 0.0 for ip in project.inspection_pits)
    # 'Dynamic Sampling'!C92: =SUM(C2:C91) — C = "Depth"
    dynamic_sampling_c92 = sum(ds.depth_m for ds in project.dynamic_samples)

    return (
        _boreholes_k92_cp_drilling_total_depth(project)
        + trial_pits_m92
        + trenches_n93
        + inspection_pit_e92
        + dynamic_sampling_c92
    )


def e12_environmental_sample_count(project: Project) -> int:
    """Count exploratory holes with "EV" in their test selection (item E12).

    Also read by Section L, as in the Calculator.

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


def _boreholes_k92_cp_drilling_total_depth(project: Project) -> float:
    """Boreholes!K92: =SUM(K2:K91) — K = "CP Drilling Total Depth"."""
    return sum(
        phase.depth_m for bh in project.boreholes for phase in bh.phases if phase.method is _CP
    )
