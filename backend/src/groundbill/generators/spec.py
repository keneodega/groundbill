"""Specification .docx generator.

Walks the clause tree from ``groundbill.clauses`` and renders it to a Word
document using python-docx. All python-docx calls are isolated to this
module; clause modules produce pure data only.

Document structure:
    Cover page -> Preamble -> Body (Chapters 1-7 from Master Small GI
    Specification Rev C).

Styling applied in Phase 6 (minimum viable polish; finer parity with
Havilah's issued deliverables needs a redacted sample to copy fonts
and margins from):
    - Page break between each top-level chapter (Preamble, 1, 2, ... 7)
    - Running header with spec title and project name
    - Running footer with a dynamic page-number field

Word recalculates auto-generated fields (the page-number field below,
plus any TOC) on first open; python-docx cannot trigger that update
programmatically, so a freshly generated file may show "PAGE" as
literal text until Word is allowed to update fields. Most modern Word
versions update fields automatically when opening the document.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.document import Document as DocxDocument
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph as DocxParagraph

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
    _apply_running_header(doc, ctx)
    _apply_running_footer(doc)
    _render_cover_page(doc, ctx)

    # Assemble every top-level clause (Preamble + the seven chapters) in order
    # so we can drop page breaks between them without special-casing.
    top_level_clauses: list[Clause] = []
    top_level_clauses.extend(build_preamble(project, ctx))
    top_level_clauses.extend(build_body(project, ctx))

    for index, clause in enumerate(top_level_clauses):
        _render_clause(doc, clause)
        if index < len(top_level_clauses) - 1:
            doc.add_page_break()

    path = Path(output_path)
    doc.save(path)
    return path.resolve()


# ---------------------------------------------------------------------------
# Cover page
# ---------------------------------------------------------------------------


def _render_cover_page(doc: DocxDocument, ctx: SpecContext) -> None:
    doc.add_heading("Ground Investigation Specification", level=0)
    doc.add_paragraph(ctx.project_name)
    doc.add_paragraph(ctx.site_address)
    doc.add_paragraph(f"Contract route: {ctx.contract_route_label}")
    doc.add_paragraph(f"Site category: {ctx.site_category_label}")
    doc.add_paragraph(f"Date: {ctx.today.isoformat()}")
    doc.add_page_break()


# ---------------------------------------------------------------------------
# Running header and footer
# ---------------------------------------------------------------------------


def _apply_running_header(doc: DocxDocument, ctx: SpecContext) -> None:
    """Add a simple header: spec title on the left, project name on the right.

    Uses a single tab stop to separate left- and right-aligned runs — the
    standard Word idiom for "A | ... | B" headers without inserting a table.
    """
    header = doc.sections[0].header
    paragraph = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    paragraph.text = ""  # reset the default empty paragraph
    paragraph.add_run("Ground Investigation Specification")
    paragraph.add_run("\t\t")
    paragraph.add_run(ctx.project_name)


def _apply_running_footer(doc: DocxDocument) -> None:
    """Add a right-aligned page-number field to the footer.

    python-docx doesn't expose Word fields directly, so we inject the
    ``PAGE`` field as raw OOXML. Word recalculates the field value on
    first open of the document.
    """
    footer = doc.sections[0].footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.text = ""
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    paragraph.add_run("Page ")
    _add_page_number_field(paragraph)


def _add_page_number_field(paragraph: DocxParagraph) -> None:
    """Append a Word PAGE field to the paragraph.

    The field is expressed as the canonical three-element XML sequence
    Word emits for simple fields: begin -> instrText -> end. Word
    substitutes the current page number when fields are updated.
    """
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")

    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"

    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)


# ---------------------------------------------------------------------------
# Clause rendering
# ---------------------------------------------------------------------------


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
