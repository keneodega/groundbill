"""Chapter 4 — Laboratory Testing.

Mirrors Rev C Chapter "Laboratory Testing", which has two sub-sections:
- 4.1 Geotechnical Laboratory Testing (Soil): narrative with a bulleted
  indicative scope and a closing note about additions.
- 4.2 Chemical Testing (Soil): short narrative; the actual schedule of
  scheduled tests lives in Chapter 5 (Testing Scheduling) where the
  lab_schedule table is rendered.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..types import Clause, Paragraph, Run


def build_ch4_lab_testing(project: Project, ctx: SpecContext) -> Clause:
    """Return the Chapter 4 clause with its two sub-sections."""
    del project, ctx
    return Clause(
        number="4",
        heading="Laboratory Testing",
        level=1,
        children=[
            _build_ch4_1_geotechnical(),
            _build_ch4_2_chemical(),
        ],
    )


def _build_ch4_1_geotechnical() -> Clause:
    return Clause(
        number="4.1",
        heading="Geotechnical Laboratory Testing (Soil)",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The extent of geotechnical laboratory soil testing is "
                            "anticipated to comprise, but not limited to, the following:"
                        )
                    )
                ]
            ),
            Paragraph(runs=[Run(text="Soil Classification Tests")], list_level=0),
            Paragraph(runs=[Run(text="Soil Strength Tests")], list_level=0),
            Paragraph(runs=[Run(text="Chemical Tests")], list_level=0),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Additional geotechnical tests (both type and quantity) may be "
                            "required depending on the samples recovered and ground "
                            "conditions encountered."
                        )
                    )
                ]
            ),
        ],
    )


def _build_ch4_2_chemical() -> Clause:
    return Clause(
        number="4.2",
        heading="Chemical Testing (Soil)",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Chemical testing requirements shall be confirmed against the "
                            "samples recovered and any contamination encountered during "
                            "the fieldworks. The scheduled laboratory testing schedule is "
                            "set out in Chapter 5."
                        )
                    )
                ]
            )
        ],
    )
