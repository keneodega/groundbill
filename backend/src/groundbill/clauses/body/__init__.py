"""Main-body chapters of the Specification.

The document's body is divided into seven chapters mirroring the structure
of ``Master Small GI Specification Rev C.docx`` (see
``reference/specification_info/source_outline.txt``). Each chapter lives
in its own module and exposes a ``build_chN_*`` function returning one
top-level ``Clause`` (with nested children for sub-sections). The
``build_body`` aggregator simply collects them in order.

Phase 3 implements Chapter 1 (Introduction) and Chapter 2 (GI Schedule).
Chapters 3-7 land in Phases 4-6.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..types import Clause
from .ch1_introduction import build_ch1_introduction
from .ch2_gi_schedule import build_ch2_gi_schedule
from .ch3_sampling_requirements import build_ch3_sampling_requirements


def build_body(project: Project, ctx: SpecContext) -> list[Clause]:
    """Return the ordered list of main-body chapters for the specification."""
    return [
        build_ch1_introduction(project, ctx),
        build_ch2_gi_schedule(project, ctx),
        build_ch3_sampling_requirements(project, ctx),
        # build_ch4_lab_testing(project, ctx),            # Phase 5
        # build_ch5_testing_scheduling(project, ctx),     # Phase 5
        # build_ch6_reporting(project, ctx),              # Phase 5
        # build_ch7_further_information(project, ctx),    # Phase 6
    ]


__all__ = [
    "build_body",
    "build_ch1_introduction",
    "build_ch2_gi_schedule",
    "build_ch3_sampling_requirements",
]
