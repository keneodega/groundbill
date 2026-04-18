"""Chapter 6 — Reporting.

Transcribed from Rev C's "Reporting" chapter. Covers driller's logs
turnaround, the Factual and Interpretive reports (both referencing the
Engineers Ireland standard specification), and digital deliverables
including AGS 4.0 transfer format.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..types import Clause, Paragraph, Run


def build_ch6_reporting(project: Project, ctx: SpecContext) -> Clause:
    """Return the Chapter 6 clause."""
    del project
    referenced_spec = ctx.referenced_specification
    return Clause(
        number="6",
        heading="Reporting",
        level=1,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Typed Engineer's logs are to be submitted to the Engineer's "
                            "Representative within one week of completion of each "
                            "exploratory hole."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "A standard Factual Report is required and shall be produced "
                            f"in accordance with {referenced_spec}."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "A standard Interpretive Report is required and shall be "
                            f"produced in accordance with {referenced_spec}."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "All contamination testing results must be presented in both "
                            "PDF and Excel format. AGS data 4.0 shall be provided for the "
                            "ground investigation, both in draft format whilst laboratory "
                            "testing is underway and as a final version upon completion "
                            "of the project."
                        )
                    )
                ]
            ),
        ],
    )
