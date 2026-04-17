"""Schedule 2 — Exploratory Holes table.

Produces the single unified table of every scheduled exploratory hole:
number, type, grid reference (TBC until the Project model carries it),
scheduled depth in metres, and remarks (test selections and
instrumentation).

This module exports the row-building helpers in two forms:

- ``build_holes_table(project)`` — returns a bare ``Table`` ready to embed
  inside a chapter clause (used by ``clauses.body.ch2_gi_schedule``).
- ``build_schedule_2(project, ctx)`` — returns a stand-alone Schedule 2
  clause; retained for projects that want the holes table as its own
  top-level chapter (or a later Schedule-2 ``.xlsx`` generator that
  needs the same rows).

The per-hole row builders are intentionally small and explicit so the
standalone Schedule 2 ``.xlsx`` generator (build-order step 6) can reuse
them without duplication.
"""

from collections.abc import Iterator

from groundbill.models import Borehole, Project

from .context import SpecContext
from .types import Clause, Table

HOLES_TABLE_HEADERS = ["Hole No.", "Type", "Grid Reference", "Scheduled Depth (m)", "Remarks"]

_GRID_REFERENCE_TBC = "TBC"


def build_holes_table(project: Project) -> Table:
    """Return the exploratory-holes ``Table`` for the given project."""
    return Table(
        headers=list(HOLES_TABLE_HEADERS),
        rows=list(_iter_rows(project)),
    )


def build_schedule_2(project: Project, ctx: SpecContext) -> list[Clause]:
    """Return a single-clause Schedule 2 chapter wrapping the holes table."""
    del ctx  # no contextual labels needed
    return [
        Clause(
            number="Schedule 2",
            heading="Exploratory Holes",
            level=1,
            body=[build_holes_table(project)],
        )
    ]


def _iter_rows(project: Project) -> Iterator[list[str]]:
    for bh in project.boreholes:
        yield _row(
            bh.hole_number,
            "Borehole",
            f"{bh.total_schedule_depth_m:.2f}",
            _borehole_remarks(bh),
        )
    for tp in project.trial_pits:
        yield _row(
            tp.trial_pit_number,
            "Trial Pit",
            f"{tp.schedule_depth_m:.2f}",
            _tests_remarks(tp.in_situ_tests),
        )
    for tr in project.trenches:
        depth = f"{tr.overall_total_depth_m:.2f}" if tr.overall_total_depth_m is not None else "TBC"
        yield _row(tr.trench_number, "Slit Trench", depth, _tests_remarks(tr.in_situ_tests))
    for ip in project.inspection_pits:
        yield _row(
            ip.inspection_pit_number,
            "Inspection Pit",
            f"{ip.scheduled_depth_m:.2f}",
            _tests_remarks(ip.in_situ_tests),
        )
    for ds in project.dynamic_samples:
        yield _row(
            ds.sample_number,
            "Dynamic Sample",
            f"{ds.depth_m:.2f}",
            _tests_remarks(ds.tests),
        )
    for sk in project.soakaways:
        yield _row(
            sk.soakaway_id,
            "Soakaway (BRE)",
            f"{sk.schedule_depth_m:.2f}",
            _tests_remarks(sk.in_situ_tests),
        )
    for dp in project.dynamic_probes:
        yield _row(dp.probe_number, "Dynamic Probe (DPH)", f"{dp.depth_m:.2f}", "")
    for cp in project.cpts:
        yield _row(
            cp.cpt_number,
            "CPT",
            f"{cp.depth_m:.2f}",
            "Piezocone" if cp.piezocone else "",
        )


def _row(hole_number: str, hole_type: str, scheduled_depth: str, remarks: str) -> list[str]:
    return [hole_number, hole_type, _GRID_REFERENCE_TBC, scheduled_depth, remarks]


def _borehole_remarks(bh: Borehole) -> str:
    parts: list[str] = []
    if bh.tests:
        parts.append("Tests: " + ",".join(sorted(t.value for t in bh.tests)))
    if bh.piezometer_type.value != "none":
        parts.append(f"Instrumentation: {bh.piezometer_type.value}")
    return "; ".join(parts)


def _tests_remarks(tests: set) -> str:
    if not tests:
        return ""
    return "Tests: " + ",".join(sorted(t.value for t in tests))
