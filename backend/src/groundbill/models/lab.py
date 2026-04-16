"""Laboratory test schedule models.

Source: 'Lab Schedules' sheet in `reference/excel/1_BOQ_Log_Rev_A.xlsx`.
Row 3 is the header; rows 4+ list one lab test per row with quantity and
sample-source percentages.
"""

from pydantic import BaseModel, ConfigDict, Field


class LabTestAllocation(BaseModel):
    """One row of the lab schedule — one test and its scheduled quantity."""

    model_config = ConfigDict(extra="forbid")

    test_name: str = Field(description="Col A — 'TEST'")
    quantity: int = Field(
        ge=0, description="Col B — scheduled test count (Excel header 'Quantaty' is a typo)"
    )
    pct_from_trial_pits: float | None = Field(
        default=None, ge=0, le=1, description="Col J — '% of TP'"
    )
    pct_from_boreholes: float | None = Field(
        default=None, ge=0, le=1, description="Col K — '% of BH'"
    )


class LabSchedule(BaseModel):
    """The project's full lab schedule as a collection of allocations."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, description="Schedule identifier (row 1 'Name')")
    allocations: list[LabTestAllocation] = Field(default_factory=list)
