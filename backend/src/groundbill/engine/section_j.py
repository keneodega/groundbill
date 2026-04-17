"""Section J — Installation Monitoring.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section J'.

All 25 items are "Not Required" — this is an entirely static section with no
computed quantities.
"""

from groundbill.models import Project

from .boq_items import BoqItem


def compute_section_j(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section J BOQ items for the given project."""

    return [
        BoqItem(
            code="J1",
            description="Groundwater level monitoring — standpipe piezometer (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J2",
            description="Groundwater level monitoring — standpipe piezometer (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J3",
            description="Groundwater level monitoring — vibrating wire piezometer (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J4",
            description="Groundwater level monitoring — vibrating wire piezometer (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J5",
            description="Ground gas monitoring (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J6",
            description="Ground gas monitoring (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J7",
            description="Inclinometer reading (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J8",
            description="Inclinometer reading (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J9",
            description="Extensometer reading (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J10",
            description="Extensometer reading (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J11",
            description="Settlement gauge reading (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J12",
            description="Settlement gauge reading (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J13",
            description="Datalogger download (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J14",
            description="Datalogger download (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J15",
            description="Groundwater sampling (first visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J16",
            description="Groundwater sampling (subsequent visit)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J17",
            description="Surface water sampling",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J18",
            description="Leachate sampling",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J19",
            description="Installation decommissioning — borehole standpipe or piezometer",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J20",
            description="Installation decommissioning — dynamic sample standpipe",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J21",
            description="Installation decommissioning — inclinometer",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J22",
            description="Monitoring report — factual",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J23",
            description="Monitoring report — interpretive",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="J24",
            description="Monitoring — standing time",
            unit="h",
            quantity="Not Required",
        ),
        BoqItem(
            code="J25",
            description="Additional monitoring (to be specified)",
            unit="nr",
            quantity="Not Required",
        ),
    ]
