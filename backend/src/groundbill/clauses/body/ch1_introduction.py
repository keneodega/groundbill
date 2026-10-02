"""Chapter 1 — Introduction.

Mirrors Chapter 1 of Master Small GI Specification Rev C:
- Opening narrative (project description + reference to the standard spec)
- 1.1 Roles (PSDP, Employer, Investigation Supervisor)
- 1.2 Timescales (stub — populated once ContractDates lands)
- Anticipated Geology (Drift, Solid, Historical GI, Mining)

Source wording is translated verbatim where it is generic boilerplate;
project-specific phrases are replaced with named placeholders that
``SpecContext`` supplies.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..types import Clause, Paragraph, Run


def build_ch1_introduction(project: Project, ctx: SpecContext) -> Clause:
    """Return the Chapter 1 clause (heading + body + nested sub-sections)."""
    del project  # all variables come via ctx
    return Clause(
        number="1",
        heading="Introduction",
        level=1,
        body=[
            Paragraph(
                runs=[
                    Run(text=f"A ground investigation is proposed for {ctx.project_description}.")
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The following provides an overview of the ground "
                            "investigation proposal together with details of the "
                            "investigation requirements."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The Specification referred to in the Tender shall be "
                            f"{ctx.referenced_specification}."
                        )
                    )
                ]
            ),
        ],
        children=[
            _build_ch1_1_roles(ctx),
            _build_ch1_2_timescales(ctx),
            _build_ch1_3_anticipated_geology(ctx),
        ],
    )


def _build_ch1_1_roles(ctx: SpecContext) -> Clause:
    return Clause(
        number="1.1",
        heading="Roles",
        level=2,
        body=[
            Paragraph(runs=[Run(text="The following roles are applicable to this contract:")]),
            Paragraph(
                runs=[
                    Run(text="Project Supervisor Design Process (PSDP): ", bold=True),
                    Run(text=ctx.psdp_organisation),
                ],
                list_level=0,
            ),
            Paragraph(
                runs=[
                    Run(text="Employer: ", bold=True),
                    Run(text=ctx.employer_name),
                ],
                list_level=0,
            ),
            Paragraph(
                runs=[
                    Run(text="Investigation Supervisor: ", bold=True),
                    Run(text=ctx.investigation_supervisor_organisation),
                ],
                list_level=0,
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Details of the nominated Investigation Supervisor on behalf of "
                            f"{ctx.investigation_supervisor_organisation} shall be confirmed "
                            "prior to the commencement of the works."
                        )
                    )
                ]
            ),
        ],
    )


def _build_ch1_2_timescales(ctx: SpecContext) -> Clause:
    """Placeholder until the ContractDates sub-model lands (planned for Phase 5)."""
    del ctx
    return Clause(
        number="1.2",
        heading="Timescales",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Tender return date, contract start date, and report delivery "
                            "requirements shall be confirmed in the contract documents."
                        )
                    )
                ]
            )
        ],
    )


def _build_ch1_3_anticipated_geology(ctx: SpecContext) -> Clause:
    return Clause(
        number="1.3",
        heading="Anticipated Geology",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The following summary of anticipated ground conditions is based "
                            "on published information. No assurance is given to its accuracy."
                        )
                    )
                ]
            )
        ],
        children=[
            _geology_subsection("1.3.1", "Drift Geology", ctx.drift_geology),
            _geology_subsection("1.3.2", "Solid Geology", ctx.solid_geology),
            _geology_subsection(
                "1.3.3",
                "Historical Ground Investigation Information",
                ctx.historical_gi_information,
            ),
            _geology_subsection("1.3.4", "Mining Information", ctx.mining_information),
        ],
    )


def _geology_subsection(number: str, heading: str, body_text: str) -> Clause:
    return Clause(
        number=number,
        heading=heading,
        level=3,
        body=[Paragraph(runs=[Run(text=body_text)])],
    )
