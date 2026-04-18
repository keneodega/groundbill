"""Chapter 7 — Further Information.

Closing chapter covering services, H&S, security, traffic management,
and access. Transcribed from Rev C with project-specific wording
generalised (Rev C's "people working on the port" referred to a Dublin
Port project — generalised here to "people working at or passing the
site"). Dated COVID-19 references from the 2019 source have been
dropped; the general H&S compliance framing remains.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..types import Clause, Paragraph, Run


def build_ch7_further_information(project: Project, ctx: SpecContext) -> Clause:
    """Return the Chapter 7 clause with its five sub-sections."""
    del project, ctx
    return Clause(
        number="7",
        heading="Further Information",
        level=1,
        children=[
            _build_ch7_1_services(),
            _build_ch7_2_health_safety(),
            _build_ch7_3_security(),
            _build_ch7_4_traffic_management(),
            _build_ch7_5_access(),
        ],
    )


def _build_ch7_1_services() -> Clause:
    return Clause(
        number="7.1",
        heading="Services Information",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The GI Contractor shall contact the relevant utility providers "
                            "and comply with their requirements with respect to excavations "
                            "in the vicinity of their services. It is the responsibility of "
                            "the GI Contractor to ensure that all services have been cleared "
                            "and are not damaged as a result of the fieldworks."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The Contractor is to satisfy himself that the risk from buried "
                            "services and overhead cables has been mitigated through, but "
                            "not limited to: ascertaining the location of the services at "
                            "the site, use of cable-avoidance equipment, risk assessments "
                            "and any other means to mitigate potential risks."
                        )
                    )
                ]
            ),
        ],
    )


def _build_ch7_2_health_safety() -> Clause:
    return Clause(
        number="7.2",
        heading="Health and Safety Requirements",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The Safety, Health and Welfare at Work (Construction) "
                            "Regulations 2013 (and SI 291 of 2013) are applicable to "
                            "this contract."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Prior to the start of site operations, the Contractor shall "
                            "provide risk assessments and method statements covering all "
                            "aspects of the work to be carried out; these shall form part "
                            "of the Construction Phase Health and Safety Plan produced by "
                            "the Project Supervisor Construction Stage (PSCS) and "
                            "submitted to the Investigation Supervisor."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Current public-health guidance issued by the HSE and HSA "
                            "applicable to construction activities shall be followed at "
                            "all times. Appropriate personal protective equipment shall "
                            "be provided to the Investigation Supervisor where required."
                        )
                    )
                ]
            ),
        ],
    )


def _build_ch7_3_security() -> Clause:
    return Clause(
        number="7.3",
        heading="Security of the Site",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The GI Contractor shall erect a compound (welfare, offices, "
                            "storage etc. as required for their operations) at their own "
                            "cost. The GI Contractor shall liaise with the Employer to "
                            "agree a suitable location if one is deemed to be required."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The GI Contractor shall ensure that the general public and "
                            "people working at or passing the site are protected at all "
                            "times while plant and equipment are mobilised, in use at, "
                            "and demobilised to/from each exploratory location."
                        )
                    )
                ]
            ),
        ],
    )


def _build_ch7_4_traffic_management() -> Clause:
    return Clause(
        number="7.4",
        heading="Traffic Management Measures",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "The GI Contractor must satisfy themselves of the need for any "
                            "traffic management measures required in order to safely "
                            "access the site. Should a need for such measures be "
                            "identified, this should be raised at an early stage to allow "
                            "timely discussions with the site owner."
                        )
                    )
                ]
            )
        ],
    )


def _build_ch7_5_access() -> Clause:
    return Clause(
        number="7.5",
        heading="Access to Site",
        level=2,
        body=[
            Paragraph(runs=[Run(text="Access arrangements are to be confirmed by the Employer.")])
        ],
    )
