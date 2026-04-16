"""Sanity tests for the Pydantic domain models."""

import pytest
from pydantic import ValidationError

from groundbill.models import (
    Borehole,
    ContractRoute,
    DrillingMethod,
    DrillingPhase,
    InSituTest,
    LabSchedule,
    LabTestAllocation,
    Project,
    PSEVTest,
    SiteCategory,
    TrialPit,
)


def test_project_accepts_minimal_definition():
    project = Project(
        name="Sample Site",
        site_address="1 Test Street, Dublin",
        contract_route=ContractRoute.PRIVATE,
    )
    assert project.site_category is SiteCategory.GREEN
    assert project.boreholes == []
    assert project.lab_schedule.allocations == []


def test_project_composes_boreholes_trial_pits_and_lab_schedule():
    project = Project(
        name="Sample Site",
        site_address="1 Test Street, Dublin",
        contract_route=ContractRoute.PW_CF,
        site_category=SiteCategory.YELLOW,
        boreholes=[
            Borehole(
                hole_number="BH01",
                phases=[
                    DrillingPhase(method=DrillingMethod.CABLE_PERCUSSION, depth_m=10.0),
                    DrillingPhase(method=DrillingMethod.ROTARY_CORE_HARD, depth_m=5.0),
                ],
                total_schedule_depth_m=15.0,
                tests={PSEVTest.S, PSEVTest.EV},
            ),
        ],
        trial_pits=[
            TrialPit(
                trial_pit_number="TP01",
                schedule_depth_m=3.0,
                in_situ_tests={InSituTest.DCP, InSituTest.HV},
                width_m=1.0,
                length_m=2.0,
                depth_m=3.0,
            ),
        ],
        lab_schedule=LabSchedule(
            allocations=[
                LabTestAllocation(test_name="Moisture content", quantity=40),
            ],
        ),
    )

    assert project.boreholes[0].phases[0].method is DrillingMethod.CABLE_PERCUSSION
    assert project.boreholes[0].tests == {PSEVTest.S, PSEVTest.EV}
    assert project.trial_pits[0].in_situ_tests == {InSituTest.DCP, InSituTest.HV}
    assert project.lab_schedule.allocations[0].quantity == 40


def test_project_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        Project(
            name="X",
            site_address="Y",
            contract_route=ContractRoute.PRIVATE,
            unknown_field="boom",
        )


def test_borehole_requires_positive_schedule_depth():
    with pytest.raises(ValidationError):
        Borehole(hole_number="BH01", total_schedule_depth_m=0.0)
