"""Enumerations for the GroundBill domain model.

All enums trace to columns or lookup tabs in the Log Tracker workbook
(`reference/excel/1_BOQ_Log_Rev_A.xlsx`).
"""

from enum import StrEnum


class ContractRoute(StrEnum):
    """The contract mechanism under which the investigation is being let."""

    PRIVATE = "private"
    PW_CF = "pw_cf"


class SiteCategory(StrEnum):
    """Site risk / complexity banding used to scope provisional items."""

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class DrillingMethod(StrEnum):
    """Drilling method used for one phase of a borehole.

    Source: 'Boreholes' sheet column groups — one column band per method.
    A single borehole may combine multiple phases (for example, cable
    percussion down to the rockhead followed by rotary coring into rock).
    """

    CABLE_PERCUSSION = "CP"
    ROTARY_CORE_HARD = "RC_CORE_HARD"
    ROTARY_NO_CORE_HARD = "RC_NO_CORE_HARD"
    ROTARY_CORE_SOFT = "RC_CORE_SOFT"
    ROTARY_NO_CORE_SOFT = "RC_NO_CORE_SOFT"


class InSituTest(StrEnum):
    """In-situ tests offered on trial pits, inspection pits, soakaways, and similar.

    Source: 'TESTS' sheet in the Log Tracker. The sheet itself lists 32 pre-built
    combinations (rows 4-34); those combinations are the Cartesian product of the
    five codes below. In Python we represent a hole's test selection as a
    ``set[InSituTest]`` and derive the combination label on the fly.
    """

    DCP = "DCP"
    HV = "HV"
    BRE = "BRE"
    PT = "PT"
    EV = "EV"


class PSEVTest(StrEnum):
    """'Tests P/S/EV' column on boreholes and dynamic samples.

    These are sampling / installation selections rather than in-situ tests,
    retained under the Excel column's own label for traceability:

    - ``P`` — Piezometer
    - ``S`` — Standpipe
    - ``EV`` — Environmental Sampling
    """

    P = "P"
    S = "S"
    EV = "EV"


class PiezometerType(StrEnum):
    """Borehole instrumentation type recorded in the Log Tracker."""

    NONE = "none"
    PIEZOMETER = "piezometer"
    STANDPIPE = "standpipe"
