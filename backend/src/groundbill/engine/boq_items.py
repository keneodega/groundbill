"""Shared BOQ line-item model used by every section of the calculation engine."""

from pydantic import BaseModel, ConfigDict, Field


class BoqItem(BaseModel):
    """One line in the Bill of Quantities.

    ``quantity`` is deliberately polymorphic to mirror the source workbook's
    Quantity column, which holds either a computed number or a text placeholder
    (``"Not Required"``, ``"Included in A7"``, ``"included in A2"``, etc.).

    ``subheading`` carries the workbook's un-numbered heading rows (bold,
    underlined text in column B, e.g. "Land-based mapping techniques"). It is
    set only on the first item beneath each heading; the generator writes the
    heading as its own row immediately above that item.
    """

    model_config = ConfigDict(extra="forbid")

    code: str = Field(description="Item code, e.g. 'A1', 'A2.3', 'B1.1'")
    description: str
    unit: str = Field(description="Unit of measure, e.g. 'sum', 'Nr', 'per day', '%'")
    quantity: int | float | str | None = None
    subheading: str | None = Field(
        default=None,
        description="Sub-heading row that precedes this item in the workbook, if any",
    )
