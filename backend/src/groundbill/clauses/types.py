"""Dumb-data types for specification clauses.

These classes describe *what* to render in the specification document, not
*how* to render it. Any python-docx specific logic lives in
``groundbill.generators.spec``. Keeping the clause modules free of
Word-library imports means clause authors only need to think about content,
and the renderer can be swapped (e.g. to produce PDF or HTML later) without
touching the clause library.

Design note for future readers: ``Clause`` is self-referential — a clause
can contain child clauses for sub-sub numbering (S1.3.2 under S1.3). Pydantic
v2 resolves the forward reference to ``"Clause"`` automatically within the
same class body.
"""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    """Shared config — forbid unknown fields so clause authoring stays explicit."""

    model_config = ConfigDict(extra="forbid")


class Run(_Base):
    """A span of formatted text within a paragraph (bold/italic inline)."""

    text: str
    bold: bool = False
    italic: bool = False


class Paragraph(_Base):
    """One paragraph of body text.

    ``list_level`` drives bullet/number-list rendering:
    ``None`` = ordinary body text, ``0`` = first-level bullet, ``1`` = nested,
    and so on. ``style`` is the Word paragraph style name; the renderer
    falls back to "Normal" if the requested style is missing.
    """

    runs: list[Run] = Field(default_factory=list)
    style: str = "Normal"
    list_level: int | None = None


class Table(_Base):
    """A tabular body element rendered as a Word table.

    ``rows`` is a list of rows; each row is a list of cell strings with the
    same length as ``headers``. Validation of row-width is left to the
    builder (the renderer would simply produce a ragged table).
    """

    headers: list[str]
    rows: list[list[str]]
    style: str = "Light Grid Accent 1"


class Clause(_Base):
    """One specification clause. May contain nested child clauses.

    ``level`` controls the Word heading style (1 = Heading 1, 2 = Heading 2,
    etc.). Numbers are hard-coded by the clause builder rather than
    auto-derived from tree position, because the spec's numbering must match
    the authoritative source document one-for-one.
    """

    number: str
    heading: str
    level: int = 1
    body: list[Paragraph | Table] = Field(default_factory=list)
    children: list["Clause"] = Field(default_factory=list)
