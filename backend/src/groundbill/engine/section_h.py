"""Section H — In situ testing.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section H' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section H', which reads
the `Boreholes`, `Dynamic Sampling`, `Trial Pits`, `Inspection pit`,
`Trenches` and `Soakaway (BRE)` sheets of the Log Tracker
(`reference/excel/1_BOQ_Log_Rev_A.xlsx`).

Formulas — standard penetration tests
-------------------------------------
- H1.1 ``=Boreholes!$N92``  cable percussion metres between 0 and 10 m
- H1.2 ``=Boreholes!$O92``  ... between 10 and 20 m
- H1.3 ``=Boreholes!$P92``  ... between 20 and 30 m
- H1.4 ``Not Required``
- H2.1 ``=ROUNDUP((Boreholes!$AQ92+Boreholes!$BA92)/1.5,0)``
- H2.2 ``=ROUNDUP((Boreholes!$AR92+Boreholes!$BB92)/1.5,0)``
- H2.3 ``=ROUNDUP((Boreholes!$AS92+Boreholes!$BC92)/1.5,0)``
- H2.4 ``Not Required``
- H3.1 ``='Dynamic Sampling'!$C92``

So: one SPT per metre of cable percussion boring (not rounded); one SPT per
1.5 m of rotary drilling in *soft* strata, with or without core (columns AQ:AS
and BA:BC), rounded up per band; and one SPT per metre of dynamic sampling.
Rotary drilling in hard strata attracts no SPTs.

Formulas — tests in pits and trenches
-------------------------------------
Each counts holes whose test selection contains a code, using the wildcard
``COUNTIF(range,"*CODE*")`` over 'Trial Pits'!J, 'Inspection pit'!K and
Trenches!G:

- H6   "DCP"  trial pits + inspection pits + trenches
- H9   "HV"   trial pits **× 4** + inspection pits + trenches
- H19  "BRE"  trial pits + inspection pits + trenches + 'Soakaway (BRE)'!F
- H30  "PT"   trial pits + inspection pits + trenches

Derived from those:

- H23 ``=D43``  (same as H19)
- H25 ``=D47``  (same as H23)
- H26 ``=D49``  (same as H25)
- H34 ``=IF(D56>0,1,"Not Required")``  one plate test report if H30 > 0

Everything else is ``Not Required``.

Open items for review (by Havilah)
----------------------------------
All translated literally:

- **H9 multiplier.** ``COUNTIF('Trial Pits'!…,"*HV*")*4+COUNTIF('Inspection
  pit'!…)+COUNTIF(Trenches!…)`` — the ``*4`` applies to the trial pit term
  only, so a trial pit with hand vanes counts as four sets of readings and an
  inspection pit or trench as one.
- **H3.1 unit.** The quantity is the total depth of dynamic sampling in
  metres, billed as a number of SPTs (one per metre). It is not rounded.
- **H1.x not rounded.** Unlike H2.x there is no ROUNDUP, so 12.5 m of cable
  percussion boring gives 12.5 SPTs.
- **Soakaway sheet.** Only H19 reads the 'Soakaway (BRE)' sheet. A soakaway
  location with "DCP" or "PT" selected is not counted in H6 or H30.
- **H34 note.** The Calculator's note reads "IF D51 is greater than 0 then let
  D59=1", which refers to rows that have since moved; the formula itself
  points at D56 (H30) and is what is translated.

Footnote
--------
Row 41, "Note: rates for permeability test in boreholes or rotary holes to
include standing time rate for plant and equipment", is carried as the
``note`` of H18, so the generator writes it on row 41 as in the workbook.

Descriptions are verbatim, including the workbook's own slips (H21 refers to
"H18", H33 to "Items H29-H31", "steelement" and "valu" in H34).
"""

import math

from groundbill.models import Borehole, DrillingMethod, InSituTest, Project

from .boq_items import BoqItem
from .section_b import cp_band_distribution
from .section_c import sum_rotary_bands

_NOT_REQUIRED = "Not Required"


def compute_section_h(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section H BOQ items for the given project."""

    # Boreholes!N92:Q92 — cable percussion metres per 10 m band, summed over all boreholes
    cp_n92, cp_o92, cp_p92, _cp_q92 = _sum_cp_bands(project.boreholes)
    # Boreholes!AQ92:AT92 — rotary WITH CORE in SOFT strata
    aq92, ar92, as92, _at92 = sum_rotary_bands(project.boreholes, DrillingMethod.ROTARY_CORE_SOFT)
    # Boreholes!BA92:BD92 — rotary WITHOUT CORE in SOFT strata
    ba92, bb92, bc92, _bd92 = sum_rotary_bands(
        project.boreholes, DrillingMethod.ROTARY_NO_CORE_SOFT
    )

    # 'Section H'!D10: =[1]Boreholes!$N92
    h1_1 = cp_n92
    # 'Section H'!D11: =[1]Boreholes!$O92
    h1_2 = cp_o92
    # 'Section H'!D12: =[1]Boreholes!$P92
    h1_3 = cp_p92
    # 'Section H'!D14: =ROUNDUP(([1]Boreholes!$AQ92+[1]Boreholes!$BA92)/1.5,0)
    h2_1 = _roundup((aq92 + ba92) / 1.5)
    # 'Section H'!D15: =ROUNDUP(([1]Boreholes!$AR92+[1]Boreholes!$BB92)/1.5,0)
    h2_2 = _roundup((ar92 + bb92) / 1.5)
    # 'Section H'!D16: =ROUNDUP(([1]Boreholes!$AS92+[1]Boreholes!$BC92)/1.5,0)
    h2_3 = _roundup((as92 + bc92) / 1.5)
    # 'Section H'!D18: ='[1]Dynamic Sampling'!$C92      ('Dynamic Sampling'!C92: =SUM(C2:C91))
    h3_1 = sum(ds.depth_m for ds in project.dynamic_samples)

    # 'Section H'!D26:
    # =COUNTIF('[1]Trial Pits'!$J$2:$J91,"*DCP*")+COUNTIF('[1]Inspection pit'!$K$2:$K91,"*DCP*")
    #  +COUNTIF([1]Trenches!$G$3:$G92,"*DCP*")
    h6 = (
        _count_trial_pits(project, InSituTest.DCP)
        + _count_inspection_pits(project, InSituTest.DCP)
        + _count_trenches(project, InSituTest.DCP)
    )
    # 'Section H'!D29:
    # =COUNTIF('[1]Trial Pits'!$J$2:$J91,"*HV*")*4+COUNTIF('[1]Inspection pit'!$K$2:$K91,"*HV*")
    #  +COUNTIF([1]Trenches!$G$3:$G92,"*HV*")
    # Open item: the *4 applies to the trial pit term only (translated literally).
    h9 = (
        _count_trial_pits(project, InSituTest.HV) * 4
        + _count_inspection_pits(project, InSituTest.HV)
        + _count_trenches(project, InSituTest.HV)
    )
    # 'Section H'!D43:
    # =COUNTIF('[1]Trial Pits'!$J$2:$J91,"*BRE*")+COUNTIF('[1]Inspection pit'!$K$2:$K91,"*BRE*")
    #  +COUNTIF([1]Trenches!$G$3:$G92,"*BRE*")+COUNTIF('[1]Soakaway (BRE)'!$F$2:$F$52,"*BRE*")
    h19 = (
        _count_trial_pits(project, InSituTest.BRE)
        + _count_inspection_pits(project, InSituTest.BRE)
        + _count_trenches(project, InSituTest.BRE)
        + sum(1 for s in project.soakaways if InSituTest.BRE in s.in_situ_tests)
    )
    # 'Section H'!D47: =D43
    h23 = h19
    # 'Section H'!D49: =D47
    h25 = h23
    # 'Section H'!D50: =D49
    h26 = h25
    # 'Section H'!D56:
    # =COUNTIF('[1]Trial Pits'!$J$2:$J91,"*PT*")+COUNTIF('[1]Inspection pit'!$K$2:$K91,"*PT*")
    #  +COUNTIF([1]Trenches!$G$3:$G92,"*PT*")
    h30 = (
        _count_trial_pits(project, InSituTest.PT)
        + _count_inspection_pits(project, InSituTest.PT)
        + _count_trenches(project, InSituTest.PT)
    )
    # 'Section H'!D60: =IF(D56>0,1,"Not Required")
    h34 = 1 if h30 > 0 else _NOT_REQUIRED

    return [
        # 'Section H'!D10: =[1]Boreholes!$N92
        BoqItem(
            code="H1.1",
            description="Standard penetration test in percussive borehole, depth range 0 to 10m",
            unit="nr",
            quantity=h1_1,
        ),
        # 'Section H'!D11: =[1]Boreholes!$O92
        BoqItem(
            code="H1.2",
            description="Standard penetration test in percussive borehole, depth range 10 to 20m",
            unit="nr",
            quantity=h1_2,
        ),
        # 'Section H'!D12: =[1]Boreholes!$P92
        BoqItem(
            code="H1.3",
            description="Standard penetration test in percussive borehole, depth range 20 to 30m",
            unit="nr",
            quantity=h1_3,
        ),
        # 'Section H'!D13: Not Required
        BoqItem(
            code="H1.4",
            description="Standard penetration test in percussive borehole, depth range 30 to 40m",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D14: =ROUNDUP(([1]Boreholes!$AQ92+[1]Boreholes!$BA92)/1.5,0)
        BoqItem(
            code="H2.1",
            description="Standard penetration test in rotary drillhole, depth range 0 to 10m",
            unit="nr",
            quantity=h2_1,
        ),
        # 'Section H'!D15: =ROUNDUP(([1]Boreholes!$AR92+[1]Boreholes!$BB92)/1.5,0)
        BoqItem(
            code="H2.2",
            description="Standard penetration test in rotary drillhole, depth range 10 to 20m",
            unit="nr",
            quantity=h2_2,
        ),
        # 'Section H'!D16: =ROUNDUP(([1]Boreholes!$AS92+[1]Boreholes!$BC92)/1.5,0)
        BoqItem(
            code="H2.3",
            description="Standard penetration test in rotary drillhole, depth range 20 to 30m",
            unit="nr",
            quantity=h2_3,
        ),
        # 'Section H'!D17: Not Required
        BoqItem(
            code="H2.4",
            description="Standard penetration test in rotary drillhole, depth range 30 to 40m",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D18: ='[1]Dynamic Sampling'!$C92
        BoqItem(
            code="H3.1",
            description=(
                "Standard penetration test in dynamic sampling boreholes, depth range" " 0 to 10m"
            ),
            unit="nr",
            quantity=h3_1,
        ),
        # 'Section H'!D19: Not Required
        BoqItem(
            code="H4",
            description="In-situ density testing",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D20: Not Required
        BoqItem(
            code="H4.1",
            description="Small pouring cylinder method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D21: Not Required
        BoqItem(
            code="H4.2",
            description="Large pouring cylinder method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D22: Not Required
        BoqItem(
            code="H4.3",
            description="Water replacement method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D23: Not Required
        BoqItem(
            code="H4.4",
            description="Core cutter method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D24: Not Required
        BoqItem(
            code="H4.5",
            description="Nuclear gauge method",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D25: Not Required
        BoqItem(
            code="H5",
            description="California Bearing Ratio by plate bearing test by plunger method",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D26: COUNTIF of "*DCP*" — full formula quoted above
        BoqItem(
            code="H6",
            description="California Bearing Ratio by TRL DCP method",
            unit="nr",
            quantity=h6,
        ),
        # 'Section H'!D27: Not Required
        BoqItem(
            code="H7",
            description="Vane shear strength test in borehole / trial pit / trench",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D28: Not Required
        BoqItem(
            code="H8",
            description="Hand penetrometer test (set of 3 readings)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D29: COUNTIF of "*HV*" — full formula quoted above
        BoqItem(
            code="H9",
            description="Hand vane test (set of 3 readings)",
            unit="nr",
            quantity=h9,
        ),
        # 'Section H'!D31: Not Required
        BoqItem(
            code="H10",
            description=(
                "In situ geophysical techniques (resistivity and redox potential) for"
                " earthing analysis"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Other tests",
        ),
        # 'Section H'!D33: Not Required
        BoqItem(
            code="H11",
            description=(
                "Set up, execute and dismantle variable head permeability test in "
                "cable percussive borehole"
            ),
            unit="hr",
            quantity=_NOT_REQUIRED,
            subheading="Permeability testing",
        ),
        # 'Section H'!D34: Not Required
        BoqItem(
            code="H12",
            description=(
                "Set up, execute and dismantle constant head permeability test in "
                "cable percussive borehole"
            ),
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D35: Not Required
        BoqItem(
            code="H13",
            description=(
                "Set up, execute and dismantle variable head permeability test in "
                "rotary drillhole"
            ),
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D36: Not Required
        BoqItem(
            code="H14",
            description=(
                "Set up, execute and dismantle constant head permeability test in "
                "rotary drillhole"
            ),
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D37: Not Required
        BoqItem(
            code="H15",
            description=(
                "Set up, execute and dismantle variable head permeability test in "
                "standpipe or standpipe piezometer (rising or falling head test)"
            ),
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D38: Not Required
        BoqItem(
            code="H16",
            description=(
                "Set up and execute constant head permeability test in standpipe or "
                "standpipe piezometer"
            ),
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D39: Not Required
        BoqItem(
            code="H17",
            description="Set up and execute packer permeability test in rotary borehole (0 to 10m)",
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D40: Not Required
        BoqItem(
            code="H18",
            description="Set up and execute packer permeability test in rotary borehole (10 to 20m)",
            unit="hr",
            quantity=_NOT_REQUIRED,
            # Row 41 footnote
            note=(
                "Note: rates for permeability test in boreholes or rotary holes to include "
                "standing time rate for plant and equipment"
            ),
        ),
        # 'Section H'!D43: COUNTIF of "*BRE*" — full formula quoted above
        BoqItem(
            code="H19",
            description="Set up at each test location, excavate trial hole and prepare test area",
            unit="nr",
            quantity=h19,
            subheading="Soil infiltration test (BRE Digest 365)",
        ),
        # 'Section H'!D44: Not Required
        BoqItem(
            code="H20",
            description=(
                "Backfill test hole with clean imported gravel where excavation side "
                "walls are unstable"
            ),
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D45: Not Required
        BoqItem(
            code="H21",
            description="Install 50mm standpipe in H18 to allow for monitoring of water levels",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D46: Not Required
        BoqItem(
            code="H22",
            description="Carry out pre-soaking of test areas",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D47: =D43
        BoqItem(
            code="H23",
            description="Carry out soakaway tests in accordance with BRE Digest 365 (3 cycles)",
            unit="nr",
            quantity=h23,
        ),
        # 'Section H'!D48: Not Required
        BoqItem(
            code="H24",
            description="Provision of water supply for infiltration testing",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D49: =D47
        BoqItem(
            code="H25",
            description=(
                "Protection and temporary fencing of works area as instructed by "
                "Investigation Supervisor"
            ),
            unit="nr",
            quantity=h25,
        ),
        # 'Section H'!D50: =D49
        BoqItem(
            code="H26",
            description="Calculation of infiltration rate for each test location",
            unit="nr",
            quantity=h26,
        ),
        # 'Section H'!D52: Not Required
        BoqItem(
            code="H27",
            description="Set up at each test location, excavate trial hole and prepare test area",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Soil infiltration test (EPA Percolation test)",
        ),
        # 'Section H'!D53: Not Required
        BoqItem(
            code="H28",
            description=(
                "Carry out infiltration tests in accordance with EPA Guidelines (test"
                " to be carried out by an approved Engineer / Geologist in accordance"
                " with EPA requirements)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D54: Not Required
        BoqItem(
            code="H29",
            description=(
                "Provide report on percolation test (by Chartered Engineer or "
                "Professional Geologist)"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D56: COUNTIF of "*PT*" — full formula quoted above
        BoqItem(
            code="H30",
            description=(
                "Set up at each plate test location to include kentledge / reaction "
                "weight and carry out plate test using a 300mm diameter plate. Test "
                "in accordance with NRA SRW CL642"
            ),
            unit="nr",
            quantity=h30,
            subheading="Plate Bearing Test",
        ),
        # 'Section H'!D57: Not Required
        BoqItem(
            code="H31",
            description=(
                "Set up at each plate test location to include kentledge / reaction "
                "weight and carry out plate test using a 450mm diameter plate. Test "
                "in accordance with NRA SRW CL642"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D58: Not Required
        BoqItem(
            code="H32",
            description=(
                "Set up at each plate test location to include kentledge / reaction "
                "weight and carry out plate test using a 600mm diameter plate. Test "
                "in accordance with NRA SRW CL642"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D59: Not Required
        BoqItem(
            code="H33",
            description=(
                "Extra over Items H29-H31 for test durations in excess of 2 hours per" " location"
            ),
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D60: =IF(D56>0,1,"Not Required")
        BoqItem(
            code="H34",
            description=(
                "Provide plate test report with load steelement plot and calculation "
                "of Ks and CBR valu to HD 25-26/10"
            ),
            unit="nr",
            quantity=h34,
        ),
        # 'Section H'!D62: Not Required
        BoqItem(
            code="H35",
            description="Reading of free product level in borehole using an interface probe",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Other specialist tests",
        ),
        # 'Section H'!D63: Not Required
        BoqItem(
            code="H36",
            description="Provide contamination screening test kits (per sample)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D64: Not Required
        BoqItem(
            code="H37",
            description="Carry out headspace testing on sample by FID or PID methods",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D65: Not Required
        BoqItem(
            code="H38",
            description="Self boring pressuremeter",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D66: Not Required
        BoqItem(
            code="H39",
            description="high pressure dilatometer",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section H'!D67: Not Required
        BoqItem(
            code="H40",
            description="Menard Presuremeter",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
    ]


def _sum_cp_bands(boreholes: list[Borehole]) -> list[float]:
    """Boreholes!N92:Q92 — each cable percussion band column summed over all boreholes."""
    bands = [0.0, 0.0, 0.0, 0.0]
    for bh in boreholes:
        for i, metres in enumerate(cp_band_distribution(bh)):
            bands[i] += metres
    return bands


def _roundup(value: float) -> int:
    """Excel ``ROUNDUP(value, 0)`` for a non-negative value.

    The value is first rounded to 9 decimal places so that binary
    floating-point noise (e.g. 3.0000000000000004) is not rounded up to the
    next whole number, which Excel would not do.
    """
    return math.ceil(round(value, 9))


def _count_trial_pits(project: Project, test: InSituTest) -> int:
    """COUNTIF('Trial Pits'!$J$2:$J91, "*<test>*") — J = 'Insitu Tests'."""
    return sum(1 for tp in project.trial_pits if test in tp.in_situ_tests)


def _count_inspection_pits(project: Project, test: InSituTest) -> int:
    """COUNTIF('Inspection pit'!$K$2:$K91, "*<test>*") — K = 'Insitu Tests'."""
    return sum(1 for ip in project.inspection_pits if test in ip.in_situ_tests)


def _count_trenches(project: Project, test: InSituTest) -> int:
    """COUNTIF(Trenches!$G$3:$G92, "*<test>*") — G = 'TESTS'."""
    return sum(1 for t in project.trenches if test in t.in_situ_tests)
