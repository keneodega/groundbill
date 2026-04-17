"""Section G — Geophysical Testing.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section G'.

All 10 items are "Not Required" — this is an entirely static section with no
computed quantities.
"""

from groundbill.models import Project

from .boq_items import BoqItem


def compute_section_g(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section G BOQ items for the given project."""

    return [
        BoqItem(
            code="G1",
            description="Mobilise geophysical survey equipment to site",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="G2",
            description="Ground penetrating radar (GPR) survey",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="G3",
            description="Electromagnetic (EM) conductivity survey",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="G4",
            description="Resistivity survey (electrical resistivity tomography)",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="G5",
            description="Seismic refraction survey",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="G6",
            description="Seismic reflection survey",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="G7",
            description="Multi-channel analysis of surface waves (MASW)",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="G8",
            description="Microgravity survey",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="G9",
            description="Magnetometer survey",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="G10",
            description="Factual and interpretive geophysical report",
            unit="nr",
            quantity="Not Required",
        ),
    ]
