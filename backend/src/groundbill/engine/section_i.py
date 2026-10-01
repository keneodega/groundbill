"""Section I — Instrumentation.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section I' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section I', which reads
the `Boreholes` and `Dynamic Sampling` sheets of the Log Tracker
(`reference/excel/1_BOQ_Log_Rev_A.xlsx`).

Log Tracker columns used
------------------------
Boreholes sheet:

- BH 'ROAD'            "YES" / "NO"            → ``Borehole.on_road``
- BI 'Pizezometer'     "YES"                   → ``Borehole.piezometer``
- BJ 'Plain Depth (m)' piezometer plain pipe   → ``piezometer_plain_depth_m``
- BL 'Standpipe (mm)'  "YES"                   → ``Borehole.standpipe``
- BM 'Plain Depth (m)' standpipe plain pipe    → ``standpipe_plain_depth_m``
- BN 'Slotted Depth (m)'                       → ``standpipe_slotted_depth_m``
- BP 'PIE/SP Complete' ``=IF(OR(BI2="YES",BL2="YES"), 1, 0)`` (derived)

Dynamic Sampling sheet:

- I 'ROAD'             "YES" / "NO"            → ``DynamicSample.on_road``
- K 'Standpipe (mm)'   "YES"                   → ``DynamicSample.standpipe``
- L 'Plain Depth (m)'                          → ``plain_depth_m``
- M 'Slotted Depth (m)'                        → ``slotted_depth_m``
- O 'PIE/SP Complete'  ``=IF(OR(G2="YES",K2="YES"), 1, 0)`` (derived)

Row 92 of each sheet holds the column totals (``=SUM(BJ2:BJ91)`` and so on).

Formulas
--------
- I1  ``=Boreholes!$BJ92+Boreholes!$BM92+'Dynamic Sampling'!$L$92``
- I2  ``=COUNTIF(Boreholes!$BI$2:$BI91,"YES")+COUNTIF('Dynamic Sampling'!$K$2:$K$91,"YES")``
- I3  ``=D12``                 (same as I2)
- I4  ``=Boreholes!$BJ92``
- I5  ``=(COUNTIF(Boreholes!$BI$2:$BI91,"YES"))*1``  (note: "assumed one 1m seal")
- I6  ``=Boreholes!$BN92+'Dynamic Sampling'!$M$92``
- I7  ``=D16``                 (same as I6)
- I8  ``=Boreholes!$BM92+'Dynamic Sampling'!$L92``
- I9  ``=(COUNTIF(Boreholes!$BM$2:$BM91,">0"))*1+(COUNTIF('Dynamic Sampling'!$O$2:$O$91,">0"))*1``
  (note: "assumed one 1m seal")
- I14 ``=(COUNTIF(Boreholes!$BI…,"YES")+COUNTIF(Boreholes!$BL…,"YES")
  +COUNTIF('Dynamic Sampling'!$K…,"YES"))*2``
- I16 ``=COUNTIFS(Boreholes!$BH…,"YES",Boreholes!$BP…,">0")
  +COUNTIFS('Dynamic Sampling'!$I…,"YES",'Dynamic Sampling'!$O…,">0")``
- I17 as I16 but with ROAD = "NO"
- I19 ``=D27``                 (same as I17)
- I20 ``=D27``                 (same as I17)

I10-I13, I15, I18 and I21-I35 are ``Not Required``.

In words: installations on a road get a flush cover (I16); those off a road
get a raised cover (I17), stock-proof fencing (I19) and marker posts (I20).

Model decisions (agreed 2026-10-01)
-----------------------------------
- The ROAD columns are yes/no flags. ``on_road=False`` stands for both "NO"
  and a blank cell, so an installation with no ROAD entry is given a raised
  cover. (In the workbook a blank ROAD cell matches neither "YES" nor "NO"
  and the installation would get no cover at all.)
- The 'Standpipe (mm)' columns are yes/no flags: every formula tests them for
  "YES" and none reads a diameter. The 100 mm standpipe items (I10-I13) are
  ``Not Required``.
- A borehole can have both a piezometer and a standpipe (two separate flags).

Open items for review (by Havilah)
----------------------------------
All translated literally:

- **I2 counts dynamic-sampling standpipes as piezometer tips.** The second
  term reads 'Dynamic Sampling'!K ('Standpipe (mm)'), so each dynamic sampling
  hole with a standpipe adds one "19mm casagrande piezometer tip" (and, via
  I3, one metre of sand cell).
- **I5 and I9 differ in what they count.** I5 (seals to piezometer pipe)
  counts boreholes only. I9 (seals to standpipe) counts boreholes with a
  standpipe plain depth greater than 0 (column BM, not the BL flag) plus
  dynamic sampling holes with a standpipe.
- **I1 backfill length** is the sum of the *plain* pipe depths. The
  Calculator's own note reads "currently adding the total meters of 'Plain
  Depth' for piezo and standpipe".
- **Depth totals are not filtered on the YES flags.** I1, I4, I6 and I8 read
  the totals row, so a depth entered without its YES flag is still measured.
- **'Dynamic Sampling'!O** tests column G, which is an empty spacer column,
  as well as K. In effect it is 1 when K is "YES".

Descriptions are verbatim, including the workbook's spellings ("propietary",
"Provdie", "upraight").
"""

from groundbill.models import Borehole, DynamicSample, Project

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"


def compute_section_i(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section I BOQ items for the given project."""

    boreholes = project.boreholes
    samples = project.dynamic_samples

    # Totals row of the Boreholes sheet
    # Boreholes!BJ92: =SUM(BJ2:BJ91) — piezometer plain depth
    bh_bj92 = sum(b.piezometer_plain_depth_m or 0.0 for b in boreholes)
    # Boreholes!BM92: =SUM(BM2:BM91) — standpipe plain depth
    bh_bm92 = sum(b.standpipe_plain_depth_m or 0.0 for b in boreholes)
    # Boreholes!BN92: =SUM(BN2:BN91) — standpipe slotted depth
    bh_bn92 = sum(b.standpipe_slotted_depth_m or 0.0 for b in boreholes)

    # Totals row of the Dynamic Sampling sheet
    # 'Dynamic Sampling'!L92: =SUM(L2:L91) — plain depth
    ds_l92 = sum(d.plain_depth_m or 0.0 for d in samples)
    # 'Dynamic Sampling'!M92: =SUM(M2:M91) — slotted depth
    ds_m92 = sum(d.slotted_depth_m or 0.0 for d in samples)

    # COUNTIF([1]Boreholes!$BI$2:$BI91,"YES")
    bh_piezometers = sum(1 for b in boreholes if b.piezometer)
    # COUNTIF([1]Boreholes!$BL$2:$BL91,"YES")
    bh_standpipes = sum(1 for b in boreholes if b.standpipe)
    # COUNTIF('[1]Dynamic Sampling'!$K$2:$K$91,"YES")
    ds_standpipes = sum(1 for d in samples if d.standpipe)

    # 'Section I'!D11: =[1]Boreholes!$BJ92+[1]Boreholes!$BM92+'[1]Dynamic Sampling'!$L$92
    i1 = bh_bj92 + bh_bm92 + ds_l92
    # 'Section I'!D12:
    # =COUNTIF([1]Boreholes!$BI$2:$BI91,"YES")+COUNTIF('[1]Dynamic Sampling'!$K$2:$K$91,"YES")
    i2 = bh_piezometers + ds_standpipes
    # 'Section I'!D13: =D12
    i3 = i2
    # 'Section I'!D14: =[1]Boreholes!$BJ92
    i4 = bh_bj92
    # 'Section I'!D15: =(COUNTIF([1]Boreholes!$BI$2:$BI91,"YES"))*1
    i5 = bh_piezometers * 1
    # 'Section I'!D16: =[1]Boreholes!$BN92+'[1]Dynamic Sampling'!$M$92
    i6 = bh_bn92 + ds_m92
    # 'Section I'!D17: =D16
    i7 = i6
    # 'Section I'!D18: =[1]Boreholes!$BM92+'[1]Dynamic Sampling'!$L92
    i8 = bh_bm92 + ds_l92
    # 'Section I'!D19:
    # =(COUNTIF([1]Boreholes!$BM$2:$BM91,">0"))*1+(COUNTIF('[1]Dynamic Sampling'!$O$2:$O$91,">0"))*1
    i9 = (
        sum(1 for b in boreholes if (b.standpipe_plain_depth_m or 0.0) > 0) * 1
        + sum(1 for d in samples if _ds_o_pie_sp_complete(d) > 0) * 1
    )
    # 'Section I'!D24:
    # =(COUNTIF([1]Boreholes!$BI$2:$BI91,"YES")+COUNTIF([1]Boreholes!$BL$2:$BL91,"YES")
    #   +COUNTIF('[1]Dynamic Sampling'!$K$2:$K$91, "YES"))*2
    i14 = (bh_piezometers + bh_standpipes + ds_standpipes) * 2
    # 'Section I'!D26:
    # =COUNTIFS([1]Boreholes!$BH$2:$BH91,"YES",[1]Boreholes!$BP$2:$BP91,">0")
    #  +COUNTIFS('[1]Dynamic Sampling'!$I$2:$I$91,"YES",'[1]Dynamic Sampling'!$O$2:$O$91,">0")
    i16 = sum(1 for b in boreholes if b.on_road and _bh_bp_pie_sp_complete(b) > 0) + sum(
        1 for d in samples if d.on_road and _ds_o_pie_sp_complete(d) > 0
    )
    # 'Section I'!D27:
    # =(COUNTIFS([1]Boreholes!$BH$2:$BH91,"NO",[1]Boreholes!$BP$2:$BP91,">0")
    #   +COUNTIFS('[1]Dynamic Sampling'!$I$2:$I$91,"NO",'[1]Dynamic Sampling'!$O$2:$O$91,">0"))
    i17 = sum(1 for b in boreholes if not b.on_road and _bh_bp_pie_sp_complete(b) > 0) + sum(
        1 for d in samples if not d.on_road and _ds_o_pie_sp_complete(d) > 0
    )
    # 'Section I'!D29: =D27
    i19 = i17
    # 'Section I'!D30: =D27
    i20 = i17

    return [
        # 'Section I'!D11: =[1]Boreholes!$BJ92+[1]Boreholes!$BM92+'[1]Dynamic Sampling'!$L$92
        BoqItem(
            code="I1",
            description="Backfill exploratory hole with cement/bentonite grout or bentonite pellets",
            unit="m",
            quantity=i1,
            subheading="Standpipes and piezometers",
        ),
        # 'Section I'!D12: =COUNTIF([1]Boreholes!$BI$2:$BI91,"YES")+COUNTIF('[1]Dynamic Sampling'!$K$2:$K$91,"YES")
        BoqItem(
            code="I2",
            description="Provide and install 19mm casagrande piezometer tip",
            unit="nr",
            quantity=i2,
        ),
        # 'Section I'!D13: =D12
        BoqItem(
            code="I3",
            description="Provide and install sand cell to I2",
            unit="m",
            quantity=i3,
        ),
        # 'Section I'!D14: =[1]Boreholes!$BJ92
        BoqItem(
            code="I4",
            description="Provide and install 19mm casing/piezometer plain pipe",
            unit="m",
            quantity=i4,
        ),
        # 'Section I'!D15: =(COUNTIF([1]Boreholes!$BI$2:$BI91,"YES"))*1
        BoqItem(
            code="I5",
            description="Provide and install bentonite seals to I4",
            unit="m",
            quantity=i5,
        ),
        # 'Section I'!D16: =[1]Boreholes!$BN92+'[1]Dynamic Sampling'!$M$92
        BoqItem(
            code="I6",
            description="Provide and install propietary slotted standpipe (50mm internal diameter)",
            unit="m",
            quantity=i6,
        ),
        # 'Section I'!D17: =D16
        BoqItem(
            code="I7",
            description="Provide and install gravel pack to I6",
            unit="m",
            quantity=i7,
        ),
        # 'Section I'!D18: =[1]Boreholes!$BM92+'[1]Dynamic Sampling'!$L92
        BoqItem(
            code="I8",
            description=(
                "Provide and install propietary casing / plain standpipe (50mm "
                "internal diameter)"
            ),
            unit="m",
            quantity=i8,
        ),
        # 'Section I'!D19: full formula quoted above
        BoqItem(
            code="I9",
            description="Provide and install bentonite seals to I8",
            unit="m",
            quantity=i9,
        ),
        # 'Section I'!D20: Not Required
        BoqItem(
            code="I10",
            description="Provide and install slotted propietary standpipe (100mm internal diameter)",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D21: Not Required
        BoqItem(
            code="I11",
            description="Provide and install gravel pack to I10",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D22: Not Required
        BoqItem(
            code="I12",
            description="Provide and install casing/plain standpipe (100mm internal diameter)",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D23: Not Required
        BoqItem(
            code="I13",
            description="Provide and install bentonite seals to I12",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D24: full formula quoted above
        BoqItem(
            code="I14",
            description="Provide an install end caps to I6 or I10",
            unit="nr",
            quantity=i14,
        ),
        # 'Section I'!D25: Not Required
        BoqItem(
            code="I15",
            description="Provide and install quick release gas valve to I6 or I10",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D26: full formula quoted above
        BoqItem(
            code="I16",
            description="Provide and install protective cover (flush)",
            unit="nr",
            quantity=i16,
        ),
        # 'Section I'!D27: full formula quoted above
        BoqItem(
            code="I17",
            description="Provide and install protective cover (raised)",
            unit="nr",
            quantity=i17,
        ),
        # 'Section I'!D28: Not Required
        BoqItem(
            code="I18",
            description="Extra over item I16 for heavy duty cover in pavements or highways",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D29: =D27
        BoqItem(
            code="I19",
            description=(
                "Supply and erect protective stock proof fencing around standpipe or "
                "piezometer installation"
            ),
            unit="nr",
            quantity=i19,
        ),
        # 'Section I'!D30: =D27
        BoqItem(
            code="I20",
            description="Supply and erect 1.5m high marker posts (3 x 1.5m)",
            unit="nr",
            quantity=i20,
        ),
        # 'Section I'!D32: Not Required
        BoqItem(
            code="I21",
            description="Supply equipment and personnel to carry out purging",
            unit="sum",
            quantity=_NOT_REQUIRED,
            subheading="Standpipe and piezometer development / purging",
        ),
        # 'Section I'!D33: Not Required
        BoqItem(
            code="I22",
            description="Develop standpipe or piezometer by purging (3 well volumes)",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D34: Not Required
        BoqItem(
            code="I23",
            description="As item I22 but by airlift pumping",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D35: Not Required
        BoqItem(
            code="I24",
            description="As item I22 but by over pumping",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D36: Not Required
        BoqItem(
            code="I25",
            description="As item I22 but by jetting",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D37: Not Required
        BoqItem(
            code="I26",
            description="Disposal of purged water",
            unit="litre",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D39: Not Required
        BoqItem(
            code="I27",
            description=(
                "Supply and install inclinometer tubing in exploratory hole (not "
                "including forming/drilling of borehole)"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
            subheading="Inclinometer",
        ),
        # 'Section I'!D40: Not Required
        BoqItem(
            code="I28",
            description="Grout in place inclinometer in cable percussive or rotary borehole",
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D41: Not Required
        BoqItem(
            code="I29",
            description=(
                "Provision of calibrated inclinometer read out unit for monitoring "
                "during investigation"
            ),
            unit="per week",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D42: Not Required
        BoqItem(
            code="I30",
            description="Carry out base set of inclinometer readings in inclinometer and process",
            unit="hr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D43: Not Required
        BoqItem(
            code="I31",
            description="Provide and install protective cover (flush)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D45: Not Required
        BoqItem(
            code="I32",
            description="Provdie and install protective cover (raised) slip indicators",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Slip Indicator",
        ),
        # 'Section I'!D46: Not Required
        BoqItem(
            code="I33",
            description=(
                "Supply and install slip indicator in exploratory borehole, including"
                " brass probe (not including forming/drilling of borehole)"
            ),
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D47: Not Required
        BoqItem(
            code="I34",
            description="Provide and install protective cover (flush)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section I'!D48: Not Required
        BoqItem(
            code="I35",
            description="Provide and install protective headwork cover (upraight)",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
    ]


def _bh_bp_pie_sp_complete(borehole: Borehole) -> int:
    """Boreholes!BP: =IF(OR(BI2="YES",BL2="YES"), 1, 0)"""
    return 1 if (borehole.piezometer or borehole.standpipe) else 0


def _ds_o_pie_sp_complete(sample: DynamicSample) -> int:
    """'Dynamic Sampling'!O: =IF(OR(G2="YES",K2="YES"), 1, 0)

    Column G is an empty spacer column, so only K ('Standpipe (mm)') matters.
    """
    return 1 if sample.standpipe else 0
