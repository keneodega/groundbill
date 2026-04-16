"""BOQ .xlsx generator.

Produces a Bill of Quantities workbook whose layout matches
`reference/excel/4_BOQ_Contractor_Rev_A.xlsx`:

- Data starts at row 7 (header row).
- Row 8 holds the currency markers (€ in cols E and F).
- Row 9 is the section heading (code and title, bold).
- Row 10 onwards is one BOQ item per row across columns A-F:
  A=Number, B=Item description, C=Unit, D=Quantity, E=Rate, F=Amount.

The Amount cell is written as ``=IFERROR(D*E, "")`` so it resolves to the
priced total once the contractor fills in the Rate column, and stays blank
otherwise.

Currently only Section A is implemented; sections B-L will be added as each
is translated in the calculation engine.
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from groundbill.engine import compute_section_a
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


def generate_boq(project: Project, output_path: Path | str) -> Path:
    """Write a BOQ workbook for the project. Returns the absolute output path."""

    wb = Workbook()
    section_a_ws = wb.active
    section_a_ws.title = "Section A"
    _write_section_a(section_a_ws, project)

    path = Path(output_path)
    wb.save(path)
    return path.resolve()


def _write_section_a(ws: Worksheet, project: Project) -> None:
    for letter, width in _COLUMN_WIDTHS.items():
        ws.column_dimensions[letter].width = width

    for col, text in enumerate(_HEADERS, start=1):
        cell = ws.cell(row=_HEADER_ROW, column=col, value=text)
        cell.font = _BOLD

    ws.cell(row=_CURRENCY_ROW, column=5, value="€")
    ws.cell(row=_CURRENCY_ROW, column=6, value="€")

    code_cell = ws.cell(row=_SECTION_HEADING_ROW, column=1, value="A")
    code_cell.font = _BOLD
    title_cell = ws.cell(
        row=_SECTION_HEADING_ROW,
        column=2,
        value="General items, provisional services and additional items",
    )
    title_cell.font = _BOLD

    for offset, item in enumerate(compute_section_a(project)):
        r = _FIRST_ITEM_ROW + offset
        ws.cell(row=r, column=1, value=item.code)
        ws.cell(row=r, column=2, value=item.description)
        ws.cell(row=r, column=3, value=item.unit)
        ws.cell(row=r, column=4, value=item.quantity)
        ws.cell(row=r, column=6, value=f'=IFERROR(D{r}*E{r},"")')
