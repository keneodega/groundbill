"""Chapter 2 — Ground Investigation Schedule.

Contains the commentary introducing the proposed exploratory-hole schedule
and the holes table itself. Mirrors Master Small GI Specification Rev C's
"Ground Investigation Schedule" chapter.

The actual row-building lives in ``clauses/schedule_2.py`` so the eventual
standalone Schedule 2 ``.xlsx`` generator can reuse the same logic.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..schedule_2 import build_holes_table
from ..types import Clause, Paragraph, Run


def build_ch2_gi_schedule(project: Project, ctx: SpecContext) -> Clause:
    """Return the Chapter 2 clause (commentary + holes table + key)."""
    body: list = [
        Paragraph(
            runs=[
                Run(
                    text=(
                        "The schedule of the proposed ground investigation is presented "
                        "in the table below."
                    )
                )
            ]
        ),
        Paragraph(
            runs=[
                Run(
                    text=(
                        "The boreholes, dynamic probes and trial pits are proposed to "
                        "determine the geology, groundwater and underlying bedrock "
                        "conditions at the site."
                    )
                )
            ]
        ),
    ]

    if project.trenches:
        body.append(
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The slit trenches are proposed to locate and identify "
                            "underground services and perform soil sampling for "
                            "geotechnical and environmental testing."
                        )
                    )
                ]
            )
        )

    body.append(build_holes_table(project))

    body.append(
        Paragraph(
            runs=[
                Run(
                    text=(
                        "The proposed exploratory locations are shown on drawing number "
                        f"{ctx.location_drawing_reference}. Final locations are to be agreed "
                        "on site with the Investigation Supervisor."
                    )
                )
            ]
        )
    )

    body.append(
        Paragraph(runs=[Run(text="Abbreviations: CP — Cable Percussion; RC — Rotary Coring.")])
    )

    return Clause(
        number="2",
        heading="Ground Investigation Schedule",
        level=1,
        body=body,
    )
