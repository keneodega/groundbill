"""Chapter 3 — Geotechnical Sampling and In-situ Testing Requirements.

Mirrors Chapter 3 of Master Small GI Specification Rev C. The opening
paragraphs (CAT-scan, HSA references, groundwater recording, backfill)
apply to any intrusive investigation and are always rendered. Each
per-method sub-section is always emitted so numbering stays stable
project-to-project; sub-sections whose method is unused show a short
"Not applicable to this contract" body instead of the full clause text.

Source text transcribed from ``reference/specification_info/ch3_full_text.txt``.
Project-specific phrases from the source (e.g. "3 of the boreholes",
"13-tonne excavator") have been either derived from ``SpecContext`` or
generalised so the output is correct for any project.
"""

from groundbill.models import Project

from ..context import SpecContext
from ..types import Clause, Paragraph, Run

_NOT_APPLICABLE = "Not applicable to this contract."


def build_ch3_sampling_requirements(project: Project, ctx: SpecContext) -> Clause:
    """Return the Chapter 3 clause, with all nine sub-sections."""
    return Clause(
        number="3",
        heading="Geotechnical Sampling and In-situ Testing Requirements",
        level=1,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "A CAT scan is to be carried out and inspection pits are to be "
                            "excavated by hand to depths of 1.2 m at each exploratory hole "
                            "location where services may be encountered. Under the Safety, "
                            "Health and Welfare at Work (Construction) Regulations 2013, "
                            "persons carrying out the task of locating underground services "
                            "are required to be in possession of a Construction Skills "
                            "Certification Scheme (CSCS) card."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "In addition, avoidance of underground services shall follow the "
                            "guidance outlined in the 'Code of Practice For Avoiding Danger "
                            "From Underground Services', 2010, published by the HSA. CAT scans "
                            "shall be undertaken in accordance with UK HSG47 'Avoiding danger "
                            "from underground services' (2000, published by UK HSE) by an "
                            "approved and qualified operator."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Groundwater strikes or inflow encountered within any exploratory "
                            "hole shall be recorded and presented on the engineering logs."
                        )
                    )
                ]
            ),
            Paragraph(
                runs=[Run(text="All ground investigation holes must be backfilled and left safe.")]
            ),
        ],
        children=[
            _build_hard_standing(ctx),
            _build_cable_percussion(ctx),
            _build_rotary_drilling(ctx),
            _build_dynamic_probes(ctx),
            _build_trial_pits(ctx),
            _build_slit_trenching(project, ctx),
            _build_insitu_testing(ctx),
            _build_contamination_avoidance(ctx),
            _build_photography(ctx),
        ],
    )


# ---------------------------------------------------------------------------
# 3.1 Hard Standing
# ---------------------------------------------------------------------------


def _build_hard_standing(ctx: SpecContext) -> Clause:
    if not ctx.has_hard_standing:
        return _not_applicable_clause("3.1", "Hard Standing")
    return Clause(
        number="3.1",
        heading="Hard Standing",
        level=2,
        body=[
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "Some exploratory holes will be carried out on areas covered by "
                            "concrete pavement of unknown thickness, but can typically be "
                            "expected at a thickness of 0.3 m. The use of the correct method "
                            "to penetrate the hard standing shall be determined by the "
                            "Contractor after inspection of the site."
                        )
                    )
                ]
            )
        ],
    )


# ---------------------------------------------------------------------------
# 3.2 Cable Percussion Boring
# ---------------------------------------------------------------------------


def _build_cable_percussion(ctx: SpecContext) -> Clause:
    if not ctx.has_cable_percussion:
        return _not_applicable_clause("3.2", "Cable Percussion Boring")
    return Clause(
        number="3.2",
        heading="Cable Percussion Boring",
        level=2,
        body=[
            _p(
                "The Contractor shall select plant appropriate to the proposed drill "
                "locations, depths and anticipated geological conditions. The method of "
                "advancement and the diameter of the borehole shall be such that the boring "
                "can be completed and logged to the scheduled depth."
            ),
            _p(
                "Soil boring shall be undertaken using a rig with the capability of "
                "undertaking Standard Penetration Tests (SPT) and U100 samples. The Engineer "
                "is to be notified of the intended plant/soil-boring rig prior to "
                "commencement on site."
            ),
            _p("Casing may be required."),
            _p(
                "Cable Percussion holes shall be taken to the indicative depth proposed in "
                "the exploratory holes schedule to this Specification, or refusal, whichever "
                "comes first."
            ),
            _p(
                "Starting hole diameter shall be a minimum of 200 mm. The Contractor shall "
                "agree with the Investigation Supervisor reductions in casing diameter with "
                "depth depending on the ground conditions encountered."
            ),
            _p(
                "The position, number and depth of each exploratory hole may be subject to "
                "adjustment on site as directed by the Engineer."
            ),
            _p(
                "The Contractor shall allow for whatever plant and/or equipment they deem "
                "necessary in order to safely locate the drilling rig in the vicinity of the "
                "proposed hole locations."
            ),
            _p("Any groundwater seepage shall be recorded on the borehole logs."),
            _p(
                "The Contractor is required to obtain the Engineer's approval before "
                "commencing and before backfilling any borehole. The Engineer will give any "
                "installation details and backfill instructions."
            ),
        ],
    )


# ---------------------------------------------------------------------------
# 3.3 Rotary Drilling
# ---------------------------------------------------------------------------


def _build_rotary_drilling(ctx: SpecContext) -> Clause:
    if not ctx.has_rotary:
        return _not_applicable_clause("3.3", "Rotary Drilling")

    scope_intro = (
        f"Rotary coring is required as a cable-percussive technique follow-on for "
        f"{ctx.rotary_borehole_count} of the boreholes. It is expected to be required "
        "through soil and rock. Unless otherwise instructed by the Investigation "
        "Supervisor, all Rotary Cored Boreholes will be cored to a minimum of 5 m into "
        "substantially unweathered competent rock at each location where rock is "
        "encountered. Rotary coring is required from rockhead in all boreholes where "
        "rock is encountered."
    )

    return Clause(
        number="3.3",
        heading="Rotary Drilling",
        level=2,
        body=[
            _p(scope_intro),
            _p(
                "The Contractor may use an alternative method for drilling in the overburden "
                "and rock, subject to approval. This method may consist of other similar "
                "rotary techniques to achieve the minimum hole diameter in one drilling "
                "operation."
            ),
            _p(
                "Rotary coring may also be permitted or required through soil from 1.20 m "
                "level or at depth instead of cable-percussive techniques. Unless otherwise "
                "instructed or agreed with the Investigation Supervisor, it shall consist of "
                "hollow-stem auger, Geobor S or other similar techniques subject to approval "
                "by the Investigation Supervisor, using a semi-rigid liner and producing a "
                "continuous core not less than 100 mm in diameter."
            ),
            _p(
                "Where rotary coring is scheduled at cable-percussive borehole locations, it "
                "is to be carried out from the final depth of the cable-percussive borehole "
                "at that location. If rotary coring is required in rock, the same rig shall "
                "be used for coring through soil and rock without additional setting-up at "
                "the borehole location."
            ),
            _p(
                "If the cable-percussive borehole does not reach bedrock, rotary coring is "
                "required from the final depth of the cable-percussive borehole through the "
                "overburden and weathered bedrock. In-situ testing in the form of SPTs in "
                "cohesive materials and CPTs in granular material shall be carried out at "
                "regular intervals. Samples should be obtained from the split spoon."
            ),
            _p(
                "All boreholes shall be backfilled (with grout, bentonite pellets or "
                "instrumentation installation) immediately upon completion of drilling, and "
                "the location and access route(s) reinstated as close as possible to the "
                "original ground condition. All dismantled or damaged walls, fences, edges "
                "etc. must be reinstated and made good."
            ),
            _p(
                "Where exploratory holes are carried out in grassed areas, the ground shall "
                "be reinstated as close as possible to the existing condition prior to the "
                "start of the works, including topsoiling and reseeding. This includes any "
                "damage to grassed areas along access routes to exploratory hole locations."
            ),
            _p(
                "Where boreholes are not completed in the day they are commenced, or when "
                "left unattended, the entire work area shall be fenced off at the end of the "
                "shift by the Contractor using Heras or similar style fencing."
            ),
            _p(
                "Rotary-cored boreholes are to be carried out to produce continuous core of "
                "not less than 92 mm in rock and 100 mm in soil, to allow Class 1 samples to "
                "be retrieved for laboratory testing. The drilling diameter shall allow for "
                "casing if required in unstable ground in order to achieve the required core "
                "diameter."
            ),
            _p(
                "Advancing the hole to the scheduled depth is not permitted unless specified "
                "in the exploratory holes schedule. If the Contractor chooses to use "
                "open-hole drilling techniques, this shall be at their own cost in order to "
                "retrieve the depth of a borehole already achieved by cable-percussive "
                "and/or rotary-coring techniques."
            ),
        ],
    )


# ---------------------------------------------------------------------------
# 3.4 Dynamic Probes
# ---------------------------------------------------------------------------


def _build_dynamic_probes(ctx: SpecContext) -> Clause:
    if ctx.dynamic_probe_count == 0:
        return _not_applicable_clause("3.4", "Dynamic Probes")
    depth_phrase = (
        f"an anticipated maximum depth of up to {ctx.max_dynamic_probe_depth_m:.1f} m"
        if ctx.max_dynamic_probe_depth_m is not None
        else "the depths set out in the exploratory holes schedule"
    )
    return Clause(
        number="3.4",
        heading="Dynamic Probes",
        level=2,
        body=[
            _p(
                f"{ctx.dynamic_probe_count} no. Dynamic Probe Heavy (DPH) to be put down to "
                f"{depth_phrase}."
            )
        ],
    )


# ---------------------------------------------------------------------------
# 3.5 Trial Pits
# ---------------------------------------------------------------------------


def _build_trial_pits(ctx: SpecContext) -> Clause:
    if ctx.trial_pit_count == 0:
        return _not_applicable_clause("3.5", "Trial Pits")
    depth_phrase = (
        f"a scheduled depth of {ctx.max_trial_pit_depth_m:.1f} m"
        if ctx.max_trial_pit_depth_m is not None
        else "the scheduled depths set out in the exploratory holes schedule"
    )
    return Clause(
        number="3.5",
        heading="Trial Pits",
        level=2,
        body=[
            _p(
                "An appropriately sized tracked excavator will be required to complete the "
                f"trial pits to {depth_phrase}."
            ),
            _p("Hand vanes will be required every metre in cohesive material."),
            _p("DCPs will be required in every trial pit at a depth of 1.2 mbgl."),
            _p("Environmental samples will be required in any Made Ground encountered."),
            _p(
                "Bulk bag and tub samples should be taken at 0.5 m, 1 m and every metre "
                "thereafter, and at every change in stratum."
            ),
        ],
    )


# ---------------------------------------------------------------------------
# 3.6 Slit Trenching
# ---------------------------------------------------------------------------


def _build_slit_trenching(project: Project, ctx: SpecContext) -> Clause:
    del project  # trench count is already available via ctx
    if ctx.trench_count == 0:
        return _not_applicable_clause("3.6", "Slit Trenching")
    depth_phrase = (
        f"a depth of {ctx.max_trench_depth_m:.1f} mbgl"
        if ctx.max_trench_depth_m is not None
        else "the scheduled depths set out in the exploratory holes schedule"
    )
    return Clause(
        number="3.6",
        heading="Slit Trenching",
        level=2,
        body=[
            _p(
                "The slit trenches should locate the services identified and will be to "
                f"{depth_phrase}. The slit trenches should also identify any foundations "
                "from demolition or Made Ground."
            )
        ],
    )


# ---------------------------------------------------------------------------
# 3.7 In-situ Testing, Sampling and Monitoring
# ---------------------------------------------------------------------------


def _build_insitu_testing(ctx: SpecContext) -> Clause:
    # Always render — any investigation that reaches this chapter has some form
    # of sampling or monitoring.
    del ctx
    return Clause(
        number="3.7",
        heading="In-situ Testing, Sampling and Monitoring",
        level=2,
        body=[
            _p(
                "Standard Penetration Testing in accordance with IS EN ISO 22476-3 shall be "
                "undertaken at 1 m intervals, alternating with thin-walled open-tube sampling "
                "(UT100) where in a cohesive stratum."
            ),
            _p(
                "In granular soils SPTs shall be taken at 1.0 m intervals to borehole "
                "completion. The mass, dimensions, energy ratio and calibration sheets of "
                "the SPT equipment shall be provided with the engineering log."
            ),
            _p(
                "Undisturbed samples shall be recovered by use of a UT100 capable of "
                "obtaining a sample of a minimum diameter of 100 mm, complying with "
                "Clause 6.4.2.3.2 of IS EN ISO 22475-1:2006."
            ),
            _p(
                "Bulk bag, plastic tub and jar samples shall be taken immediately below "
                "topsoil, at every change of strata and at one-metre intervals within the "
                "same stratum for soil description logging purposes in all exploratory "
                "holes. Where samples are taken at depths corresponding to the boundary of "
                "two material types, the Contractor shall clearly state which of the "
                "materials has been sampled."
            ),
            _p(
                "Where groundwater samples are taken at a depth corresponding to a boundary "
                "between different materials, the Contractor shall clearly state within "
                "which material the water is associated."
            ),
            _p(
                "The Contractor shall ensure that sufficient sample quantities are collected "
                "for the material type in question and for the likely laboratory testing "
                "required (refer to Chapter 4). Where insufficient sample is available for "
                "testing, the Contractor shall be responsible, at their cost, for the "
                "collection of sufficient material to test."
            ),
            _p(
                "Where there is suspected asbestos encountered, a double-bagged sample shall "
                "be taken and clearly labelled as potentially containing asbestos."
            ),
        ],
    )


# ---------------------------------------------------------------------------
# 3.8 Contamination Avoidance / Aquifer Protection
# ---------------------------------------------------------------------------


def _build_contamination_avoidance(ctx: SpecContext) -> Clause:
    del ctx
    return Clause(
        number="3.8",
        heading="Contamination Avoidance and Aquifer Protection",
        level=2,
        body=[
            _p(
                "Asbestos awareness procedures shall be in place in case asbestos is "
                "encountered, so as to minimise the risk of harm to human health."
            ),
            _p("Containment of fluid for all works is to be suitably compounded."),
            _p(
                "All equipment shall be thoroughly cleaned before being used on site. A "
                "clean stainless-steel trowel shall be used to sub-sample soil samples for "
                "chemical testing, cleaned between samples. When working on land affected "
                "by contamination, the Contractor shall clean equipment (including wheels) "
                "before leaving the site and, where deemed necessary, between exploratory "
                "hole positions."
            ),
            _p(
                "If significant contamination is encountered, sampling equipment and tools "
                "shall be cleaned between strata, specifically at the boundary between Made "
                "Ground and natural strata, in order to prevent cross-contamination."
            ),
            _p("The Contractor may only use vegetable oil-based lubricants."),
        ],
    )


# ---------------------------------------------------------------------------
# 3.9 Photography Requirements
# ---------------------------------------------------------------------------


def _build_photography(ctx: SpecContext) -> Clause:
    del ctx
    return Clause(
        number="3.9",
        heading="Photography Requirements",
        level=2,
        body=[
            _p(
                "The Contractor shall provide sufficient digital photographs to show the "
                "condition of each exploratory hole location prior to the start of the "
                "investigation works and on completion of the investigation."
            ),
            _p(
                "Digital copies of the photographs shall be provided to the Investigation "
                "Supervisor within 48 hours of being taken."
            ),
            _p(
                "All inspection pits and trial pits shall be photographed to show a general "
                "view of the pit and excavation arisings, plus separate views of each "
                "excavated face and any foundations exposed, as well as any noted "
                "contamination. Photographs shall include:"
            ),
            Paragraph(
                runs=[
                    Run(text="A colour chart and graduated scale in centimetres; and"),
                ],
                list_level=0,
            ),
            Paragraph(
                runs=[
                    Run(
                        text=(
                            "A clearly legible reference board identifying the project title, "
                            "exploratory hole number, date and depth range of drill runs, "
                            "included in each photograph."
                        )
                    ),
                ],
                list_level=0,
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _p(text: str) -> Paragraph:
    """Shorthand: build a simple single-run paragraph of plain body text."""
    return Paragraph(runs=[Run(text=text)])


def _not_applicable_clause(number: str, heading: str) -> Clause:
    return Clause(
        number=number,
        heading=heading,
        level=2,
        body=[_p(_NOT_APPLICABLE)],
    )
