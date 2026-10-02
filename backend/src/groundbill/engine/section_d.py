"""Section D — Pitting and trenching.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section D' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section D', which reads
the `Trial Pits`, `Trenches` and `Inspection pit` sheets of the Log Tracker
(`reference/excel/1_BOQ_Log_Rev_A.xlsx`).

Row numbering: the Calculator's Section D sheet has one extra row at the top,
so its rows are one greater than the Contractor workbook's. The cell
references quoted below are the Calculator's own (item D1 is on row 12, D3 on
row 15, and so on).

Formulas
--------
Inspection pits

- D1  ``='Inspection pit'!$H92``    number of inspection pits dug
- D2  ``='Inspection pit'!$J$92``   volume of surface obstructions broken out

Trial pits and trenches (non paved areas)

- D3   ``=COUNTIF('Trial Pits'!$C$2:$C91,"NON-PAVED")+COUNTIF(Trenches!$C$3:$C92,"NON-PAVED")``
- D3.1 as D3, also requiring Barrier (column B) = "YES"
- D4   as D3, also requiring Slope > 20% (column D) = "YES"
- D6   ``=SUMIFS('Trial Pits'!$O$2:$O91,'Trial Pits'!$C$2:$C91,"NON-PAVED")``
- D7   ``=SUMIFS('Trial Pits'!$P$2:$P91,'Trial Pits'!$C$2:$C91,"NON-PAVED")``
- D9   ``=Trenches!$AD93``
- D10  ``=Trenches!$AE93``

Trial pits and trenches (paved areas)

- D12  ``=COUNTIFS('Trial Pits'!$E$2:$E91,"YES")``
- D13  ``=COUNTIFS(Trenches!$E$3:$E92,"YES")``
- D14  ``=SUMIFS('Trial Pits'!$T$2:$T91,'Trial Pits'!$C$2:$C91,"PAVED")+Trenches!$U93``
- D15  ``='Trial Pits'!$V$92+Trenches!$V93``
- D16  ``='Trial Pits'!$V$92+Trenches!$Q93`` — **not translated literally**, see below
- D17  ``=SUMIFS('Trial Pits'!$R$2:$R91,'Trial Pits'!$C$2:$C91,"PAVED")``
- D18  ``=Trenches!$S93``
- D19  ``=Trenches!$X93`` — **not translated literally**, see below
- D20  ``=D15*0.5`` — row 15 is item D3, so this is D3 × 0.5 (Calculator note:
  "0.5 hr for every trench")

Backfill and reinstatement

- D49  ``=('Trial Pits'!$I92+Trenches!$K93)-(COUNTIF('Trial Pits'!$F$2:$F91,"NATIONAL")
  +COUNTIF(Trenches!$F$3:$F92,"NATIONAL"))`` (Calculator note: "(total TPs+STs) -
  (TP national + ST National)")
- D51  ``='Trial Pits'!$X92+'Trial Pits'!$Y92+Trenches!$AG93+Trenches!$AH93``
- D53  ``='Trial Pits'!$AA92+'Trial Pits'!$AB92+Trenches!$AI93+Trenches!$AJ93``
- D55  ``='Trial Pits'!$X96+'Trial Pits'!$Y96+Trenches!$AG97+Trenches!$AH97``

Text placeholders: D36 "Included in A2, A2.4, D3 to D19"; D43 "To be included
in item D13 to D15"; D50 and D50.2 "Included in Item D3 & D3.1". Everything
else is ``Not Required``.

Paved or non-paved
------------------
Column C of both sheets ('Paved/Non Paved') holds "PAVED" or "NON-PAVED"; the
model stores it as the ``paved`` flag.

For trial pits the paved items (D14, D16, D17) and non-paved items (D6, D7)
are filtered on that column. For trenches they are not: the Trenches sheet has
separate PAVED (columns M:P) and NON-PAVED (columns Y:AA) dimensions, and the
Calculator reads the totals row for each set regardless of column C. A trench
that crosses both kinds of ground therefore contributes to both D9/D10 and
D18/D19. Column C only decides whether the trench is counted in D3, D3.1 and
D4.

"Completed" is derived, not an input
------------------------------------
The Log Tracker's "Completed" columns are formulas, so the models carry no
``completed`` flag:

- ``'Trial Pits'!I     = IF(M2>0,1,0)``   recorded depth entered
- ``Trenches!K         = IF(J3>0,1,0)``   recorded total depth entered
- ``'Inspection pit'!H = IF(E2>0,1,0)``   recorded depth entered

Open items for review (by Havilah)
----------------------------------
Deliberate deviations (agreed 2026-10-01):

- **D16.** The Calculator formula adds the trial pits' hard-material volume
  (m³) to the trenches' 0-1.2 m depths for an item measured in metres of
  paved trial pit; the sheet's own note reads "Error in Calculating paved area
  trial pits". Translated instead on the pattern of D17:
  ``SUMIFS('Trial Pits'!$Q$2:$Q91,'Trial Pits'!$C$2:$C91,"PAVED")`` — the sum
  of the 0-1.2 m depth band over paved trial pits.
- **D19.** ``Trenches!$X93`` is an empty column. Translated as
  ``Trenches!$T93`` ("Volume 1.2-3"), the neighbour of the ``S93`` used by D18.
- **D1 / D2.** The inspection pit totals row sums rows 65-91 only
  (``=SUM(H65:H91)``). All inspection pits are summed.

- **3-4.5 m depth band.** ``'Trial Pits'!P`` is ``=IF(M2>4.5,4.5,MAX(0,M2-3))``
  and ``Trenches!AC`` is ``=IF(AA3>4.5,4.5,MAX(0,AA3-3))``. For a depth over
  4.5 m these return 4.5 m, although the band is only 1.5 m thick (every other
  band formula caps at the band's thickness: 3, 1.2, 1.8). The engine caps
  at 1.5 m. Depths up to 4.5 m are unaffected.

Translated literally:

- **D55.** Rows 96 ('Trial Pits') and 97 (Trenches) are empty, so the formula
  always gives 0. The Calculator's note says "Disposal material should match
  the amount of backfill in D51/D52".

Descriptions are verbatim, including the workbook's own slips (D46 reads
"Extra over Item D38" under the pumping items).
"""

from groundbill.models import InspectionPit, Project, Trench, TrialPit

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"


def compute_section_d(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section D BOQ items for the given project."""

    tps = project.trial_pits
    trenches = project.trenches
    ips = project.inspection_pits

    tp_non_paved = [tp for tp in tps if not tp.paved]
    tp_paved = [tp for tp in tps if tp.paved]
    tr_non_paved = [t for t in trenches if not t.paved]

    # 'Section D'!D12: ='[1]Inspection pit'!$H92        ('Inspection pit'!H92: =SUM(H65:H91))
    # Deliberate deviation: summed over all inspection pits, not rows 65-91 only.
    d1 = sum(_ip_h_completed(ip) for ip in ips)
    # 'Section D'!D13: ='[1]Inspection pit'!$J$92       ('Inspection pit'!J92: =SUM(J65:J91))
    # Deliberate deviation: summed over all inspection pits, not rows 65-91 only.
    d2 = sum(_ip_j_volume_of_hard_surface(ip) for ip in ips)

    # 'Section D'!D15:
    # =COUNTIF('[1]Trial Pits'!$C$2:$C91,"NON-PAVED")+COUNTIF([1]Trenches!$C$3:$C92,"NON-PAVED")
    d3 = len(tp_non_paved) + len(tr_non_paved)
    # 'Section D'!D16:
    # =COUNTIFS('[1]Trial Pits'!$C$2:$C91,"NON-PAVED",'[1]Trial Pits'!$B$2:$B91,"YES")
    #  +COUNTIFS([1]Trenches!$C$3:$C92,"NON-PAVED",[1]Trenches!$B$3:$B92,"YES")
    d3_1 = sum(1 for tp in tp_non_paved if tp.barrier) + sum(1 for t in tr_non_paved if t.barrier)
    # 'Section D'!D17:
    # =COUNTIFS('[1]Trial Pits'!$C$2:$C91,"NON-PAVED",'[1]Trial Pits'!$D$2:$D91,"YES")
    #  +COUNTIFS([1]Trenches!$C$3:$C92,"NON-PAVED",[1]Trenches!$D$3:$D92,"YES")
    d4 = sum(1 for tp in tp_non_paved if tp.slope_over_20pct) + sum(
        1 for t in tr_non_paved if t.slope_over_20pct
    )
    # 'Section D'!D19: =SUMIFS('[1]Trial Pits'!$O$2:$O91,'[1]Trial Pits'!$C$2:$C91,"NON-PAVED")
    d6 = sum(_tp_o_band_0_3(tp) for tp in tp_non_paved)
    # 'Section D'!D20: =SUMIFS('[1]Trial Pits'!$P$2:$P91,'[1]Trial Pits'!$C$2:$C91,"NON-PAVED")
    d7 = sum(_tp_p_band_3_4_5(tp) for tp in tp_non_paved)
    # 'Section D'!D22: =[1]Trenches!$AD93               (Trenches!AD93: =SUM(AD3:AD92))
    d9 = sum(_trench_ad_non_paved_volume_0_3(t) for t in trenches)
    # 'Section D'!D23: =[1]Trenches!$AE93               (Trenches!AE93: =SUM(AE3:AE92))
    d10 = sum(_trench_ae_non_paved_volume_3_4_5(t) for t in trenches)

    # 'Section D'!D26: =COUNTIFS('[1]Trial Pits'!$E$2:$E91,"YES")
    d12 = sum(1 for tp in tps if tp.traffic_management)
    # 'Section D'!D27: =COUNTIFS([1]Trenches!$E$3:$E92,"YES")
    d13 = sum(1 for t in trenches if t.traffic_management)
    # 'Section D'!D28:
    # =SUMIFS('[1]Trial Pits'!$T$2:$T91,'[1]Trial Pits'!$C$2:$C91,"PAVED")+[1]Trenches!$U93
    d14 = sum(_tp_t_perimeter(tp) for tp in tp_paved) + sum(
        _trench_u_paved_perimeter(t) for t in trenches
    )
    # 'Section D'!D29: ='[1]Trial Pits'!$V$92+[1]Trenches!$V93
    d15 = sum(_tp_v_volume_of_hard_material(tp) for tp in tps) + sum(
        _trench_v_volume_of_hard_material(t) for t in trenches
    )
    # 'Section D'!D30: ='[1]Trial Pits'!$V$92+[1]Trenches!$Q93
    # Deliberate deviation (see module docstring): translated on the pattern of D17 as
    # SUMIFS('Trial Pits'!$Q$2:$Q91,'Trial Pits'!$C$2:$C91,"PAVED").
    d16 = sum(_tp_q_band_0_1_2(tp) for tp in tp_paved)
    # 'Section D'!D31: =SUMIFS('[1]Trial Pits'!$R$2:$R91,'[1]Trial Pits'!$C$2:$C91,"PAVED")
    d17 = sum(_tp_r_band_1_2_3(tp) for tp in tp_paved)
    # 'Section D'!D32: =[1]Trenches!$S93                (Trenches!S93: =SUM(S3:S92))
    d18 = sum(_trench_s_paved_volume_0_1_2(t) for t in trenches)
    # 'Section D'!D33: =[1]Trenches!$X93
    # Deliberate deviation (see module docstring): column X is empty; Trenches!$T93 is used.
    d19 = sum(_trench_t_paved_volume_1_2_3(t) for t in trenches)
    # 'Section D'!D34: =D15*0.5                         (Calculator row 15 is item D3)
    d20 = d3 * 0.5

    # 'Section D'!D67:
    # =('[1]Trial Pits'!$I92+[1]Trenches!$K93)
    #  -(COUNTIF('[1]Trial Pits'!$F$2:$F91,"NATIONAL")+COUNTIF([1]Trenches!$F$3:$F92,"NATIONAL"))
    d49 = (
        sum(_tp_i_completed(tp) for tp in tps) + sum(_trench_k_completed(t) for t in trenches)
    ) - (
        sum(1 for tp in tps if tp.road == "NATIONAL")
        + sum(1 for t in trenches if t.road == "NATIONAL")
    )
    # 'Section D'!D70: ='[1]Trial Pits'!$X92+'[1]Trial Pits'!$Y92+[1]Trenches!$AG93+[1]Trenches!$AH93
    d51 = (
        sum(_tp_x_vol_804_rural(tp) for tp in tps)
        + sum(_tp_y_vol_804_national(tp) for tp in tps)
        + sum(_trench_ag_vol_804_rural(t) for t in trenches)
        + sum(_trench_ah_vol_804_national(t) for t in trenches)
    )
    # 'Section D'!D72: ='[1]Trial Pits'!$AA92+'[1]Trial Pits'!$AB92+[1]Trenches!$AI93+[1]Trenches!$AJ93
    d53 = (
        sum(_tp_aa_asphalt_area_rural(tp) for tp in tps)
        + sum(_tp_ab_asphalt_area_national(tp) for tp in tps)
        + sum(_trench_ai_asphalt_area_rural(t) for t in trenches)
        + sum(_trench_aj_asphalt_area_national(t) for t in trenches)
    )
    # 'Section D'!D74: ='[1]Trial Pits'!$X96+'[1]Trial Pits'!$Y96+[1]Trenches!$AG97+[1]Trenches!$AH97
    # Open item: all four cells are empty in the Log Tracker, so this is always 0.
    d55 = 0

    return [
        # 'Section D'!D12: ='[1]Inspection pit'!$H92
        BoqItem(
            code="D1",
            description="Excavate inspection pit by hand to 1.2m depth.",
            unit="nr",
            quantity=d1,
            subheading=(
                "Inspection pits Included for each exploratory hole: refer hand "
                "digging and CAT scan items at exploratory hole locations"
            ),
        ),
        # 'Section D'!D13: ='[1]Inspection pit'!$J$92
        BoqItem(
            code="D2",
            description="Extra over Item D1 for breaking out surface obstructions.",
            unit="m³",
            quantity=d2,
        ),
        # 'Section D'!D15: =COUNTIF('[1]Trial Pits'!$C$2:$C91,"NON-PAVED")+COUNTIF([1]Trenches!$C$3:$C92,"NON-PAVED")
        BoqItem(
            code="D3",
            description=(
                "Move equipment to the site of each trial pit or trench dismantle on "
                "completion and reinstate."
            ),
            unit="nr",
            quantity=d3,
            subheading="Trial pits and trenches (non paved areas)",
        ),
        # 'Section D'!D16: =COUNTIFS('[1]Trial Pits'!$C$2:$C91,"NON-PAVED",'[1]Trial Pits'!$B$2:$B91,"YES")+COUNTIFS([1]Trenches!$C$3:$C92,"NON-PAVED",[1]Trenches!$B$3:$B92,"YES")
        BoqItem(
            code="D3.1",
            description=(
                "Extra over item D3 for setting to the site of exploratory hole over "
                "safety barrier or other fence or wall, set up, dismantle on "
                "completion and reinstate."
            ),
            unit="nr",
            quantity=d3_1,
        ),
        # 'Section D'!D17: =COUNTIFS('[1]Trial Pits'!$C$2:$C91,"NON-PAVED",'[1]Trial Pits'!$D$2:$D91,"YES")+COUNTIFS([1]Trenches!$C$3:$C92,"NON-PAVED",[1]Trenches!$D$3:$D92,"YES")
        BoqItem(
            code="D4",
            description="Extra over Item D3 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=d4,
        ),
        # 'Section D'!D18: Not Required
        BoqItem(
            code="D5",
            description="Extra over Item D3 for trial pit or trench between 4.5 and 6m depth",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D19: =SUMIFS('[1]Trial Pits'!$O$2:$O91,'[1]Trial Pits'!$C$2:$C91,"NON-PAVED")
        BoqItem(
            code="D6",
            description="Excavate trial pit between existing ground level and 3m depth",
            unit="m",
            quantity=d6,
        ),
        # 'Section D'!D20: =SUMIFS('[1]Trial Pits'!$P$2:$P91,'[1]Trial Pits'!$C$2:$C91,"NON-PAVED")
        BoqItem(
            code="D7",
            description="As Item D6 but between 3.0 and 4.5m depth",
            unit="m",
            quantity=d7,
        ),
        # 'Section D'!D21: Not Required
        BoqItem(
            code="D8",
            description="As Item D6 but between 4.5 and 6m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D22: =[1]Trenches!$AD93
        BoqItem(
            code="D9",
            description="Excavate trial trench between existing ground level and 3.0m depth",
            unit="m³",
            quantity=d9,
        ),
        # 'Section D'!D23: =[1]Trenches!$AE93
        BoqItem(
            code="D10",
            description="As Item D9 between 3.0 and 4.5m in depth",
            unit="m³",
            quantity=d10,
        ),
        # 'Section D'!D24: Not Required
        BoqItem(
            code="D11",
            description="As Item D9 between 4.5 and 6m depth",
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D26: =COUNTIFS('[1]Trial Pits'!$E$2:$E91,"YES")
        BoqItem(
            code="D12",
            description=(
                "Set up trial pit in road area to include erection of traffic "
                "management systems (works supervised by Engineer/ Geologist with "
                "valid CSCS Card for signing, lighting and guarding at roadworks)"
            ),
            unit="nr",
            quantity=d12,
            subheading="Trial pits and trenches (paved areas)",
        ),
        # 'Section D'!D27: =COUNTIFS([1]Trenches!$E$3:$E92,"YES")
        BoqItem(
            code="D13",
            description=(
                "Set up slit trench in road area to include erection of traffic "
                "management systems (works supervised by Engineer/ Geologist with "
                "valid CSCS Card for signing, lighting and guarding at roadworks)"
            ),
            unit="nr",
            quantity=d13,
        ),
        # 'Section D'!D28: =SUMIFS('[1]Trial Pits'!$T$2:$T91,'[1]Trial Pits'!$C$2:$C91,"PAVED")+[1]Trenches!$U93
        BoqItem(
            code="D14",
            description="Saw cut paved areas in advance of the works",
            unit="ln m",
            quantity=d14,
        ),
        # 'Section D'!D29: ='[1]Trial Pits'!$V$92+[1]Trenches!$V93
        BoqItem(
            code="D15",
            description="Breaking out hard material or surface obstructions",
            unit="m³",
            quantity=d15,
        ),
        # 'Section D'!D30: ='[1]Trial Pits'!$V$92+[1]Trenches!$Q93 — deliberate deviation, see module docstring
        BoqItem(
            code="D16",
            description=(
                "Excavate trial pit in paved areas between ground level and 1.20m "
                "depth (works by either hand excavation or hand assisted machine "
                "excavation)"
            ),
            unit="m",
            quantity=d16,
        ),
        # 'Section D'!D31: =SUMIFS('[1]Trial Pits'!$R$2:$R91,'[1]Trial Pits'!$C$2:$C91,"PAVED")
        BoqItem(
            code="D17",
            description="As D16 but depth in range 1.2m to 3.0m",
            unit="m",
            quantity=d17,
        ),
        # 'Section D'!D32: =[1]Trenches!$S93
        BoqItem(
            code="D18",
            description=(
                "Excavate slit trench in paved areas between ground level and 1.2m "
                "depth (works by either hand excavation or hand assisted machine "
                "excavation)"
            ),
            unit="m³",
            quantity=d18,
        ),
        # 'Section D'!D33: =[1]Trenches!$X93 — deliberate deviation, see module docstring
        BoqItem(
            code="D19",
            description=(
                "Excavate slit trench in paved areas between 1.2m to 3.0m depth "
                "(works by either hand excavation or hand assisted machine "
                "excavation)"
            ),
            unit="m³",
            quantity=d19,
        ),
        # 'Section D'!D34: =D15*0.5
        BoqItem(
            code="D20",
            description=(
                "Standing time for excavation plant, equipment and crew for machine "
                "dug trial pit or trench"
            ),
            unit="h",
            quantity=d20,
        ),
        # 'Section D'!D36: Not Required
        BoqItem(
            code="D21",
            description=(
                "Move equipment to the site of each observation pit or trench of not "
                "greater than 4.5m depth"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Observation pits and trenches",
        ),
        # 'Section D'!D37: Not Required
        BoqItem(
            code="D22",
            description="Extra over Item D21 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D38: Not Required
        BoqItem(
            code="D23",
            description="Extra over Item D21 for trial pit or trench between 4.5 and 6m depth",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D39: Not Required
        BoqItem(
            code="D24",
            description="Excavate observation pit between existing ground level and 3.0m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D40: Not Required
        BoqItem(
            code="D25",
            description="As Item D24 but between 3.0 and 4.5m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D41: Not Required
        BoqItem(
            code="D26",
            description="As Item D24 but between 4.5 and 6m depth",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D42: Not Required
        BoqItem(
            code="D27",
            description="Extra over Item D24 for hand excavation",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D43: Not Required
        BoqItem(
            code="D28",
            description="Excavate observation trench between existing ground level and 3.0m depth",
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D44: Not Required
        BoqItem(
            code="D29",
            description="As Item D28 but between 3.0 and 4.5m depth",
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D45: Not Required
        BoqItem(
            code="D30",
            description="As Item D28 but between 4.5 and 6m depth",
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D46: Not Required
        BoqItem(
            code="D31",
            description="Extra over Item D28 for hand excavation",
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D47: Not Required
        BoqItem(
            code="D32",
            description="Extra over Items D24 to D26 for breaking out hard strata or obstructions",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D48: Not Required
        BoqItem(
            code="D33",
            description="Extra over Items D28 to D30 for breaking out hard strata or obstructions",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D49: Not Required
        BoqItem(
            code="D34",
            description=(
                "Standing time for excavation plant, equipment and crew for machine "
                "dug observation pit or trench"
            ),
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D50: Not Required
        BoqItem(
            code="D35",
            description=(
                "Standing time for excavation plant, equipment and crew for hand dug "
                "observation pit or trench"
            ),
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D52: Included in A2, A2.4, D3 to D19
        BoqItem(
            code="D36",
            description=(
                "Provision of excavation plant equipment and crew for machine dug "
                "trial pits or trenches as directed by the Investigation Supervisor, "
                "maximum depth 3.0m"
            ),
            unit="day",
            quantity="Included in A2, A2.4, D3 to D19",
            subheading="Daily provision of pitting crew and equipment",
        ),
        # 'Section D'!D53: Not Required
        BoqItem(
            code="D37",
            description="As Item D36 but between 3.0 and 4.5m depth",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D54: Not Required
        BoqItem(
            code="D38",
            description="As Item D36 but between 4.5 and 6.0m depth",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D55: Not Required
        BoqItem(
            code="D39",
            description=(
                "Provision of excavation plant, equipment and crew for machine-dug "
                "observation pit or trench as directed by the Investigation "
                "Supervisor, maximum depth 3.0m"
            ),
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D56: Not Required
        BoqItem(
            code="D40",
            description="As Item D39 but between 3.0 and 4.5m depth",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D57: Not Required
        BoqItem(
            code="D41",
            description="As Item D39 but between 4.5 and 6.0m depth",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D58: Not Required
        BoqItem(
            code="D42",
            description="As Item D39 but for hand excavation",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D59: To be included in item D13 to D15
        BoqItem(
            code="D43",
            description=(
                "Extra over Items D36 to D38 and D39 to D41 for breaking out hard "
                "strata or obstructions"
            ),
            unit="day",
            quantity="To be included in item D13 to D15",
        ),
        # 'Section D'!D61: Not Required
        BoqItem(
            code="D44",
            description="Bring pump to the position of each exploratory pit or trench",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="General",
        ),
        # 'Section D'!D62: Not Required
        BoqItem(
            code="D45",
            description="Pump water from pit or trench",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D63: Not Required
        BoqItem(
            code="D46",
            description=(
                "Extra over Item D38 for temporary storage, treatment and disposal of"
                " contaminated groundwater from trial pit or trench"
            ),
            unit="Provisional Sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D64: Not Required
        BoqItem(
            code="D47",
            description="Leave open observation pit or trench",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D65: Not Required
        BoqItem(
            code="D48",
            description="Leave open trial pit or trench",
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D67: =('[1]Trial Pits'!$I92+[1]Trenches!$K93)-(COUNTIF('[1]Trial Pits'!$F$2:$F91,"NATIONAL")+COUNTIF([1]Trenches!$F$3:$F92,"NATIONAL"))
        BoqItem(
            code="D49",
            description="Backfill trial pit or trench excavation with arisings/excavated materials",
            unit="nr",
            quantity=d49,
            subheading="Trial pit / slit trench backfill & reinstatement works",
        ),
        # 'Section D'!D68: Included in Item D3 & D3.1
        BoqItem(
            code="D50",
            description="Reinstate grassed surface to include replacing of sod",
            unit="m²",
            quantity="Included in Item D3 & D3.1",
        ),
        # 'Section D'!D69: Included in Item D3 & D3.1
        BoqItem(
            code="D50.2",
            description="Laying Turf Along Access Routes to Exploratory Holes",
            unit="m²",
            quantity="Included in Item D3 & D3.1",
        ),
        # 'Section D'!D70: ='[1]Trial Pits'!$X92+'[1]Trial Pits'!$Y92+[1]Trenches!$AG93+[1]Trenches!$AH93
        BoqItem(
            code="D51",
            description=(
                "Backfill trenches, trial pits and inspection pits at exploratory "
                "hole locations in paved areas with imported granular fill (CL 804 "
                "sub-base)"
            ),
            unit="m³",
            quantity=d51,
        ),
        # 'Section D'!D71: Not Required
        BoqItem(
            code="D52",
            description=(
                "Backfill trenches, trial pits and inspection pits at exploratory "
                "hole locations in paved areas with CBGMB as Fig.A4.0 Method A of "
                "TII's CC-PAV-04007"
            ),
            unit="m³",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D72: ='[1]Trial Pits'!$AA92+'[1]Trial Pits'!$AB92+[1]Trenches!$AI93+[1]Trenches!$AJ93
        BoqItem(
            code="D53",
            description=(
                "Reinstatement of asphalt/bituminous pavement in accordance with "
                "TII's CC-PAV-04007."
            ),
            unit="m²",
            quantity=d53,
        ),
        # 'Section D'!D73: Not Required
        BoqItem(
            code="D54",
            description="Repair of road markings",
            unit="ln m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section D'!D74: ='[1]Trial Pits'!$X96+'[1]Trial Pits'!$Y96+[1]Trenches!$AG97+[1]Trenches!$AH97 — empty cells, always 0
        BoqItem(
            code="D55",
            description=(
                "Disposal of excess or surplus inert arisings from trial pits or "
                "trenches (where imported granular fill or lean mix concrete is used "
                "as backfill)"
            ),
            unit="m³",
            quantity=d55,
        ),
    ]


# ---------------------------------------------------------------------------
# 'Trial Pits' sheet derived columns (K = Width, L = Length, M = Depth,
# N = Depth of Hard Material, F = Road). Blank cells count as 0, as in Excel.
# ---------------------------------------------------------------------------


def _tp_i_completed(tp: TrialPit) -> int:
    """'Trial Pits'!I: =IF(M2>0, 1, 0)"""
    return 1 if (tp.depth_m or 0.0) > 0 else 0


def _tp_o_band_0_3(tp: TrialPit) -> float:
    """'Trial Pits'!O: =IF(M2>3, 3, M2)"""
    m = tp.depth_m or 0.0
    return 3.0 if m > 3 else m


def _tp_p_band_3_4_5(tp: TrialPit) -> float:
    """'Trial Pits'!P: =IF(M2>4.5,4.5,MAX(0,M2-3))

    Deliberate deviation (see module docstring): the workbook returns 4.5
    for depths over 4.5 m; the band is 1.5 m thick, so 1.5 is returned here.
    """
    m = tp.depth_m or 0.0
    return 1.5 if m > 4.5 else max(0.0, m - 3)


def _tp_q_band_0_1_2(tp: TrialPit) -> float:
    """'Trial Pits'!Q: =IF(M2>1.2, 1.2, M2)"""
    m = tp.depth_m or 0.0
    return 1.2 if m > 1.2 else m


def _tp_r_band_1_2_3(tp: TrialPit) -> float:
    """'Trial Pits'!R: =IF(M2>3,1.8,MAX(0,M2-1.2))"""
    m = tp.depth_m or 0.0
    return 1.8 if m > 3 else max(0.0, m - 1.2)


def _tp_t_perimeter(tp: TrialPit) -> float:
    """'Trial Pits'!T: =(2*K2)+(2*L2)"""
    return 2 * (tp.width_m or 0.0) + 2 * (tp.length_m or 0.0)


def _tp_v_volume_of_hard_material(tp: TrialPit) -> float:
    """'Trial Pits'!V: =K2*L2*N2"""
    return (tp.width_m or 0.0) * (tp.length_m or 0.0) * (tp.depth_of_hard_material_m or 0.0)


def _tp_x_vol_804_rural(tp: TrialPit) -> float:
    """'Trial Pits'!X: =IF(F2="RURAL",K2*L2*(M2-0.1),0)"""
    if tp.road != "RURAL":
        return 0.0
    return (tp.width_m or 0.0) * (tp.length_m or 0.0) * ((tp.depth_m or 0.0) - 0.1)


def _tp_y_vol_804_national(tp: TrialPit) -> float:
    """'Trial Pits'!Y: =IF(F2="NATIONAL",(M2-0.45)*K2*L2,0)"""
    if tp.road != "NATIONAL":
        return 0.0
    return ((tp.depth_m or 0.0) - 0.45) * (tp.width_m or 0.0) * (tp.length_m or 0.0)


def _tp_aa_asphalt_area_rural(tp: TrialPit) -> float:
    """'Trial Pits'!AA: =IF(F2="RURAL",(K2+0.2)*(L2+0.2),0)"""
    if tp.road != "RURAL":
        return 0.0
    return ((tp.width_m or 0.0) + 0.2) * ((tp.length_m or 0.0) + 0.2)


def _tp_ab_asphalt_area_national(tp: TrialPit) -> float:
    """'Trial Pits'!AB: =IF(F2="NATIONAL",K2*L2,0)"""
    if tp.road != "NATIONAL":
        return 0.0
    return (tp.width_m or 0.0) * (tp.length_m or 0.0)


# ---------------------------------------------------------------------------
# 'Inspection pit' sheet derived columns (E = Recorded Depth, F = Recorded
# length, G = Recorded Width, I = Depth of hard Surface obstruction).
# ---------------------------------------------------------------------------


def _ip_h_completed(ip: InspectionPit) -> int:
    """'Inspection pit'!H: =IF(E2>0,1,0)"""
    return 1 if (ip.recorded_depth_m or 0.0) > 0 else 0


def _ip_j_volume_of_hard_surface(ip: InspectionPit) -> float:
    """'Inspection pit'!J: =F2*G2*I2"""
    return (
        (ip.recorded_length_m or 0.0)
        * (ip.recorded_width_m or 0.0)
        * (ip.depth_hard_surface_obstruction_m or 0.0)
    )


# ---------------------------------------------------------------------------
# 'Trenches' sheet derived columns.
# OVERALL: J = Recorded Total Depth.
# PAVED: M = Length, N = Width, O = Depth, P = Depth Hard Material.
# NON-PAVED: Y = Length, Z = Width, AA = Depth.  F = ROAD.
# ---------------------------------------------------------------------------


def _trench_k_completed(t: Trench) -> int:
    """Trenches!K: =IF(J3>0,1,0)"""
    return 1 if (t.overall_total_depth_m or 0.0) > 0 else 0


def _trench_q_paved_band_0_1_2(t: Trench) -> float:
    """Trenches!Q: =IF(O3>1.2, 1.2, O3)"""
    o = t.paved_depth_m or 0.0
    return 1.2 if o > 1.2 else o


def _trench_r_paved_band_1_2_3(t: Trench) -> float:
    """Trenches!R: =IF(O3>3,1.8,MAX(0,O3-1.2))"""
    o = t.paved_depth_m or 0.0
    return 1.8 if o > 3 else max(0.0, o - 1.2)


def _trench_s_paved_volume_0_1_2(t: Trench) -> float:
    """Trenches!S: =M3*N3*Q3"""
    return (t.paved_length_m or 0.0) * (t.paved_width_m or 0.0) * _trench_q_paved_band_0_1_2(t)


def _trench_t_paved_volume_1_2_3(t: Trench) -> float:
    """Trenches!T: =M3*N3*R3"""
    return (t.paved_length_m or 0.0) * (t.paved_width_m or 0.0) * _trench_r_paved_band_1_2_3(t)


def _trench_u_paved_perimeter(t: Trench) -> float:
    """Trenches!U: =(2*M3)+(2*N3)"""
    return 2 * (t.paved_length_m or 0.0) + 2 * (t.paved_width_m or 0.0)


def _trench_v_volume_of_hard_material(t: Trench) -> float:
    """Trenches!V: =M3*N3*P3"""
    return (
        (t.paved_length_m or 0.0)
        * (t.paved_width_m or 0.0)
        * (t.paved_depth_hard_material_m or 0.0)
    )


def _trench_ab_non_paved_band_0_3(t: Trench) -> float:
    """Trenches!AB: =IF(AA3>3, 3, AA3)"""
    aa = t.non_paved_depth_m or 0.0
    return 3.0 if aa > 3 else aa


def _trench_ac_non_paved_band_3_4_5(t: Trench) -> float:
    """Trenches!AC: =IF(AA3>4.5,4.5,MAX(0,AA3-3))

    Deliberate deviation (see module docstring): the workbook returns 4.5
    for depths over 4.5 m; the band is 1.5 m thick, so 1.5 is returned here.
    """
    aa = t.non_paved_depth_m or 0.0
    return 1.5 if aa > 4.5 else max(0.0, aa - 3)


def _trench_ad_non_paved_volume_0_3(t: Trench) -> float:
    """Trenches!AD: =Y3*Z3*AB3"""
    return (
        (t.non_paved_length_m or 0.0)
        * (t.non_paved_width_m or 0.0)
        * _trench_ab_non_paved_band_0_3(t)
    )


def _trench_ae_non_paved_volume_3_4_5(t: Trench) -> float:
    """Trenches!AE: =Y3*Z3*AC3"""
    return (
        (t.non_paved_length_m or 0.0)
        * (t.non_paved_width_m or 0.0)
        * _trench_ac_non_paved_band_3_4_5(t)
    )


def _trench_ag_vol_804_rural(t: Trench) -> float:
    """Trenches!AG: =IF(F3="RURAL",M3*N3*(O3-0.1),0)"""
    if t.road != "RURAL":
        return 0.0
    return (t.paved_length_m or 0.0) * (t.paved_width_m or 0.0) * ((t.paved_depth_m or 0.0) - 0.1)


def _trench_ah_vol_804_national(t: Trench) -> float:
    """Trenches!AH: =IF(F3="NATIONAL",(O3-0.45)*M3*N3,0)"""
    if t.road != "NATIONAL":
        return 0.0
    return ((t.paved_depth_m or 0.0) - 0.45) * (t.paved_length_m or 0.0) * (t.paved_width_m or 0.0)


def _trench_ai_asphalt_area_rural(t: Trench) -> float:
    """Trenches!AI: =IF(F3="RURAL",(M3+0.2)*(N3+0.2),0)"""
    if t.road != "RURAL":
        return 0.0
    return ((t.paved_length_m or 0.0) + 0.2) * ((t.paved_width_m or 0.0) + 0.2)


def _trench_aj_asphalt_area_national(t: Trench) -> float:
    """Trenches!AJ: =IF(F3="NATIONAL",M3*N3,0)"""
    if t.road != "NATIONAL":
        return 0.0
    return (t.paved_length_m or 0.0) * (t.paved_width_m or 0.0)
