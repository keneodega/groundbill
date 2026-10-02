"""Anticipated geology — desk-study summary of ground conditions.

These narrative paragraphs are reproduced verbatim in the Specification's
Introduction chapter under "Anticipated Geology". Each field is a free-text
paragraph typically derived from GSI/BGS published mapping plus any
available historical ground investigation information.
"""

from pydantic import BaseModel, ConfigDict, Field


class AnticipatedGeology(BaseModel):
    """Narrative summary of expected ground conditions for the site."""

    model_config = ConfigDict(extra="forbid")

    drift_geology: str | None = Field(
        default=None, description="Superficial/Quaternary deposits expected at the site"
    )
    solid_geology: str | None = Field(
        default=None, description="Bedrock expected beneath the drift"
    )
    historical_gi_information: str | None = Field(
        default=None, description="Summary of any previous ground investigations in the vicinity"
    )
    mining_information: str | None = Field(
        default=None, description="Known or suspected mine workings / extraction"
    )
