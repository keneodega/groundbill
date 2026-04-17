"""Specification clause library.

The ``clauses/`` tree is the structural source for the .docx output. Each
submodule returns dumb-data ``Clause`` objects; the actual rendering to
Word lives in ``groundbill.generators.spec``. This separation means a
clause author only needs to think about content, not about python-docx
APIs, and the rendering layer can be swapped later (for example, a PDF
or HTML exporter) without touching clause content.
"""

from .body import build_body
from .context import TBC_MARKER, SpecContext
from .preamble import build_preamble
from .schedule_2 import build_holes_table, build_schedule_2
from .types import Clause, Paragraph, Run, Table

__all__ = [
    "Clause",
    "Paragraph",
    "Run",
    "SpecContext",
    "TBC_MARKER",
    "Table",
    "build_body",
    "build_holes_table",
    "build_preamble",
    "build_schedule_2",
]
