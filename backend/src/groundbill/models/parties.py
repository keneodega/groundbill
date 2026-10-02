"""Contract parties — client, supervisor, and designer roles.

These names flow into the Specification's Introduction chapter ("1.1 Roles")
and into various clauses that reference the Employer or Investigation
Supervisor by name. All fields are optional so a part-filled project
still round-trips through validation; missing parties render as ``[TBC]``
in the generated specification.
"""

from pydantic import BaseModel, ConfigDict, Field


class ContractParties(BaseModel):
    """The organisations and individuals named in the contract."""

    model_config = ConfigDict(extra="forbid")

    employer_name: str | None = Field(
        default=None, description="The client letting the contract (the 'Employer')"
    )
    psdp_organisation: str | None = Field(
        default=None,
        description="Project Supervisor Design Process — under the Safety, Health "
        "and Welfare at Work Construction Regulations",
    )
    investigation_supervisor_organisation: str | None = Field(
        default=None, description="Organisation acting as Investigation Supervisor"
    )
    investigation_supervisor_name: str | None = Field(
        default=None, description="Named individual; often confirmed prior to start"
    )
    principal_designer: str | None = Field(
        default=None, description="CDM 2015 Principal Designer (UK projects)"
    )
    principal_contractor: str | None = Field(
        default=None, description="CDM 2015 Principal Contractor (UK projects)"
    )
