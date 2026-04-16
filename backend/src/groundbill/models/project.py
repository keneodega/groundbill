"""The top-level Project model — single source of truth for one GI pack.

All three deliverables (BOQ, Schedule 2, Specification) are derived from one
instance of ``Project``. Internal consistency across outputs is guaranteed by
computing every line item from this shared object.
"""

from pydantic import BaseModel, ConfigDict, Field

from .enums import ContractRoute, SiteCategory
from .holes import (
    CPT,
    Borehole,
    DynamicProbe,
    DynamicSample,
    InspectionPit,
    Soakaway,
    Trench,
    TrialPit,
)
from .lab import LabSchedule


class Project(BaseModel):
    """One GI investigation as defined by the consultant."""

    model_config = ConfigDict(extra="forbid")

    name: str
    site_address: str
    contract_route: ContractRoute
    site_category: SiteCategory = SiteCategory.GREEN

    boreholes: list[Borehole] = Field(default_factory=list)
    trial_pits: list[TrialPit] = Field(default_factory=list)
    trenches: list[Trench] = Field(default_factory=list)
    inspection_pits: list[InspectionPit] = Field(default_factory=list)
    dynamic_samples: list[DynamicSample] = Field(default_factory=list)
    soakaways: list[Soakaway] = Field(default_factory=list)
    dynamic_probes: list[DynamicProbe] = Field(default_factory=list)
    cpts: list[CPT] = Field(default_factory=list)
    lab_schedule: LabSchedule = Field(default_factory=LabSchedule)
