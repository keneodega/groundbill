"""BOQ .xlsx generator.

Produces a Bill of Quantities workbook whose layout matches
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`:

- One worksheet per BOQ section (Section A, Section B, ...).
- Within each sheet, data starts at row 7 (header row).
- Row 8 holds the currency markers (€ in cols E and F).
- Row 9 is the section heading (code and title, bold).
- Row 10 onwards is one BOQ item per row across columns A-F:
  A=Number, B=Item description, C=Unit, D=Quantity, E=Rate, F=Amount.

The Amount cell is written as ``=IFERROR(D*E, "")`` so it resolves to the
priced total once the contractor fills in the Rate column, and stays blank
otherwise.

Sections A and B are implemented; sections C-L will be added as each is
translated in the calculation engine.
"""

from collections.abc import Callable
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from groundbill.engine import (
    BoqItem,
    compute_section_a,
    compute_section_b,
    compute_section_c,
    compute_section_d,
    compute_section_e,
    compute_section_f,
    compute_section_g,
    compute_section_h,
    compute_section_i,
    compute_section_j,
    compute_section_k,
    compute_section_l,
)
from groundbill.models import Project

_HEADER_ROW = 7
_CURRENCY_ROW = 8
_SECTION_HEADING_ROW = 9
_FIRST_ITEM_ROW = 10

_COLUMN_WIDTHS = {
    "A": 9.2,
    "B": 35.8,
    "C": 10.2,
    "D": 11.5,
    "E": 11.5,
    "F": 11.5,
}

_BOLD = Font(bold=True)

_HEADERS = ("Number", "Item description", "Unit", "Quantity", "Rate", "Amount")

_SECTIONS: list[tuple[str, str, str, Callable[[Project], list[BoqItem]]]] = [
    (
        "Section A",
        "A",
        "General items, provisional services and additional items",
        compute_section_a,
    ),
    (
        "Section B",
        "B",
        (
            "Cable Percussion Boring (cable tool or percussive boring using "
            "minimum of 200mm diameter casing)"
        ),
        compute_section_b,
    ),
    (
        "Section C",
        "C",
        "Rotary Drilling",
        compute_section_c,
    ),
    (
        "Section D",
        "D",
        "Pitting and Trenching",
        compute_section_d,
    ),
    (
        "Section E",
        "E",
        "Sampling and Monitoring",
        compute_section_e,
    ),
    (
        "Section F",
        "F",
        "Probing and Cone Penetration Testing",
        compute_section_f,
    ),
    (
        "Section G",
        "G",
        "Geophysical Testing",
        compute_section_g,
    ),
    (
        "Section H",
        "H",
        "In-situ Testing",
        compute_section_h,
    ),
    (
        "Section I",
        "I",
        "Instrumentation",
        compute_section_i,
    ),
    (
        "Section J",
        "J",
        "Installation Monitoring",
        compute_section_j,
    ),
    (
        "Section K",
        "K",
        "Geotechnical Laboratory Testing",
        compute_section_k,
    ),
    (
        "Section L",
        "L",
        "Geoenvironmental Laboratory Testing",
        compute_section_l,
    ),
]


def generate_boq(project: Project, output_path: Path | str) -> Path:
    """Write a BOQ workbook for the project. Returns the absolute output path."""

    wb = Workbook()
    first = True
    for sheet_title, code, title, compute in _SECTIONS:
        ws = wb.active if first else wb.create_sheet()
        ws.title = sheet_title
        _write_section(ws, code, title, compute(project))
        first = False

    path = Path(output_path)
    wb.save(path)
    return path.resolve()


def _write_section(ws: Worksheet, code: str, title: str, items: list[BoqItem]) -> None:
    for letter, width in _COLUMN_WIDTHS.items():
        ws.column_dimensions[letter].width = width

    for col, text in enumerate(_HEADERS, start=1):
        cell = ws.cell(row=_HEADER_ROW, column=col, value=text)
        cell.font = _BOLD

    ws.cell(row=_CURRENCY_ROW, column=5, value="€")
    ws.cell(row=_CURRENCY_ROW, column=6, value="€")

    code_cell = ws.cell(row=_SECTION_HEADING_ROW, column=1, value=code)
    code_cell.font = _BOLD
    title_cell = ws.cell(row=_SECTION_HEADING_ROW, column=2, value=title)
    title_cell.font = _BOLD

    for offset, item in enumerate(items):
        r = _FIRST_ITEM_ROW + offset
        ws.cell(row=r, column=1, value=item.code)
        ws.cell(row=r, column=2, value=item.description)
        ws.cell(row=r, column=3, value=item.unit)
        ws.cell(row=r, column=4, value=item.quantity)
        ws.cell(row=r, column=6, value=f'=IFERROR(D{r}*E{r},"")')
