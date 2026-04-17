"""Specification .docx generator.

Walks the clause tree from ``groundbill.clauses`` and renders it to a Word
document using python-docx. All python-docx calls are isolated to this
module; clause modules produce pure data only.

Current structure (Rev C small-GI model):
    Cover page -> Preamble -> Body (Chapters 1-7).

Chapters 1 and 2 are populated as of Phase 3; Chapters 3-7 land in later
phases.

Word's auto-generated fields (table of contents, page-number totals) are
recalculated by Word on first open; python-docx cannot trigger that
update programmatically.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.document import Document as DocxDocument

from groundbill.clauses import (
    Clause,
    Paragraph,
    SpecContext,
    Table,
    build_body,
    build_preamble,
)
from groundbill.models import ContractRoute, Project

_MAX_HEADING_LEVEL = 9  # python-docx refuses heading levels > 9

_FALLBACK_TABLE_STYLE = "Table Grid"


def generate_spec(project: Project, output_path: Path | str) -> Path:
    """Write a specification .docx for the project; return the absolute path.

    Only the private/bespoke contract route is supported at present; PW-CF
    (Irish public works) is deferred to a parallel clause tree in a later
    phase. Passing a ``PW_CF`` project raises ``NotImplementedError``
    loudly rather than producing a half-correct document.
    """
    if project.contract_route is not ContractRoute.PRIVATE:
        raise NotImplementedError(
            "Specification generator currently supports ContractRoute.PRIVATE only; "
            f"got {project.contract_route.value!r}."
        )

    ctx = SpecContext.from_project(project)
    doc = Document()
    _render_cover_page(doc, ctx)

    for clause in build_preamble(project, ctx):
        _render_clause(doc, clause)
    for clause in build_body(project, ctx):
        _render_clause(doc, clause)

    path = Path(output_path)
    doc.save(path)
    return path.resolve()


def _render_cover_page(doc: DocxDocument, ctx: SpecContext) -> None:
    doc.add_heading("Ground Investigation Specification", level=0)
    doc.add_paragraph(ctx.project_name)
    doc.add_paragraph(ctx.site_address)
    doc.add_paragraph(f"Contract route: {ctx.contract_route_label}")
    doc.add_paragraph(f"Site category: {ctx.site_category_label}")
    doc.add_paragraph(f"Date: {ctx.today.isoformat()}")
    doc.add_page_break()


def _render_clause(doc: DocxDocument, clause: Clause) -> None:
    heading_text = f"{clause.number} {clause.heading}".strip()
    level = max(1, min(clause.level, _MAX_HEADING_LEVEL))
    doc.add_heading(heading_text, level=level)
    for item in clause.body:
        if isinstance(item, Paragraph):
            _render_paragraph(doc, item)
        else:
            _render_table(doc, item)
    for child in clause.children:
        _render_clause(doc, child)


def _render_paragraph(doc: DocxDocument, para: Paragraph) -> None:
    style = _list_style(para.list_level) if para.list_level is not None else para.style
    try:
        p = doc.add_paragraph(style=style)
    except KeyError:
        p = doc.add_paragraph()
    for run in para.runs:
        r = p.add_run(run.text)
        r.bold = run.bold
        r.italic = run.italic


def _render_table(doc: DocxDocument, table: Table) -> None:
    rows_total = len(table.rows) + 1  # +1 for header row
    cols_total = len(table.headers)
    t = doc.add_table(rows=rows_total, cols=cols_total)
    try:
        t.style = table.style
    except KeyError:
        t.style = _FALLBACK_TABLE_STYLE

    for col_index, header in enumerate(table.headers):
        cell = t.rows[0].cells[col_index]
        cell.text = header
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True

    for row_index, row in enumerate(table.rows, start=1):
        for col_index, value in enumerate(row):
            t.rows[row_index].cells[col_index].text = value


def _list_style(level: int) -> str:
    """Map a 0-indexed list level to the corresponding python-docx style.

    python-docx ships "List Bullet" for level 0 and "List Bullet 2",
    "List Bullet 3", ... for nested levels.
    """
    if level == 0:
        return "List Bullet"
    return f"List Bullet {level + 1}"
