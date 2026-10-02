"""Pre-computed values for specification clauses.

``SpecContext`` is built once from a ``Project`` at the start of generation
and then passed to every clause builder. This keeps each builder short
(no re-deriving ``len(project.boreholes)`` in 12 places) and gives all
clauses a single consistent source for labels like the site-category name.

Missing project fields render as ``TBC_MARKER`` (``"[TBC]"``) rather than
raising. A half-filled project therefore still produces a valid draft
that the consultant can fill in later in Word.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict

from groundbill.models import ContractRoute, DrillingMethod, Project, SiteCategory

TBC_MARKER = "[TBC]"

_CATEGORY_LABEL: dict[SiteCategory, str] = {
    SiteCategory.GREEN: "Green",
    SiteCategory.YELLOW: "Yellow",
    SiteCategory.RED: "Red",
}

_ROUTE_LABEL: dict[ContractRoute, str] = {
    ContractRoute.PRIVATE: "Private (bespoke)",
    ContractRoute.PW_CF: "Public Works Contract (PW-CF)",
}

_ROTARY_METHODS = {
    DrillingMethod.ROTARY_CORE_HARD,
    DrillingMethod.ROTARY_NO_CORE_HARD,
    DrillingMethod.ROTARY_CORE_SOFT,
    DrillingMethod.ROTARY_NO_CORE_SOFT,
}

# The Specification referenced by the tender — a constant for private/UK
# small-GI work using the Engineers Ireland template family.
_REFERENCED_SPECIFICATION = "Engineers Ireland\u2019s \u2018Specification and Related Documents for Ground Investigations\u2019"


def _or_tbc(value: str | None) -> str:
    """Return value if set, else the TBC placeholder."""
    return value if value else TBC_MARKER


class SpecContext(BaseModel):
    """Immutable pre-computed context for every clause builder.

    ``frozen=True`` means the context cannot be mutated after construction —
    a safety net against a clause builder accidentally writing back into
    the shared context.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Cover page / preamble
    project_name: str
    site_address: str
    site_category_label: str
    contract_route_label: str
    today: date

    # Introduction narrative
    project_description: str
    referenced_specification: str
    location_drawing_reference: str

    # Parties (Chapter 1.1 Roles)
    employer_name: str
    psdp_organisation: str
    investigation_supervisor_organisation: str
    investigation_supervisor_name: str

    # Anticipated geology (Chapter 1 Anticipated Geology)
    drift_geology: str
    solid_geology: str
    historical_gi_information: str
    mining_information: str

    # Hole tallies (used across Chapters 2-4)
    borehole_count: int
    trial_pit_count: int
    trench_count: int
    inspection_pit_count: int
    dynamic_sample_count: int
    soakaway_count: int
    dynamic_probe_count: int
    cpt_count: int

    # Method presence + scope flags (Chapter 3 drives conditional inclusion)
    has_cable_percussion: bool
    has_rotary: bool
    has_hard_standing: bool
    rotary_borehole_count: int

    # Maximum scheduled depths per hole type — used to describe scope in
    # the body text (e.g. "trial pits to a scheduled depth of X m").
    # None when the project has none of that hole type.
    max_trial_pit_depth_m: float | None
    max_trench_depth_m: float | None
    max_dynamic_probe_depth_m: float | None

    @classmethod
    def from_project(cls, project: Project, today: date | None = None) -> SpecContext:
        """Build a SpecContext from a Project. ``today`` is injectable for tests."""
        parties = project.parties
        geology = project.anticipated_geology
        return cls(
            project_name=project.name,
            site_address=project.site_address,
            site_category_label=_CATEGORY_LABEL[project.site_category],
            contract_route_label=_ROUTE_LABEL[project.contract_route],
            today=today if today is not None else date.today(),
            project_description=_or_tbc(project.project_description),
            referenced_specification=_REFERENCED_SPECIFICATION,
            location_drawing_reference=_or_tbc(project.location_drawing_reference),
            employer_name=_or_tbc(parties.employer_name),
            psdp_organisation=_or_tbc(parties.psdp_organisation),
            investigation_supervisor_organisation=_or_tbc(
                parties.investigation_supervisor_organisation
            ),
            investigation_supervisor_name=_or_tbc(parties.investigation_supervisor_name),
            drift_geology=_or_tbc(geology.drift_geology),
            solid_geology=_or_tbc(geology.solid_geology),
            historical_gi_information=_or_tbc(geology.historical_gi_information),
            mining_information=_or_tbc(geology.mining_information),
            borehole_count=len(project.boreholes),
            trial_pit_count=len(project.trial_pits),
            trench_count=len(project.trenches),
            inspection_pit_count=len(project.inspection_pits),
            dynamic_sample_count=len(project.dynamic_samples),
            soakaway_count=len(project.soakaways),
            dynamic_probe_count=len(project.dynamic_probes),
            cpt_count=len(project.cpts),
            has_cable_percussion=_has_method(project, {DrillingMethod.CABLE_PERCUSSION}),
            has_rotary=_has_method(project, _ROTARY_METHODS),
            has_hard_standing=(
                any(tp.paved for tp in project.trial_pits)
                or any(tr.paved for tr in project.trenches)
            ),
            rotary_borehole_count=sum(
                1
                for bh in project.boreholes
                if any(phase.method in _ROTARY_METHODS for phase in bh.phases)
            ),
            max_trial_pit_depth_m=(
                max((tp.schedule_depth_m for tp in project.trial_pits), default=None)
            ),
            max_trench_depth_m=(
                max(
                    (
                        tr.overall_total_depth_m
                        for tr in project.trenches
                        if tr.overall_total_depth_m is not None
                    ),
                    default=None,
                )
            ),
            max_dynamic_probe_depth_m=(
                max((dp.depth_m for dp in project.dynamic_probes), default=None)
            ),
        )


def _has_method(project: Project, methods: set[DrillingMethod]) -> bool:
    return any(phase.method in methods for bh in project.boreholes for phase in bh.phases)
