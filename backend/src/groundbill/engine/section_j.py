"""Section J — Installation monitoring and sampling.

Item codes, descriptions, units and sub-headings are copied from
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`, sheet 'Section J' (the issued
document). Quantities are translated from column D of
`reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section J'.

Every quantity cell in the Calculator (D10:D17, D19:D31, D33:D36) holds the
static text ``Not Required`` — there are no formulas in this section and
nothing is read from the Log Tracker.

Layout note
-----------
The workbook's section title (row 9) is "Installation monitoring and sampling
(during Fieldwork Period)", so items J1-J8 sit directly beneath the title with
no sub-heading row of their own. The "post Fieldwork Period" and "Surface
water body" groups each have a sub-heading row.

Descriptions are verbatim, including the workbook's own typos ("puriging" in
J5). J7 uses the Contractor workbook's wording; the Calculator has
"samplefrom" run together.
"""

from groundbill.models import Project

from .boq_items import BoqItem

_NOT_REQUIRED = "Not Required"


def compute_section_j(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section J BOQ items for the given project."""

    return [
        # 'Section J'!D10: Not Required
        BoqItem(
            code="J1",
            description=(
                "Reading of water level in standpipe or standpipe piezometer during "
                "fieldwork period"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D11: Not Required
        BoqItem(
            code="J2",
            description="Ground gas measurement in gas monitoring standpipe during fieldwork period",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D12: Not Required
        BoqItem(
            code="J3",
            description=(
                "Provide Engineer or Geologist to take inclinometer readings as "
                "directed by Investigation Supervisor (per installation)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D13: Not Required
        BoqItem(
            code="J4",
            description=(
                "Provide Engineer or Geologist to take measurement of slip indicator "
                "(per installation)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D14: Not Required
        BoqItem(
            code="J5",
            description=(
                "Provide Engineer/Geologist to take water sample from standpipe or "
                "standpipe piezometer (rate not including puriging or micro purging)"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D15: Not Required
        BoqItem(
            code="J6",
            description=(
                "Extra over Item J5 for purging or micro-purging in excess of 3 well " "volumes"
            ),
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D16: Not Required
        BoqItem(
            code="J7",
            description=(
                "Provide Engineer / Geologist to recover ground gas sample from gas "
                "monitoring standpipe"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D17: Not Required
        BoqItem(
            code="J8",
            description=(
                "Provide Engineer / Geologist to read free product level in standpipe"
                " using an interface probe"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D19: Not Required
        BoqItem(
            code="J9",
            description=(
                "Return visit to site following completion of fieldwork for field "
                "instrumentation"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Installation monitoring and sampling (post Fieldwork Period)",
        ),
        # 'Section J'!D20: Not Required
        BoqItem(
            code="J10",
            description=(
                "Extra over Item J9 for groundwater measurements in standpipe or "
                "standpipe piezometer during return visit"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D21: Not Required
        BoqItem(
            code="J11",
            description=(
                "Extra over Item J9 for ground gas measurements in standpipe during " "return visit"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D22: Not Required
        BoqItem(
            code="J12",
            description=(
                "Extra over Item J9 for set of inclinometer readings per installation"
                " during return visit and report results"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D23: Not Required
        BoqItem(
            code="J13",
            description=(
                "Extra over Item J9 to check for ground slippage in slip indicator "
                "installation during return visit to site"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D24: Not Required
        BoqItem(
            code="J14",
            description=(
                "Extra over Item J9 for water sample from standpipe or standpipe "
                "piezometer during return visit to site, including purging 3 volumes "
                "or micro-purging up to 3.0 hours"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D25: Not Required
        BoqItem(
            code="J15",
            description="Extra over Item J14 for purging or micro-purging in excess of 3.0 hours",
            unit="h",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D26: Not Required
        BoqItem(
            code="J16",
            description=(
                "Extra over Item J9 for ground gas sample from gas monitoring "
                "standpipe during return visit to site"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D27: Not Required
        BoqItem(
            code="J17",
            description=(
                "Extra over Item J9 for reading of free product level in standpipe "
                "using an interface probe during return visit to site"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D28: Not Required
        BoqItem(
            code="J18",
            description="Provision of equipment to facilitate measuring of free product in Item J17",
            unit="sum",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D29: Not Required
        BoqItem(
            code="J19",
            description=(
                "Provide and install data logger to measure groundwater levels in " "standpipes"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D30: Not Required
        BoqItem(
            code="J20",
            description="Provide baro logger to monitor air pressure for item J19",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D31: Not Required
        BoqItem(
            code="J21",
            description=(
                "Provide Engineer / Geologist to visit site to download and process "
                "data logger and baro logger"
            ),
            unit="day",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D33: Not Required
        BoqItem(
            code="J22",
            description="Surface water body sample taken during fieldwork period",
            unit="nr",
            quantity=_NOT_REQUIRED,
            subheading="Surface water body sampling and testing",
        ),
        # 'Section J'!D34: Not Required
        BoqItem(
            code="J23",
            description="Surface water body sample taken during return visit to site",
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D35: Not Required
        BoqItem(
            code="J24",
            description=(
                "Determination of dissolved oxygen, conductivity, pH and temperature "
                "of surface water body during fieldwork period"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
        # 'Section J'!D36: Not Required
        BoqItem(
            code="J25",
            description=(
                "Determination of dissolved oxygen, conductivity, pH and temperature "
                "of surface water body during return visit to site"
            ),
            unit="nr",
            quantity=_NOT_REQUIRED,
        ),
    ]
