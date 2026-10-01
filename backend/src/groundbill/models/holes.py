"""Exploratory-hole domain models.

Each class corresponds to one sheet in the Log Tracker workbook
(`reference/excel/1_BOQ_Log_Rev_A.xlsx`). Fields map to input columns only;
derived columns (depth bands, volumes, areas) are computed by the calculation
engine rather than stored on the model.
"""

from pydantic import BaseModel, ConfigDict, Field

from .enums import DrillingMethod, InSituTest, PiezometerType, PSEVTest


class _HoleBase(BaseModel):
    """Shared configuration — forbid unknown fields so mapping stays explicit."""

    model_config = ConfigDict(extra="forbid")


class DrillingPhase(BaseModel):
    """One drilling phase within a borehole (e.g. 10 m of cable percussion)."""

    model_config = ConfigDict(extra="forbid")

    method: DrillingMethod
    depth_m: float = Field(gt=0)


class Borehole(_HoleBase):
    """Source sheet: 'Boreholes'.

    Columns N-Q, W-Z, AG-AJ, AQ-AT, BA-BD (the 0-10 / 10-20 / 20-30 / 30-40
    depth bands per drilling method) are derived by the engine and therefore
    not present here.
    """

    hole_number: str = Field(description="Col A — 'Hole Number'")
    phases: list[DrillingPhase] = Field(
        default_factory=list,
        description="Col B + per-method depth columns — one entry per drilling phase",
    )
    over_barrier_wall_fence: bool = Field(default=False, description="Col C")
    slope_over_20pct: bool = Field(default=False, description="Col D — 'Slope > 20%'")
    total_schedule_depth_m: float = Field(gt=0, description="Col F")
    tests: set[PSEVTest] = Field(default_factory=set, description="Col G — 'Tests P/S/EV'")
    total_depth_m: float | None = Field(default=None, description="Col H — actual depth achieved")
    cp_completed: bool = Field(default=False, description="Col I")
    road: str | None = Field(default=None, description="Col BH — 'ROAD'")
    piezometer_type: PiezometerType = Field(
        default=PiezometerType.NONE, description="Col BI — 'Piezometer'"
    )
    piezometer_plain_depth_m: float | None = Field(default=None, description="Col BJ")
    standpipe_diameter_mm: int | None = Field(default=None, description="Col BL")
    standpipe_plain_depth_m: float | None = Field(default=None, description="Col BM")
    standpipe_slotted_depth_m: float | None = Field(default=None, description="Col BN")
    installation_complete: bool = Field(default=False, description="Col BP — 'PIE/SP Complete'")


class TrialPit(_HoleBase):
    """Source sheet: 'Trial Pits'.

    Derived columns (I 'Completed', ``=IF(M2>0,1,0)``; O-R depth bands;
    T-Y perimeter / area / volumes; AA-AB asphalt areas) are computed by the
    engine.
    """

    trial_pit_number: str = Field(description="Col A")
    barrier: bool = Field(default=False, description="Col B")
    paved: bool = Field(default=False, description="Col C — 'Paved / Non Paved'")
    slope_over_20pct: bool = Field(default=False, description="Col D")
    traffic_management: bool = Field(default=False, description="Col E")
    road: str | None = Field(default=None, description="Col F")
    schedule_depth_m: float = Field(gt=0, description="Col H")
    in_situ_tests: set[InSituTest] = Field(
        default_factory=set, description="Col J — 'Insitu Tests'"
    )
    width_m: float | None = Field(default=None, description="Col K (Excel header: 'Witdh')")
    length_m: float | None = Field(default=None, description="Col L")
    depth_m: float | None = Field(default=None, description="Col M")
    depth_of_hard_material_m: float | None = Field(default=None, description="Col N")


class Trench(_HoleBase):
    """Source sheet: 'Trenches'.

    A single trench can cross paved and non-paved ground, so three dimension
    sets are captured: OVERALL (cols H-J), PAVED (cols M-P), NON-PAVED
    (cols Y-AA). Derived columns (K 'completed', ``=IF(J3>0,1,0)``; volumes
    and areas) are computed by the engine.
    """

    trench_number: str = Field(description="Col A — 'Trench'")
    barrier: bool = Field(default=False, description="Col B")
    paved: bool = Field(default=False, description="Col C")
    slope_over_20pct: bool = Field(default=False, description="Col D")
    traffic_management: bool = Field(default=False, description="Col E")
    road: str | None = Field(default=None, description="Col F")
    in_situ_tests: set[InSituTest] = Field(default_factory=set, description="Col G — 'TESTS'")
    overall_length_m: float | None = Field(default=None, description="Col H")
    overall_width_m: float | None = Field(default=None, description="Col I")
    overall_total_depth_m: float | None = Field(default=None, description="Col J")
    paved_length_m: float | None = Field(default=None, description="Col M")
    paved_width_m: float | None = Field(default=None, description="Col N")
    paved_depth_m: float | None = Field(default=None, description="Col O")
    paved_depth_hard_material_m: float | None = Field(default=None, description="Col P")
    non_paved_length_m: float | None = Field(default=None, description="Col Y")
    non_paved_width_m: float | None = Field(default=None, description="Col Z")
    non_paved_depth_m: float | None = Field(default=None, description="Col AA")


class InspectionPit(_HoleBase):
    """Source sheet: 'Inspection pit' (Excel header 'Inspectoin Pit' is a typo).

    Derived columns (H 'Completed', ``=IF(E2>0,1,0)``; J 'Volume of hard
    Surface', ``=F2*G2*I2``) are computed by the engine.
    """

    inspection_pit_number: str = Field(description="Col A")
    scheduled_depth_m: float = Field(gt=0, description="Col B")
    scheduled_length_m: float | None = Field(default=None, description="Col C")
    scheduled_width_m: float | None = Field(default=None, description="Col D")
    recorded_depth_m: float | None = Field(default=None, description="Col E")
    recorded_length_m: float | None = Field(default=None, description="Col F")
    recorded_width_m: float | None = Field(default=None, description="Col G")
    depth_hard_surface_obstruction_m: float | None = Field(default=None, description="Col I")
    in_situ_tests: set[InSituTest] = Field(
        default_factory=set, description="Col K — 'Insitu Tests'"
    )


class DynamicSample(_HoleBase):
    """Source sheet: 'Dynamic Sampling'."""

    sample_number: str = Field(description="Col A — 'Sample'")
    slope_over_20pct: bool = Field(default=False, description="Col B")
    depth_m: float = Field(gt=0, description="Col C")
    completed: bool = Field(default=False, description="Col H")
    road: str | None = Field(default=None, description="Col I")
    tests: set[PSEVTest] = Field(default_factory=set, description="Col J — 'Tests P/S/EV'")
    standpipe_diameter_mm: int | None = Field(default=None, description="Col K")
    plain_depth_m: float | None = Field(default=None, description="Col L")
    slotted_depth_m: float | None = Field(default=None, description="Col M")
    installation_complete: bool = Field(default=False, description="Col O — 'PIE/SP Complete'")


class Soakaway(_HoleBase):
    """Source sheet: 'Soakaway (BRE)'.

    Column E ('Completed') is a formula, ``=IF(I2>0, 1, 0)``, so it is derived
    from the recorded depth rather than stored here.
    """

    soakaway_id: str = Field(description="Col A — 'ID REF'")
    road: str | None = Field(default=None, description="Col B")
    schedule_depth_m: float = Field(gt=0, description="Col D")
    in_situ_tests: set[InSituTest] = Field(
        default_factory=set, description="Col F — 'Insitu Tests'"
    )
    width_m: float | None = Field(default=None, description="Col G (Excel header: 'Witdh')")
    length_m: float | None = Field(default=None, description="Col H")
    depth_m: float | None = Field(default=None, description="Col I")
    depth_of_hard_material_m: float | None = Field(default=None, description="Col J")


class DynamicProbe(_HoleBase):
    """Source sheet: 'DPH' (Dynamic Probe Heavy).

    Column H ('Completed') is a formula, ``=IF(C2>0,1,0)``, so it is derived
    by the engine from the depth rather than stored here.
    """

    probe_number: str = Field(description="Col A — 'DPH'")
    slope_over_20pct: bool = Field(default=False, description="Col B")
    depth_m: float = Field(gt=0, description="Col C")


class CPT(_HoleBase):
    """Source sheet: 'CPT' (Cone Penetration Test).

    Column K ('Completed') is a formula, ``=IF(D2>0,1,0)``, so it is derived
    by the engine from the depth rather than stored here.
    """

    cpt_number: str = Field(description="Col A — 'CPT'")
    slope_over_20pct: bool = Field(default=False, description="Col B")
    piezocone: bool = Field(default=False, description="Col C")
    depth_m: float = Field(gt=0, description="Col D")
