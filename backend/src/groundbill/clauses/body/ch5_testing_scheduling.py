"""Chapter 5 — Testing Scheduling.

Rev C's source chapter is a single paragraph about the 24-hour turnaround
for driller's logs and testing schedules. We additionally render the
project's lab_schedule as a table here — it's the natural home for the
list of anticipated tests and their quantities.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..types import Clause, Paragraph, Run, Table


def build_ch5_testing_scheduling(project: Project, ctx: SpecContext) -> Clause:
    """Return the Chapter 5 clause. Includes the lab-schedule table when one
    has been defined on the project."""
    del ctx

    body: list = [
        Paragraph(
            runs=[
                Run(
                    text=(
                        "Blank laboratory testing schedules and the driller's logs shall "
                        "be provided to the Designer within 24 hours following completion "
                        "of each exploratory hole."
                    )
                )
            ]
        )
    ]

    allocations = project.lab_schedule.allocations
    if allocations:
        body.append(
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The anticipated laboratory testing schedule is set out below. "
                            "Quantities may be adjusted by the Investigation Supervisor as "
                            "the fieldworks progress."
                        )
                    )
                ]
            )
        )
        rows = [[alloc.test_name, str(alloc.quantity)] for alloc in allocations]
        body.append(Table(headers=["Test", "Scheduled Quantity"], rows=rows))
    else:
        body.append(
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The detailed laboratory testing schedule shall be confirmed "
                            "following recovery of samples from the fieldworks."
                        )
                    )
                ]
            )
        )

    return Clause(number="5", heading="Testing Scheduling", level=1, body=body)
