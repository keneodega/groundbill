"""Section C — Rotary drilling.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section C' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section C', which reads
the `Boreholes` sheet of the Log Tracker
(`reference/excel/1_BOQ_Log_Rev_A.xlsx`).

Only the "Rotary drilling with and without core recovery" group (C15-C49) and
the reinstatement group (C81-C85) carry quantities. Hand augering (C1-C6),
flight augering (C7-C14), rotary percussive drilling (C50-C58) and Geobor S
(C59-C80) are all ``Not Required`` in the Calculator.

Formulas — set-ups
------------------
- C15     text: "Refer to C15.1.1 to C15.2.2 & C15.3"
- C15.1.1 ``=COUNTIFS(Boreholes!$B$2:$B38,"CP/RC",Boreholes!$C$2:$C38,"NO")``
- C15.1.2 ``=COUNTIFS(Boreholes!$B$2:$B38,"CP/RC",Boreholes!$C$2:$C38,"YES")``
- C15.2.1 ``=COUNTIFS(Boreholes!$B$2:$B91,"RC",Boreholes!$C$2:$C91,"NO")``
- C15.2.2 ``=COUNTIFS(Boreholes!$B$2:$B91,"RC",Boreholes!$C$2:$C91,"YES")``
- C15.3   ``=COUNTIF(Boreholes!$B$2:$B91,"RC")``
- C16     ``=COUNTIFS(B,"RC",D,"YES")+COUNTIFS(B,"CP/RC",D,"YES")``
- C18     ``=(COUNTIF(Boreholes!$BH$2:$BH91,"YES"))*0.125``
- C19     ``=D32+D31+D30+D29`` (C15.2.2 + C15.2.1 + C15.1.2 + C15.1.1, i.e. one
  hour of standing time per rotary set-up)

Formulas — drilling metres by 10 m depth band
---------------------------------------------
Each item reads one cell of the Boreholes totals row (row 92):

==========  =============================  ==================
Items       Boreholes column group         Totals cells
==========  =============================  ==================
C21-C24     WITHOUT CORE in SOFT strata    BA92 BB92 BC92 BD92
C27-C30     WITHOUT CORE in HARD strata    AG92 AH92 AI92 AJ92
C34-C37     WITH CORE in SOFT strata       AQ92 AR92 AS92 AT92
C41-C44     WITH CORE in HARD strata       W92  X92  Y92  Z92
==========  =============================  ==================

The 40-50 m items (C25, C31, C38, C45) are ``Not Required``; the Log Tracker
has no 40-50 m band.

Borehole classification
-----------------------
Column B of the Boreholes sheet ('Type of drilling') is typed by hand as
"CP", "CP/RC" or "RC". In the Python model it is derived from the borehole's
phases, exactly as Section B does:

- ``"CP/RC"`` — at least one cable percussion phase and at least one rotary phase.
- ``"RC"``    — at least one rotary phase and no cable percussion phase.
- Boreholes with only cable percussion phases do not appear in C15-C16.

Depth bands
-----------
The Log Tracker splits each drilling method's START/END depths into bands
with nested IFs, e.g. for "WITH CORE in HARD strata" (START = U, END = V):

- ``W = IF(AND(U2<=10,V2<=10),V2-U2,MAX(0,10-U2))``
- ``X = IF(AND(U2<=10,V2>=20),10,IF(AND(U2>=10,V2<=20),V2-U2,
  IF(AND(U2<=10,V2<=20,V2>=10),V2-10,IF(AND(U2>=10,V2>=20),MAX(0,20-U2),0))))``
- ``Y`` and ``Z`` follow the same pattern for 20-30 m and 30-40 m.

For any sensible START <= END these are the overlap of the interval
[START, END] with the band, which is how ``_rotary_band_distribution``
computes them. A method's START is the total depth of the phases above it.

Open items for review (by Havilah)
----------------------------------
- **C18 ROAD column (resolved 2026-10-01).** Column BH of the Boreholes
  sheet is headed 'ROAD'. The formula counts cells equal to "YES" across *all*
  boreholes (including cable-percussion-only holes) and multiplies by 0.125
  (the Calculator's note: "(No. of BHs on road) x (0.5x0.5x0.5)"). Sections B
  and I test the same column for "YES" / "NO", so it is a yes/no flag, stored
  on the model as ``Borehole.on_road``. Same formula as B3.1.
- **C15.1.1 / C15.1.2 range (deliberate deviation, agreed 2026-10-01).** The
  two CP/RC formulas stop at row 38 (``$B$2:$B38``) while every other formula
  runs to row 91. Treated as a slip: all CP/RC boreholes are counted.
- **Negative band metres in the Log Tracker (deliberate deviation).** The
  last branch of the 20-30 m and 30-40 m band formulas has no ``MAX(0, ...)``
  (``30-U3``, ``40-U3``), so a phase that *starts* below 30 m or 40 m gives a
  negative number in that band (for example rotary coring from 32 m to 38 m
  gives -2 m in the 20-30 m band). Row 2 of the sheet already has the
  ``MAX(0, ...)`` guard on the rotary 20-30 m columns; rows 3-91 do not. The
  Python computes the true overlap, which is never negative. The same applies
  to the cable percussion bands used by Section B.

Descriptions are verbatim, including the workbook's own slips (C71-C74 read
"As Item C65" although they follow C70).
"""

from groundbill.models import Borehole, DrillingMethod, Project

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"

_CP = DrillingMethod.CABLE_PERCUSSION
_ROTARY_METHODS = {
    DrillingMethod.ROTARY_CORE_HARD,
    DrillingMethod.ROTARY_NO_CORE_HARD,
    DrillingMethod.ROTARY_CORE_SOFT,
    DrillingMethod.ROTARY_NO_CORE_SOFT,
}

_DEPTH_BANDS_10M = ((0.0, 10.0), (10.0, 20.0), (20.0, 30.0), (30.0, 40.0))


def compute_section_c(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section C BOQ items for the given project."""

    boreholes = project.boreholes
    cp_rc = [b for b in boreholes if _drilling_type(b) == "CP/RC"]
    rc_only = [b for b in boreholes if _drilling_type(b) == "RC"]

    # 'Section C'!D29: =COUNTIFS([1]Boreholes!$B$2:$B38,"CP/RC",[1]Boreholes!$C$2:$C38,"NO")
    # Deliberate deviation: all CP/RC boreholes counted, not rows 2-38 only.
    c15_1_1 = sum(1 for b in cp_rc if not b.over_barrier_wall_fence)
    # 'Section C'!D30: =COUNTIFS([1]Boreholes!$B$2:$B38,"CP/RC",[1]Boreholes!$C$2:$C38,"YES")
    # Deliberate deviation: all CP/RC boreholes counted, not rows 2-38 only.
    c15_1_2 = sum(1 for b in cp_rc if b.over_barrier_wall_fence)
    # 'Section C'!D31: =COUNTIFS([1]Boreholes!$B$2:$B91,"RC",[1]Boreholes!$C$2:$C91,"NO")
    c15_2_1 = sum(1 for b in rc_only if not b.over_barrier_wall_fence)
    # 'Section C'!D32: =COUNTIFS([1]Boreholes!$B$2:$B91,"RC",[1]Boreholes!$C$2:$C91,"YES")
    c15_2_2 = sum(1 for b in rc_only if b.over_barrier_wall_fence)
    # 'Section C'!D33: =COUNTIF([1]Boreholes!$B$2:$B91,"RC")
    c15_3 = len(rc_only)
    # 'Section C'!D34:
    # =(COUNTIFS([1]Boreholes!$B$2:$B91,"RC",[1]Boreholes!$D$2:$D91,"YES"))
    #  +(COUNTIFS([1]Boreholes!$B$2:$B91,"CP/RC",[1]Boreholes!$D$2:$D91,"YES"))
    c16 = sum(1 for b in rc_only if b.slope_over_20pct) + sum(
        1 for b in cp_rc if b.slope_over_20pct
    )
    # 'Section C'!D36: =(COUNTIF([1]Boreholes!$BH$2:$BH91,"YES"))*0.125
    c18 = sum(1 for b in boreholes if b.on_road) * 0.125
    # 'Section C'!D37: =D32+D31+D30+D29
    c19 = c15_2_2 + c15_2_1 + c15_1_2 + c15_1_1

    # 'Section C'!D40:D43: =[1]Boreholes!$BA92 ... $BD92 — WITHOUT CORE in SOFT strata
    c21, c22, c23, c24 = sum_rotary_bands(boreholes, DrillingMethod.ROTARY_NO_CORE_SOFT)
    # 'Section C'!D46:D49: =[1]Boreholes!$AG92 ... $AJ92 — WITHOUT CORE in HARD strata
    c27, c28, c29, c30 = sum_rotary_bands(boreholes, DrillingMethod.ROTARY_NO_CORE_HARD)
    # 'Section C'!D54:D57: =[1]Boreholes!$AQ92 ... $AT92 — WITH CORE in SOFT strata
    c34, c35, c36, c37 = sum_rotary_bands(boreholes, DrillingMethod.ROTARY_CORE_SOFT)
    # 'Section C'!D61:D64: =[1]Boreholes!$W92 ... $Z92 — WITH CORE in HARD strata
    c41, c42, c43, c44 = sum_rotary_bands(boreholes, DrillingMethod.ROTARY_CORE_HARD)

    return [
        # 'Section C'!D11: Not Required
        BoqItem(
            code="C1",
            description="Bring hand auger equipment to the position of each exploratory hole",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Hand augering",
        ),
        # 'Section C'!D12: Not Required
        BoqItem(
            code="C2",
            description="Bore with hand auger from existing ground level to 2m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D13: Not Required
        BoqItem(
            code="C3",
            description="As Item C2 but between 2 and 4m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D14: Not Required
        BoqItem(
            code="C4",
            description="Standing time for hand auger equipment and crew",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D15: Not Required
        BoqItem(
            code="C5",
            description=(
                "Provision of hand augering equipment and crew for augering as "
                "directed by the Investigation Supervisor maximum depth 4m"
            ),
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D16: Not Required
        BoqItem(
            code="C6",
            description="Backfill hand auger hole with cement/bentonite grout or bentonite pellets",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D18: Not Required
        BoqItem(
            code="C7",
            description=(
                "Move mechanical augering plant and equipment to the site of each "
                "exploratory hole and set up."
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Continuous flight and hollow-stem flight augering",
        ),
        # 'Section C'!D19: Not Required
        BoqItem(
            code="C7.1",
            description=(
                "Hand digging and CAT scan at rotary drillhole location to confirm "
                "absence of utility ducts ( maximum depth of 1.2m or lesser if ground"
                " is assessed as potentially unstable)."
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D20: Not Required
        BoqItem(
            code="C8",
            description="Extra over Item C7 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D21: Not Required
        BoqItem(
            code="C9",
            description=(
                "Break out obstructions where present when hand digging at auger hole"
                " location for Item C7.1."
            ),
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D22: Not Required
        BoqItem(
            code="C10",
            description="Standing time for rotary auger equipment and crew.",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D23: Not Required
        BoqItem(
            code="C11",
            description=(
                "Auger in materials other than hard strata at the specified diameter "
                "between existing ground level and 10m depth."
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D24: Not Required
        BoqItem(
            code="C12",
            description="As Item C11 but between 10 and 20m depth.",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D25: Not Required
        BoqItem(
            code="C13",
            description="As Item C11 but between 20 and 30m depth.",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D26: Not Required
        BoqItem(
            code="C14",
            description="Backfill auger hole with cement/bentonite grout or bentonite pellets",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D28: Refer to C15.1.1 to C15.2.2 & C15.3
        BoqItem(
            code="C15",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory drillhole and set up."
            ),
            unit="nr",
            quantity="Refer to C15.1.1 to C15.2.2 & C15.3",
            subheading="Rotary drilling with and without core recovery",
        ),
        # 'Section C'!D29: =COUNTIFS([1]Boreholes!$B$2:$B38,"CP/RC",[1]Boreholes!$C$2:$C38,"NO")
        BoqItem(
            code="C15.1.1",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory drillhole, set up, dismantle on completion and reinstate"
                " (rotary follow-on)."
            ),
            unit="nr",
            quantity=c15_1_1,
        ),
        # 'Section C'!D30: =COUNTIFS([1]Boreholes!$B$2:$B38,"CP/RC",[1]Boreholes!$C$2:$C38,"YES")
        BoqItem(
            code="C15.1.2",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory drillhole over safety barrier or other fence or wall, "
                "set up, dismantle on completion and reinstate (rotary follow-on)."
            ),
            unit="nr",
            quantity=c15_1_2,
        ),
        # 'Section C'!D31: =COUNTIFS([1]Boreholes!$B$2:$B91,"RC",[1]Boreholes!$C$2:$C91,"NO")
        BoqItem(
            code="C15.2.1",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory drillhole, set up, dismantle on completion and reinstate"
                " (rotary only)."
            ),
            unit="nr",
            quantity=c15_2_1,
        ),
        # 'Section C'!D32: =COUNTIFS([1]Boreholes!$B$2:$B91,"RC",[1]Boreholes!$C$2:$C91,"YES")
        BoqItem(
            code="C15.2.2",
            description=(
                "Move rotary drilling plant and equipment to the site of each "
                "exploratory drillhole, over safety barrier or other fence or wall, "
                "set up, dismantle on completion and reinstate (rotary only)."
            ),
            unit="nr",
            quantity=c15_2_2,
        ),
        # 'Section C'!D33: =COUNTIF([1]Boreholes!$B$2:$B91,"RC")
        BoqItem(
            code="C15.3",
            description=(
                "Hand digging and CAT scan at rotary drillhole location to confirm "
                "absence of utility ducts ( maximum depth of 1.2m or lesser if ground"
                " is assessed as potentially unstable) for rotary only borehole"
            ),
            unit="nr",
            quantity=c15_3,
        ),
        # 'Section C'!D34: =(COUNTIFS([1]Boreholes!$B$2:$B91,"RC",[1]Boreholes!$D$2:$D91,"YES"))+(COUNTIFS([1]Boreholes!$B$2:$B91,"CP/RC",[1]Boreholes!$D$2:$D91,"YES"))
        BoqItem(
            code="C16",
            description=(
                "Extra over Item C15 for setting up on a slope of gradient greater " "than 20%."
            ),
            unit="nr",
            quantity=c16,
        ),
        # 'Section C'!D35: Not Required
        BoqItem(
            code="C17",
            description="Extra over Item C15 for setting up drilling plant for inclined drillhole",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D36: =(COUNTIF([1]Boreholes!$BH$2:$BH91,"YES"))*0.125
        BoqItem(
            code="C18",
            description=(
                "Break out obstructions where present when hand digging at "
                "exploratory hole location for C15.3."
            ),
            unit="m³",
            quantity=c18,
        ),
        # 'Section C'!D37: =D32+D31+D30+D29
        BoqItem(
            code="C19",
            description="Standing time for rotary drilling plant, equipment and crew",
            unit="h",
            quantity=c19,
        ),
        # 'Section C'!D38: Not Required
        BoqItem(
            code="C20",
            description=(
                "Provide aquifer protection measures at a single aquiclude/aquifer "
                "boundary in a drillhole"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D40: =[1]Boreholes!$BA92
        BoqItem(
            code="C21",
            description=(
                "Rotary drill in materials other than hard strata at the specified "
                "diameter, from which cores are not required, between existing ground"
                " level and 10m depth"
            ),
            unit="m",
            quantity=c21,
            subheading="Drilling without cores",
        ),
        # 'Section C'!D41: =[1]Boreholes!$BB92
        BoqItem(
            code="C22",
            description="As Item C21 but between 10 and 20m depth",
            unit="m",
            quantity=c22,
        ),
        # 'Section C'!D42: =[1]Boreholes!$BC92
        BoqItem(
            code="C23",
            description="As Item C21 but between 20 and 30m depth",
            unit="m",
            quantity=c23,
        ),
        # 'Section C'!D43: =[1]Boreholes!$BD92
        BoqItem(
            code="C24",
            description="As Item C21 but between 30 and 40m depth",
            unit="m",
            quantity=c24,
        ),
        # 'Section C'!D44: Not Required
        BoqItem(
            code="C25",
            description="As Item C21 but between 40 and 50m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D45: Not Required
        BoqItem(
            code="C26",
            description="Extra over Items C21 to C25 for inclined rotary drillhole",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D46: =[1]Boreholes!$AG92
        BoqItem(
            code="C27",
            description=(
                "Rotary drill in hard strata at the specified diameter, from which "
                "cores are not required, between existing ground level and 10m depth."
            ),
            unit="m",
            quantity=c27,
        ),
        # 'Section C'!D47: =[1]Boreholes!$AH92
        BoqItem(
            code="C28",
            description="As Item C27 but between 10 and 20m depth",
            unit="m",
            quantity=c28,
        ),
        # 'Section C'!D48: =[1]Boreholes!$AI92
        BoqItem(
            code="C29",
            description="As Item C27 but between 20 and 30m depth",
            unit="m",
            quantity=c29,
        ),
        # 'Section C'!D49: =[1]Boreholes!$AJ92
        BoqItem(
            code="C30",
            description="As Item C27 but between 30 and 40m depth",
            unit="m",
            quantity=c30,
        ),
        # 'Section C'!D50: Not Required
        BoqItem(
            code="C31",
            description="As Item C27 but between 40 and 50m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D51: Not Required
        BoqItem(
            code="C32",
            description="Extra over Items C27 to C31 for inclined drillhole",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D52: Included in C15 to C15.2
        BoqItem(
            code="C33",
            description=(
                "Backfill rotary drillhole with cement/bentonite grout or bentonite "
                "pellets (where standpipe or piezometer is not installed)."
            ),
            unit="m³",
            quantity="Included in C15 to C15.2",
        ),
        # 'Section C'!D54: =[1]Boreholes!$AQ92
        BoqItem(
            code="C34",
            description=(
                "Rotary drill in materials other than hard strata to obtain cores of "
                "the specified diameter between existing ground level and 10m depth"
            ),
            unit="m",
            quantity=c34,
            subheading="Drilling to obtain cores",
        ),
        # 'Section C'!D55: =[1]Boreholes!$AR92
        BoqItem(
            code="C35",
            description="As Item C34 but between 10 and 20m depth(Provisional).",
            unit="m",
            quantity=c35,
        ),
        # 'Section C'!D56: =[1]Boreholes!$AS92
        BoqItem(
            code="C36",
            description="As Item C34 but between 20 and 30m depth",
            unit="m",
            quantity=c36,
        ),
        # 'Section C'!D57: =[1]Boreholes!$AT92
        BoqItem(
            code="C37",
            description="As Item C34 but between 30 and 40m depth",
            unit="m",
            quantity=c37,
        ),
        # 'Section C'!D58: Not Required
        BoqItem(
            code="C38",
            description="As Item C34 but between 40 and 50m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D59: Not Required
        BoqItem(
            code="C39",
            description="Extra over Items C34 to C38 for use of semi-rigid core liner",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D60: Not Required
        BoqItem(
            code="C40",
            description="Extra over Items C34 to C38 for coring inclined rotary drillhole",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D61: =[1]Boreholes!$W92
        BoqItem(
            code="C41",
            description=(
                "Rotary drill in hard strata to obtain cores of the specified "
                "diameter between existing ground level and 10m depth"
            ),
            unit="m",
            quantity=c41,
        ),
        # 'Section C'!D62: =[1]Boreholes!$X92
        BoqItem(
            code="C42",
            description="As Item C41 but between 10 and 20m depth",
            unit="m",
            quantity=c42,
        ),
        # 'Section C'!D63: =[1]Boreholes!$Y92
        BoqItem(
            code="C43",
            description="As Item C41 but between 20 and 30m depth",
            unit="m",
            quantity=c43,
        ),
        # 'Section C'!D64: =[1]Boreholes!$Z92
        BoqItem(
            code="C44",
            description="As Item C41 but between 30 and 40m depth",
            unit="m",
            quantity=c44,
        ),
        # 'Section C'!D65: Not Required
        BoqItem(
            code="C45",
            description="As Item C41 but between 40 and 50m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D66: Not Required
        BoqItem(
            code="C46",
            description="Extra over Items C41 to C45 for use of semi-rigid liner",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D67: Not Required
        BoqItem(
            code="C47",
            description="Extra over Items C41 to C45 for coring inclined rotary drillhole",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D68: Included in C15 to C15.2
        BoqItem(
            code="C48",
            description=(
                "Backfill rotary drillhole with cement/bentonite grout or bentonite "
                "pellets (where standpipe or piezometer is not installed)"
            ),
            unit="m³",
            quantity="Included in C15 to C15.2",
        ),
        # 'Section C'!D69: Not Required
        BoqItem(
            code="C49",
            description="Core box to be retained by the client",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D71: Not Required
        BoqItem(
            code="C50",
            description=(
                "Move rotary percussive drilling plant and equipment to the site of "
                "each drill hole and set up"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Rotary percussive drilling (Odex / Symmetrix)",
        ),
        # 'Section C'!D72: Not Required
        BoqItem(
            code="C51",
            description="Extra over Item C50 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D73: Not Required
        BoqItem(
            code="C52",
            description=(
                "Rotary percussive drill at the specified diameter in any material "
                "between existing ground level and 10m depth"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D74: Not Required
        BoqItem(
            code="C53",
            description="As Item C52 but between 10 and 20m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D75: Not Required
        BoqItem(
            code="C54",
            description="As Item C52 but between 20 and 30m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D76: Not Required
        BoqItem(
            code="C55",
            description="As Item C52 but between 30 and 40m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D77: Not Required
        BoqItem(
            code="C56",
            description="As Item C52 but between 40 and 50m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D78: Not Required
        BoqItem(
            code="C57",
            description="Standing time for rotary percussive drilling plant, equipment and crew",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D79: Not Required
        BoqItem(
            code="C58",
            description=(
                "Backfill rotary percussive drillhole with cement/bentonite grout or "
                "bentonite pellets (where standpipe or piezometer is not installed)"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D81: Not Required
        BoqItem(
            code="C59",
            description=(
                "Move drilling plant and equipment to the site of each exploratory "
                "drillhole and set up equipment (including recirculation tanks), "
                "dismantle on completion and reinstate"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Geobor S Rotary Drilling",
        ),
        # 'Section C'!D82: Not Required
        BoqItem(
            code="C59.1",
            description=(
                "Move drilling plant and equipment to the site of each exploratory "
                "drillhole and set up equipment (including recirculation tanks) over "
                "safety barrier or other fence or wall, set up, dismantle on "
                "completion and reinstate"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D83: Not Required
        BoqItem(
            code="C60",
            description=(
                "Hand digging and CAT scan at rotary drillhole location to confirm "
                "absence of utility ducts ( maximum depth of 1.2m or lesser if ground"
                " is assessed as potentially unstable)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D84: Not Required
        BoqItem(
            code="C61",
            description=(
                "Provision of biodegradable polymer gel (drilling fluid) for Geobor S" " coring"
            ),
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D85: Not Required
        BoqItem(
            code="C62",
            description="Break out surface obstructions where present at exploratory drillhole",
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D86: Not Required
        BoqItem(
            code="C63",
            description="Standing time for Geobor S drilling plant, equipment and crew",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D88: Not Required
        BoqItem(
            code="C64",
            description=(
                "Rotary openhole drilling without core recover to install casing "
                "prior to Geobor coring (nominally 1.5m)"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
            subheading="Geobor S Rotary Coring (to produce 102mm diameter cores)",
        ),
        # 'Section C'!D89: Not Required
        BoqItem(
            code="C65",
            description=(
                "Rotary drilling with Geobor S equipment to recover cores of "
                "overburden material using polymer gel/mud drilling fluid in depth "
                "range 0 to 10m"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D90: Not Required
        BoqItem(
            code="C66",
            description="As Item C65 but between 10 and 20m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D91: Not Required
        BoqItem(
            code="C67",
            description="As Item C65 but between 20 and 30m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D92: Not Required
        BoqItem(
            code="C68",
            description="As Item C65 but between 30 and 40m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D93: Not Required
        BoqItem(
            code="C69",
            description="As Item C65 but between 40 and 50m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D94: Not Required
        BoqItem(
            code="C70",
            description=(
                "Rotary drilling using Geobor S equipment to recover cores in bedrock"
                " formation(s) using polymer gel/mud drilling fluid in depth range 0 "
                "to 10m"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D95: Not Required
        BoqItem(
            code="C71",
            description="As Item C65 but between 10 and 20m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D96: Not Required
        BoqItem(
            code="C72",
            description="As Item C65 but between 20 and 30m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D97: Not Required
        BoqItem(
            code="C73",
            description="As Item C65 but between 30 and 40m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D98: Not Required
        BoqItem(
            code="C74",
            description="As Item C65 but between 40 and 50m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D99: Not Required
        BoqItem(
            code="C75",
            description=(
                "Extra over items C64 to C74 for inclined Geobor S drillhole (maximum"
                " of 20 degrees from the vertical)"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D101: Not Required
        BoqItem(
            code="C76",
            description=(
                "Backfill Geobor S drillhole with cement/bentonite grout or bentonite"
                " pellets (where standpipe or piezometer is not installed)"
            ),
            unit="m³",
            quantity=_NOT_REQUIRED,
            subheading="Geobor S Rotary Drilling - Additional Items",
        ),
        # 'Section C'!D102: Not Required
        BoqItem(
            code="C77",
            description="Provision of semi rigid core liner for items C64 - C75",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D103: Not Required
        BoqItem(
            code="C78",
            description="Provision of core boxes (2m of Geobor S per core box)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D104: Not Required
        BoqItem(
            code="C79",
            description=(
                "Disposal of Geobor S drilling supernatant flush returns (contained "
                "in the recirculation tanks) where permitted on site. Note disposal "
                "areas / locations to be recorded and photographed by contractor"
            ),
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D105: Not Required
        BoqItem(
            code="C80",
            description=(
                "Disposal of Geobor S drilling supernatant flush returns (contained "
                "in the recirculation tanks) to landfill by tanker where on site "
                "disposal is not permitted. Note tanker delivery dockets to be "
                "retained by the Contractor."
            ),
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D107: Included in C15 to C15.2
        BoqItem(
            code="C81",
            description="Reinstatement of gravel hardstanding",
            unit="m²",
            quantity="Included in C15 to C15.2",
            subheading="Reinstatement of Rotary Boreholes",
        ),
        # 'Section C'!D108: Included in D53
        BoqItem(
            code="C82",
            description="Reinstatement of asphalt / bituminous pavement",
            unit="m²",
            quantity="Included in D53",
        ),
        # 'Section C'!D109: Included in C15 to C15.2
        BoqItem(
            code="C83",
            description="Reinstatement of grass areas",
            unit="m²",
            quantity="Included in C15 to C15.2",
        ),
        # 'Section C'!D110: Not Required
        BoqItem(
            code="C84",
            description="Provision of stock proof fencing to rotary drilling works area",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section C'!D111: Included in C15 to C15.2
        BoqItem(
            code="C85",
            description=(
                "Disposal of excess or surplus inert arisings from rotary drilling "
                "operations (where standpipe or piezometer is not installed)"
            ),
            unit="m³",
            quantity="Included in C15 to C15.2",
        ),
    ]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _drilling_type(borehole: Borehole) -> str | None:
    """Return the Boreholes!B 'Type of drilling' value: 'CP/RC', 'RC', or None.

    - ``"CP/RC"`` — at least one CP phase AND at least one rotary phase.
    - ``"RC"``    — at least one rotary phase AND no CP phase.
    - ``None``    — no rotary phases (CP-only or empty) → not counted in Section C.
    """
    methods = {p.method for p in borehole.phases}
    has_cp = _CP in methods
    has_rotary = bool(methods & _ROTARY_METHODS)
    if not has_rotary:
        return None
    if has_cp and has_rotary:
        return "CP/RC"
    return "RC"


def _rotary_band_distribution(borehole: Borehole, method: DrillingMethod) -> list[float]:
    """Return metreage for *method* split across the 0-10/10-20/20-30/30-40 m bands.

    Equivalent to the Log Tracker's four band columns for one method (e.g.
    W:Z for "WITH CORE in HARD strata"), computed as the overlap of the
    method's [START, END] interval with each band.

    Phases are assumed to run sequentially from the surface. START is the sum
    of all phases before the first occurrence of *method*; END is START plus
    the total depth of all *method* phases (the Log Tracker has a single
    START/END pair per method, so repeated phases are treated as one run).
    """
    offset = 0.0
    found = False
    total = 0.0
    for phase in borehole.phases:
        if phase.method is method:
            found = True
            total += phase.depth_m
        elif not found:
            offset += phase.depth_m
    if total == 0.0:
        return [0.0, 0.0, 0.0, 0.0]
    end = offset + total
    return [
        max(0.0, min(end, band_end) - max(offset, band_start))
        for band_start, band_end in _DEPTH_BANDS_10M
    ]


def sum_rotary_bands(boreholes: list[Borehole], method: DrillingMethod) -> list[float]:
    """Boreholes row 92 for one method: each band column summed over all boreholes.

    Also read by Section H (SPT counts in rotary drillholes), as in the Calculator.
    """
    bands = [0.0, 0.0, 0.0, 0.0]
    for bh in boreholes:
        for i, metres in enumerate(_rotary_band_distribution(bh, method)):
            bands[i] += metres
    return bands
