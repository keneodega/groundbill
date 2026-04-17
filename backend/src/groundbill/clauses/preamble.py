"""Preamble clauses — everything before Schedule 1 starts.

Phase 1 is a stub producing one paragraph. The real preamble (introduction,
definitions, references to the Contractor's obligations, legal scope) will
be translated from the source ``.docm`` in Phase 3.
"""

from groundbill.models import Project

from .context import SpecContext
from .types import Clause, Paragraph, Run


def build_preamble(project: Project, ctx: SpecContext) -> list[Clause]:
    """Return the ordered list of preamble clauses."""
    del project  # unused in the stub; accepted so the signature matches other builders
    return [
        Clause(
            number="",
            heading="Preamble",
            level=1,
            body=[
                Paragraph(
                    runs=[
                        Run(
                            text=(
                                f"This specification governs the ground investigation for "
                                f"{ctx.project_name} at {ctx.site_address}."
                            )
                        )
                    ]
                )
            ],
        )
    ]
