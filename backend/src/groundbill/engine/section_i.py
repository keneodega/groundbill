"""Section I — Instrumentation.

Translated from `reference/excel/2_BOQ_Calculator_Rev_A.xlsx`, sheet 'Section I'
(with cross-references to the Log Tracker workbook's `Boreholes` and
`Dynamic Sampling` sheets).

Key formulas
============
I1   = count of BHs with piezometer_type=PIEZOMETER and installation_complete
I2   = count of BHs with piezometer_type=STANDPIPE and installation_complete
I3   = sum of piezometer_plain_depth_m for piezometer BHs
I4   = sum of standpipe_plain_depth_m for standpipe BHs
I5   = sum of standpipe_slotted_depth_m for standpipe BHs
I6   = count of standpipe BHs with standpipe_diameter_mm == 50
I7   = count of standpipe BHs with standpipe_diameter_mm == 19
I8   = I1 + I2 (end caps — one per installation)
I9   = count of installed BHs (piezo or standpipe) where road == "RURAL"
I10  = count of installed BHs (piezo or standpipe) where road is None
I11  = count of DSs with installation_complete and plain_depth_m > 0
I12  = sum of plain_depth_m for installed DSs
I13  = sum of slotted_depth_m for installed DSs
I14  = count of installed DSs with standpipe_diameter_mm == 50
I15  = count of installed DSs with standpipe_diameter_mm == 19
I16  = I11 (end caps)
I17  = count of installed DSs where road == "RURAL"
I18  = count of installed DSs where road is None

Static items: I19–I35 — "Not Required".
"""

from groundbill.models import PiezometerType, Project

from .boq_items import BoqItem


def compute_section_i(project: Project) -> list[BoqItem]:
    """Return the ordered list of Section I BOQ items for the given project."""

    # Borehole instrumentation
    piezo_bhs = [
        bh
        for bh in project.boreholes
        if bh.piezometer_type == PiezometerType.PIEZOMETER and bh.installation_complete
    ]
    standpipe_bhs = [
        bh
        for bh in project.boreholes
        if bh.piezometer_type == PiezometerType.STANDPIPE and bh.installation_complete
    ]
    installed_bhs = piezo_bhs + standpipe_bhs

    i1 = len(piezo_bhs)
    i2 = len(standpipe_bhs)
    i3 = sum(bh.piezometer_plain_depth_m or 0.0 for bh in piezo_bhs)
    i4 = sum(bh.standpipe_plain_depth_m or 0.0 for bh in standpipe_bhs)
    i5 = sum(bh.standpipe_slotted_depth_m or 0.0 for bh in standpipe_bhs)
    i6 = sum(1 for bh in standpipe_bhs if bh.standpipe_diameter_mm == 50)
    i7 = sum(1 for bh in standpipe_bhs if bh.standpipe_diameter_mm == 19)
    i8 = i1 + i2
    i9 = sum(1 for bh in installed_bhs if bh.road == "RURAL")
    i10 = sum(1 for bh in installed_bhs if bh.road is None)

    # Dynamic sample instrumentation
    installed_ds = [
        ds
        for ds in project.dynamic_samples
        if ds.installation_complete and (ds.plain_depth_m or 0.0) > 0
    ]

    i11 = len(installed_ds)
    i12 = sum(ds.plain_depth_m or 0.0 for ds in installed_ds)
    i13 = sum(ds.slotted_depth_m or 0.0 for ds in installed_ds)
    i14 = sum(1 for ds in installed_ds if ds.standpipe_diameter_mm == 50)
    i15 = sum(1 for ds in installed_ds if ds.standpipe_diameter_mm == 19)
    i16 = i11
    i17 = sum(1 for ds in installed_ds if ds.road == "RURAL")
    i18 = sum(1 for ds in installed_ds if ds.road is None)

    return [
        BoqItem(
            code="I1",
            description="Install piezometer in borehole",
            unit="nr",
            quantity=i1,
        ),
        BoqItem(
            code="I2",
            description="Install standpipe in borehole",
            unit="nr",
            quantity=i2,
        ),
        BoqItem(
            code="I3",
            description="Piezometer plain pipe",
            unit="m",
            quantity=i3,
        ),
        BoqItem(
            code="I4",
            description="Standpipe plain pipe",
            unit="m",
            quantity=i4,
        ),
        BoqItem(
            code="I5",
            description="Standpipe slotted pipe",
            unit="m",
            quantity=i5,
        ),
        BoqItem(
            code="I6",
            description="Standpipe diameter 50 mm",
            unit="nr",
            quantity=i6,
        ),
        BoqItem(
            code="I7",
            description="Standpipe diameter 19 mm",
            unit="nr",
            quantity=i7,
        ),
        BoqItem(
            code="I8",
            description="End caps for piezometer or standpipe installation",
            unit="nr",
            quantity=i8,
        ),
        BoqItem(
            code="I9",
            description="Flush cover (rural road)",
            unit="nr",
            quantity=i9,
        ),
        BoqItem(
            code="I10",
            description="Raised cover (non-road location)",
            unit="nr",
            quantity=i10,
        ),
        BoqItem(
            code="I11",
            description="Install standpipe in dynamic sample hole",
            unit="nr",
            quantity=i11,
        ),
        BoqItem(
            code="I12",
            description="Dynamic sample standpipe plain pipe",
            unit="m",
            quantity=i12,
        ),
        BoqItem(
            code="I13",
            description="Dynamic sample standpipe slotted pipe",
            unit="m",
            quantity=i13,
        ),
        BoqItem(
            code="I14",
            description="Dynamic sample standpipe diameter 50 mm",
            unit="nr",
            quantity=i14,
        ),
        BoqItem(
            code="I15",
            description="Dynamic sample standpipe diameter 19 mm",
            unit="nr",
            quantity=i15,
        ),
        BoqItem(
            code="I16",
            description="End caps for dynamic sample standpipe installation",
            unit="nr",
            quantity=i16,
        ),
        BoqItem(
            code="I17",
            description="Dynamic sample flush cover (rural road)",
            unit="nr",
            quantity=i17,
        ),
        BoqItem(
            code="I18",
            description="Dynamic sample raised cover (non-road location)",
            unit="nr",
            quantity=i18,
        ),
        BoqItem(
            code="I19",
            description="Backfill annulus with cement/bentonite grout",
            unit="m³",
            quantity="Not Required",
        ),
        BoqItem(
            code="I20",
            description="Bentonite seal",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I21",
            description="Sand/gravel filter pack",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="I22",
            description="Response zone — sand",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="I23",
            description="Gas tap installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I24",
            description="Inclinometer casing",
            unit="m",
            quantity="Not Required",
        ),
        BoqItem(
            code="I25",
            description="Vibrating wire piezometer installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I26",
            description="Settlement gauge installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I27",
            description="Extensometer installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I28",
            description="Magnetic extensometer installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I29",
            description="Slip indicator installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I30",
            description="Pneumatic piezometer installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I31",
            description="Datalogger installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I32",
            description="Telemetry installation",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I33",
            description="Protective cover (heavy duty)",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I34",
            description="Protective bollards",
            unit="nr",
            quantity="Not Required",
        ),
        BoqItem(
            code="I35",
            description="Additional instrumentation (to be specified)",
            unit="nr",
            quantity="Not Required",
        ),
    ]
