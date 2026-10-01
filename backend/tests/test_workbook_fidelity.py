"""Regression guard: engine output must match the reference workbook row for row.

For each re-translated section this reads the corresponding sheet of
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx` (the issued Contractor BOQ) and
asserts that the engine emits the same item codes, descriptions, units and
sub-headings, in the same order.

Sections are added to ``_VERIFIED_SECTIONS`` one at a time as each is
re-translated from the workbook.
"""

import re
from collections.abc import Callable
from pathlib import Path

import pytest
from openpyxl import load_workbook

from groundbill.engine import (
    BoqItem,
    compute_section_e,
    compute_section_f,
    compute_section_g,
    compute_section_j,
    compute_section_l,
)
from groundbill.models import ContractRoute, Project

_CONTRACTOR_BOQ = (
    Path(__file__).resolve().parents[2] / "reference" / "excel" / "4_BOQ_Contractor_Rev_A.xlsx"
)

# Row 9 of every sheet is the section title; item and sub-heading rows follow.
_FIRST_BODY_ROW = 10

_VERIFIED_SECTIONS: dict[str, Callable[[Project], list[BoqItem]]] = {
    "E": compute_section_e,
    "F": compute_section_f,
    "G": compute_section_g,
    "J": compute_section_j,
    "L": compute_section_l,
}


def _norm(value: object) -> str:
    """Collapse runs of whitespace and trim, so stray trailing spaces in cells don't matter."""
    return re.sub(r"\s+", " ", str(value if value is not None else "")).strip()


@pytest.fixture(scope="module")  # module scope: open the workbook once for all tests in this file
def contractor_boq():
    return load_workbook(_CONTRACTOR_BOQ)


def _workbook_rows(ws) -> list[tuple[str, str, str, str | None]]:
    """Return (code, description, unit, sub-heading above) for each item row of a sheet.

    An item row has a code in column A and a unit in column C. A sub-heading
    row has text in column B only; it is attached to the next item row.
    """
    rows: list[tuple[str, str, str, str | None]] = []
    pending_subheading: str | None = None
    for r in range(_FIRST_BODY_ROW, ws.max_row + 1):
        code, desc, unit = (_norm(ws.cell(r, c).value) for c in (1, 2, 3))
        if code and unit:
            rows.append((code, desc, unit, pending_subheading))
            pending_subheading = None
        elif desc and not code:
            if desc.lower().startswith("total "):
                break
            pending_subheading = desc
    return rows


@pytest.mark.parametrize("letter", sorted(_VERIFIED_SECTIONS))
def test_engine_matches_contractor_workbook(contractor_boq, letter: str):
    expected = _workbook_rows(contractor_boq[f"Section {letter}"])
    project = Project(name="Empty", site_address="Nowhere", contract_route=ContractRoute.PRIVATE)
    actual = [
        (i.code, _norm(i.description), _norm(i.unit), i.subheading)
        for i in _VERIFIED_SECTIONS[letter](project)
    ]
    assert actual == expected
