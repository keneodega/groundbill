"""Section F — Probing and cone penetration testing.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section F' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section F', which reads
the `DPH` and `CPT` sheets of the Log Tracker
(`reference/excel/1_BOQ_Log_Rev_A.xlsx`).

Formulas — dynamic probing (DPH)
--------------------------------
- F1  ``=DPH!$H122``                     number of probes
- F2  ``=COUNTIF(DPH!$B$2:$B121,"YES")`` probes on a slope > 20%
- F3  ``=DPH!$D122``                     metres probed between 0 and 5 m
- F4  ``=DPH!$E122``                     metres probed between 5 and 10 m
- F5  ``=DPH!$F122``                     metres probed between 10 and 15 m
- F6  ``=D11/2``                         F1 ÷ 2 (Calculator note: "1/2 hr per
  probe assumed")
- F7  ``Not Required``

Formulas — cone penetration testing (CPT)
-----------------------------------------
- F8  ``=CPT!$K92``                      number of CPTs
- F9  ``=COUNTIF(CPT!$B$2:$B91,"YES")``  CPTs on a slope > 20%
- F10 ``=CPT!$F92``                      metres between 0 and 10 m
- F11 ``=CPT!$G92``                      metres between 10 and 20 m
- F12 ``=CPT!$H92``                      metres between 20 and 30 m
- F13 ``=CPT!$I92``                      metres between 30 and 40 m
- F18 ``=D19/2``                         F8 ÷ 2 (Calculator note: "1/2 hr per
  test")
- F14-F17, F19-F22 ``Not Required``

Log Tracker derived columns
---------------------------
DPH sheet (C = "Depth"):

- ``D = IF(C>5,5,C)``                0-5 m band
- ``E = IF(C>10,5,MAX(0,C-5))``      5-10 m band
- ``F = IF(C>15,5,MAX(0,C-10))``     10-15 m band
- ``H = IF(C>0,1,0)``                "Completed"

CPT sheet (D = "DEPTH"):

- ``F = IF(D>10,10,D)``              0-10 m band
- ``G = IF(D>20,10,MAX(0,D-10))``    10-20 m band
- ``H = IF(D>30,10,MAX(0,D-20))``    20-30 m band
- ``I = IF(D>40,10,MAX(0,D-30))``    30-40 m band
- ``K = IF(D>0,1,0)``                "Completed"

Depth beyond the last band (15 m for probes, 40 m for CPTs) is not measured
under any item, exactly as in the workbook.

"Completed" is derived, not an input
------------------------------------
The Log Tracker's "Completed" columns are formulas (1 when a depth has been
entered), so the models carry no ``completed`` flag: every probe or CPT with a
depth counts.

Notes for review (by Havilah)
-----------------------------
- The DPH totals row sums the band columns over rows 2-120
  (``=SUM(D2:D120)``) but the "Completed" column over rows 2-121, and F2
  counts slopes over rows 2-121. Row 121 would therefore be counted as a probe
  without its metres. Treated as a slip, in line with the inspection pit
  totals decision: every probe's metres are summed.
- The CPT sheet's "Piezocone" column (C) is not read by any Calculator
  formula; F14 ("Extra over ... for use of piezocone") is ``Not Required``.
  The model's ``piezocone`` flag therefore has no effect on Section F.
"""

from groundbill.models import CPT, DynamicProbe, Project

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"


def compute_section_f(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section F BOQ items for the given project."""

    probes = project.dynamic_probes
    cpts = project.cpts

    # 'Section F'!D11: =[1]DPH!$H122          (DPH!H122: =SUM(H2:H121))
    f1 = sum(_dph_h_completed(dp) for dp in probes)
    # 'Section F'!D12: =COUNTIF([1]DPH!$B$2:$B121,"YES")
    f2 = sum(1 for dp in probes if dp.slope_over_20pct)
    # 'Section F'!D13: =[1]DPH!$D122          (DPH!D122: =SUM(D2:D120))
    f3 = sum(_dph_d_band_0_5(dp) for dp in probes)
    # 'Section F'!D14: =[1]DPH!$E122          (DPH!E122: =SUM(E2:E120))
    f4 = sum(_dph_e_band_5_10(dp) for dp in probes)
    # 'Section F'!D15: =[1]DPH!$F122          (DPH!F122: =SUM(F2:F120))
    f5 = sum(_dph_f_band_10_15(dp) for dp in probes)
    # 'Section F'!D16: =D11/2
    f6 = f1 / 2

    # 'Section F'!D19: =[1]CPT!$K92           (CPT!K92: =SUM(K2:K91))
    f8 = sum(_cpt_k_completed(c) for c in cpts)
    # 'Section F'!D20: =COUNTIF([1]CPT!$B$2:$B91,"YES")
    f9 = sum(1 for c in cpts if c.slope_over_20pct)
    # 'Section F'!D21: =[1]CPT!$F92           (CPT!F92: =SUM(F2:F91))
    f10 = sum(_cpt_f_band_0_10(c) for c in cpts)
    # 'Section F'!D22: =[1]CPT!$G92           (CPT!G92: =SUM(G2:G91))
    f11 = sum(_cpt_g_band_10_20(c) for c in cpts)
    # 'Section F'!D23: =[1]CPT!$H92           (CPT!H92: =SUM(H2:H91))
    f12 = sum(_cpt_h_band_20_30(c) for c in cpts)
    # 'Section F'!D24: =[1]CPT!$I92           (CPT!I92: =SUM(I2:I91))
    f13 = sum(_cpt_i_band_30_40(c) for c in cpts)
    # 'Section F'!D29: =D19/2
    f18 = f8 / 2

    return [
        # 'Section F'!D11: =[1]DPH!$H122
        BoqItem(
            code="F1",
            description="Bring dynamic probe (DPH) equipment to the site of each test location",
            unit="nr",
            quantity=f1,
            subheading="Dynamic probing (DPH)",
        ),
        # 'Section F'!D12: =COUNTIF([1]DPH!$B$2:$B121,"YES")
        BoqItem(
            code="F2",
            description="Extra over Item F1 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=f2,
        ),
        # 'Section F'!D13: =[1]DPH!$D122
        BoqItem(
            code="F3",
            description="Carry out dynamic probe test from existing ground level to 5m depth",
            unit="m",
            quantity=f3,
        ),
        # 'Section F'!D14: =[1]DPH!$E122
        BoqItem(
            code="F4",
            description="As Item F3 but between 5 and 10m depth",
            unit="m",
            quantity=f4,
        ),
        # 'Section F'!D15: =[1]DPH!$F122
        BoqItem(
            code="F5",
            description="As Item F3 but between 10 and 15m depth",
            unit="m",
            quantity=f5,
        ),
        # 'Section F'!D16: =D11/2
        BoqItem(
            code="F6",
            description="Standing time for dynamic probe test equipment and crew",
            unit="h",
            quantity=f6,
        ),
        # 'Section F'!D17: Not Required
        BoqItem(
            code="F7",
            description=(
                "Provision of dynamic probing equipment and crew for probing as "
                "directed by the Investigation Supervisor; maximum depth 15m"
            ),
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D19: =[1]CPT!$K92
        BoqItem(
            code="F8",
            description=(
                "Bring static cone penetration test equipment to the site of each " "test location"
            ),
            unit="nr",
            quantity=f8,
            subheading="Cone penetration testing",
        ),
        # 'Section F'!D20: =COUNTIF([1]CPT!$B$2:$B91,"YES")
        BoqItem(
            code="F9",
            description="Extra over Item F8 for setting up on a slope of gradient greater than 20%",
            unit="nr",
            quantity=f9,
        ),
        # 'Section F'!D21: =[1]CPT!$F92
        BoqItem(
            code="F10",
            description=(
                "Carry out static cone penetration test measuring both cone and "
                "sleeve resistance from existing ground level to 10m depth"
            ),
            unit="m",
            quantity=f10,
        ),
        # 'Section F'!D22: =[1]CPT!$G92
        BoqItem(
            code="F11",
            description="As Item F10 but between 10 and 20m depth",
            unit="m",
            quantity=f11,
        ),
        # 'Section F'!D23: =[1]CPT!$H92
        BoqItem(
            code="F12",
            description="As Item F10 but between 20 and 30m depth",
            unit="m",
            quantity=f12,
        ),
        # 'Section F'!D24: =[1]CPT!$I92
        BoqItem(
            code="F13",
            description="As Item F10 but between 30 and 40m depth",
            unit="m",
            quantity=f13,
        ),
        # 'Section F'!D25: Not Required
        BoqItem(
            code="F14",
            description="Extra over Items F10 to F13 for use of piezocone",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D26: Not Required
        BoqItem(
            code="F15",
            description="Extra over Items F10 to F13 for interpretation of CPT/CPTU data",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D27: Not Required
        BoqItem(
            code="F16",
            description="Carry out dissipation test up to 1 hour duration",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D28: Not Required
        BoqItem(
            code="F17",
            description="Extra over Item F16 for test duration exceeding 1 hour",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D29: =D19/2
        BoqItem(
            code="F18",
            description="Standing time for static cone penetration test equipment and crew",
            unit="h",
            quantity=f18,
        ),
        # 'Section F'!D30: Not Required
        BoqItem(
            code="F19",
            description="Extra over Items F10 to F13 for use of seismic cone",
            unit="m",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D31: Not Required
        BoqItem(
            code="F20",
            description="Carry out seismic cone test",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D32: Not Required
        BoqItem(
            code="F21",
            description="Extra over Item F20 for interpretation of seismic cone data",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section F'!D33: Not Required
        BoqItem(
            code="F22",
            description="Standing time for seismic cone test equipment and crew",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
    ]


# --- DPH sheet derived columns (one function per Log Tracker column) ---


def _dph_d_band_0_5(dp: DynamicProbe) -> float:
    """DPH!D: =IF(C2>5,5,C2)"""
    return 5.0 if dp.depth_m > 5 else dp.depth_m


def _dph_e_band_5_10(dp: DynamicProbe) -> float:
    """DPH!E: =IF(C2>10,5,MAX(0,C2-5))"""
    return 5.0 if dp.depth_m > 10 else max(0.0, dp.depth_m - 5)


def _dph_f_band_10_15(dp: DynamicProbe) -> float:
    """DPH!F: =IF(C2>15,5,MAX(0,C2-10))"""
    return 5.0 if dp.depth_m > 15 else max(0.0, dp.depth_m - 10)


def _dph_h_completed(dp: DynamicProbe) -> int:
    """DPH!H: =IF(C2>0,1,0)"""
    return 1 if dp.depth_m > 0 else 0


# --- CPT sheet derived columns ---


def _cpt_f_band_0_10(cpt: CPT) -> float:
    """CPT!F: =IF(D2>10,10,D2)"""
    return 10.0 if cpt.depth_m > 10 else cpt.depth_m


def _cpt_g_band_10_20(cpt: CPT) -> float:
    """CPT!G: =IF(D2>20,10,MAX(0,D2-10))"""
    return 10.0 if cpt.depth_m > 20 else max(0.0, cpt.depth_m - 10)


def _cpt_h_band_20_30(cpt: CPT) -> float:
    """CPT!H: =IF(D2>30,10,MAX(0,D2-20))"""
    return 10.0 if cpt.depth_m > 30 else max(0.0, cpt.depth_m - 20)


def _cpt_i_band_30_40(cpt: CPT) -> float:
    """CPT!I: =IF(D2>40,10,MAX(0,D2-30))"""
    return 10.0 if cpt.depth_m > 40 else max(0.0, cpt.depth_m - 30)


def _cpt_k_completed(cpt: CPT) -> int:
    """CPT!K: =IF(D2>0,1,0)"""
    return 1 if cpt.depth_m > 0 else 0
