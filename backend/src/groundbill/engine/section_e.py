"""Section E — Sampling and Monitoring.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section E'
(with cross-references to the Log Tracker workbook's `Boreholes`, `Trial Pits`,
`Trenches`, `Inspection pit`, and `Dynamic Sampling` sheets).

Key formula: Boreholes!K92 = total CP drilling depth
-------------------------------------------------
This is ``SUM(K2:K91)`` where K = "CP Drilling Total Depth". In our model:

.. code-block:: python

    total_cp_depth = sum(
        phase.depth_m for bh in project.boreholes for phase in bh.phases
        if phase.method == DrillingMethod.CABLE_PERCUSSION
    )

E2 components
-------------
- Boreholes!K92 → total CP drilling depth
- Trial Pits!M92 → sum of TP depth (col M = actual depth recorded)
- Trenches!N93 → None in the spreadsheet (col N = "Recorded Width").
  **Flagged for review**: translated literally as 0.
- Inspection pit!E92 → sum of recorded depth
- Dynamic Sampling!C92 → sum of depth_m

E12 — EV test count
--------------------
Counts holes that have ``EV`` in their test selections across all hole types.
For boreholes and dynamic samples, ``EV`` is in the ``PSEVTest`` enum (tests
field). For trial pits, trenches, and inspection pits, ``EV`` is in the
``InSituTest`` enum (in_situ_tests field).
"""

from groundbill.models import DrillingMethod, InSituTest, Project, PSEVTest

from .boq_items import BoqItem

_CP = DrillingMethod.CABLE_PERCUSSION


def compute_section_e(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section E BOQ items for the given project."""

    # --- Total CP drilling depth (Boreholes!K92) ---
    total_cp_depth = sum(
        phase.depth_m for bh in project.boreholes for phase in bh.phases if phase.method is _CP
    )

    # --- Sum of TP depth (Trial Pits!M92) ---
    tp_depth_sum = sum(tp.depth_m or 0.0 for tp in project.trial_pits)

    # --- Trenches!N93 is None in spreadsheet — produces 0 (flagged for review) ---
    trench_tub_count = 0

    # --- Sum of IP recorded depth (Inspection pit!E92) ---
    ip_depth_sum = sum(ip.recorded_depth_m or 0.0 for ip in project.inspection_pits)

    # --- Sum of DS depth (Dynamic Sampling!C92) ---
    ds_depth_sum = sum(ds.depth_m for ds in project.dynamic_samples)

    # --- E2: Total tub sample count ---
    e2 = total_cp_depth + tp_depth_sum + trench_tub_count + ip_depth_sum + ds_depth_sum

    # --- E3: Bulk sample count = E2 ---
    e3 = e2

    # --- E4: Large bulk sample = E2 / 10 ---
    e4 = e2 / 10 if e2 else 0

    # --- E5: Thick-walled samples = total CP depth / 5 ---
    e5 = total_cp_depth / 5 if total_cp_depth else 0

    # --- E6: Thin-walled = E5 ---
    e6 = e5

    # --- E8.1: Extra thick-walled 10-20 m = total CP depth / 10 ---
    e8_1 = total_cp_depth / 10 if total_cp_depth else 0

    # --- E8.2: Extra thin-walled 10-20 m = total CP depth / 10 ---
    e8_2 = total_cp_depth / 10 if total_cp_depth else 0

    # --- E12: Count of holes with EV in their test selections ---
    ev_count = 0
    ev_count += sum(1 for tp in project.trial_pits if InSituTest.EV in tp.in_situ_tests)
    ev_count += sum(1 for ip in project.inspection_pits if InSituTest.EV in ip.in_situ_tests)
    ev_count += sum(1 for t in project.trenches if InSituTest.EV in t.in_situ_tests)
    ev_count += sum(1 for bh in project.boreholes if PSEVTest.EV in bh.tests)
    ev_count += sum(1 for ds in project.dynamic_samples if PSEVTest.EV in ds.tests)

    # --- E16: Suite I = Suite E count (= E12) ---
    e16 = ev_count

    return [
        BoqItem(
            code="E1",
            description="Tub samples — general provision",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E2",
            description=(
                "Tub samples taken at regular depth intervals from cable "
                "percussion boreholes, trial pits, trenches, inspection pits, "
                "and dynamic samples"
            ),
            unit="nr",
            quantity=e2,
        ),
        BoqItem(
            code="E3",
            description="Bulk samples",
            unit="nr",
            quantity=e3,
        ),
        BoqItem(
            code="E4",
            description="Large bulk samples",
            unit="nr",
            quantity=e4,
        ),
        BoqItem(
            code="E5",
            description="Thick-walled driven samples (U100)",
            unit="nr",
            quantity=e5,
        ),
        BoqItem(
            code="E6",
            description="Thin-walled driven or pushed samples",
            unit="nr",
            quantity=e6,
        ),
        BoqItem(
            code="E7",
            description="Piston samples",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E8.1",
            description=(
                "Extra over Items E5 for thick-walled driven sample taken "
                "between 10 m and 20 m depth"
            ),
            unit="nr",
            quantity=e8_1,
        ),
        BoqItem(
            code="E8.2",
            description=(
                "Extra over Items E6 for thin-walled driven or pushed sample "
                "taken between 10 m and 20 m depth"
            ),
            unit="nr",
            quantity=e8_2,
        ),
        BoqItem(
            code="E8.3",
            description=("Extra over Items E5/E6 for samples taken between 20 m and " "30 m depth"),
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E9",
            description="Water samples",
            unit="nr",
            quantity=None,
        ),
        BoqItem(
            code="E10",
            description="Gas samples",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E11",
            description="SPT — Standard Penetration Test",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E12",
            description=("Suite E — environmental sampling (soil and/or groundwater)"),
            unit="nr",
            quantity=ev_count,
        ),
        BoqItem(
            code="E13",
            description="Suite F — WAC testing",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E14",
            description="Suite G — asbestos in soil screening",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E15",
            description="Suite H — additional environmental testing",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="E16",
            description="Suite I — environmental monitoring installations",
            unit="nr",
            quantity=e16,
        ),
        BoqItem(
            code="E17",
            description="Suite J — additional monitoring",
            unit="nr",
            quantity="Not Required",
        ),
    ]
