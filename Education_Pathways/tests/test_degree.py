import pytest
from degree import Major, Minor


@pytest.fixture
def minor():
    """
    Returns a minor instance hardcoded to the AI minor
    """
    # Test data
    name = "Artificial Intelligence Minor"
    requirements = [
        ["APS360H1"],
        ["CSC263H1", "ECE345H1", "ECE358H1", "MIE335H1"],
        ["CSC384H1", "MIE369H1", "ROB311H1"],
        ["CSC311H1", "ECE421H1", "MIE424H1", "ROB313H1"],
        [
            "CHE507H1",
            "CSC401H1",
            "CHE507H1",
            "CSC401H1",
            "CSC420H1",
            "CSC413H1",
            "CSC485H1",
            "CSC486H1",
            "ECE368H1",
            "HPS345H1",
            "HPS346H1",
            "MIE368H1",
            "MIE451H1",
            "MIE457H1",
            "MIE562H1",
            "MIE566H1",
            "MSE403H1",
            "ROB501H1",
        ],
        [
            "CHE507H1",
            "CSC401H1",
            "CHE507H1",
            "CSC401H1",
            "CSC420H1",
            "CSC413H1",
            "CSC485H1",
            "CSC486H1",
            "ECE368H1",
            "HPS345H1",
            "HPS346H1",
            "MIE368H1",
            "MIE451H1",
            "MIE457H1",
            "MIE562H1",
            "MIE566H1",
            "MSE403H1",
            "ROB501H1",
            "AER336H1",
            "BME595H1",
            "CHE322H1",
            "CSC343H1",
            "CSC412H1",
            "ECE344H1",
            "ECE353H1",
            "ECE356H1",
            "ECE367H1",
            "ECE411H1",
            "ECE419H1",
            "ECE431H1",
            "ECE444H1",
            "ECE454H1",
            "ECE470H1",
            "ECE516H1",
            "ECE532H1",
            "ECE557H1",
            "ECE568H1",
            "MAT336H1",
            "MAT389H1",
            "STA302H1",
            "STA410H1",
        ],
    ]

    return Minor(name=name, requirements=requirements)


def test_minor_construction(minor):
    # Check class construction
    assert minor.name
    assert minor.requirements


def test_minor_contains(minor):
    # Check __contains__
    assert "CSC401H1" in minor, "CSC401H1 should be in " + minor
    assert not "APS111H1" in minor, "APS111H1 should not be in " + minor


def test_minor_progress(minor):
    # Check minor progress

    # Check correct list
    correct_course_list = [
        "APS360H1",
        "ECE358H1",
        "ROB311H1",
        "CSC311H1",
        "CSC485H1",
        "CHE322H1",
    ]
    progress_list = minor.check_progress(correct_course_list)
    for req in progress_list:
        assert req[1] == True, f"The Minor requirement {req} should be fulfilled"

    # Check blank list
    incorrect_course_list1 = []
    progress_list = minor.check_progress(incorrect_course_list1)
    for req in progress_list:
        assert req[1] == False, f"The Minor requirement {req} should not be fulfilled"

    # Check incorrect list with course that fulfills multiple requirements
    incorrect_course_list2 = [
        "APS360H1",
        "ECE358H1",
        "ROB311H1",
        "CSC311H1",
        "CHE507H1",
    ]
    progress_list = minor.check_progress(incorrect_course_list2)
    for req in progress_list:
        if req[0] == [
            "CHE507H1",
            "CSC401H1",
            "CHE507H1",
            "CSC401H1",
            "CSC420H1",
            "CSC413H1",
            "CSC485H1",
            "CSC486H1",
            "ECE368H1",
            "HPS345H1",
            "HPS346H1",
            "MIE368H1",
            "MIE451H1",
            "MIE457H1",
            "MIE562H1",
            "MIE566H1",
            "MSE403H1",
            "ROB501H1",
            "AER336H1",
            "BME595H1",
            "CHE322H1",
            "CSC343H1",
            "CSC412H1",
            "ECE344H1",
            "ECE353H1",
            "ECE356H1",
            "ECE367H1",
            "ECE411H1",
            "ECE419H1",
            "ECE431H1",
            "ECE444H1",
            "ECE454H1",
            "ECE470H1",
            "ECE516H1",
            "ECE532H1",
            "ECE557H1",
            "ECE568H1",
            "MAT336H1",
            "MAT389H1",
            "STA302H1",
            "STA410H1",
        ]:
            assert (
                req[1] == False
            ), f"The Minor requirement {req} should not be fulfilled"
        else:
            assert req[1] == True, f"The Minor requirement {req} should be fulfilled"


def test_minor_completion(minor):
    # Check minor completion
    # Check correct list
    correct_course_list = [
        "APS360H1",
        "ECE358H1",
        "ROB311H1",
        "CSC311H1",
        "CSC485H1",
        "CHE322H1",
    ]
    assert minor.check_completion(
        correct_course_list
    ), "This course list should fulfill minor requirements"

    # Check blank list
    incorrect_course_list1 = []
    assert not minor.check_completion(
        incorrect_course_list1
    ), "This course list should not fulfill minor requirements"

    # Check incorrect list with course that fulfills multiple requirements
    incorrect_course_list2 = [
        "APS360H1",
        "ECE358H1",
        "ROB311H1",
        "CSC311H1",
        "CHE507H1",
    ]
    assert not minor.check_completion(
        incorrect_course_list2
    ), "This course list should not fulfill minor requirements"


@pytest.fixture
def major():
    """
    Returns a major instance hardcoded with 4th Year EngSci MI requirements
    """
    name = "Engineering Science - Machine Intelligence"
    core_requirements = [
        ["ESC499Y1"],
        ["MIE429H1"],
        ["MIE451H1"],
        ["ECE352H1", "ECE419H1"],
    ]
    elective_requirements = [
        [
            "CSC310H1",
            "CSC413H1",
            "CSC401H1",
            "CSC420H1",
            "CSC485H1",
            "CSC486H1",
            "MIE424H1",
            "MIE457H1",
            "MIE566H1",
            "ECE352H1",
            "ECE419H1",
        ],
        [
            "CSC310H1",
            "CSC413H1",
            "CSC401H1",
            "CSC420H1",
            "CSC485H1",
            "CSC486H1",
            "MIE424H1",
            "MIE457H1",
            "MIE566H1",
            "ECE352H1",
            "ECE419H1",
        ],
    ]

    requirements = (core_requirements, elective_requirements)

    return Major(name=name, requirements=requirements)


def test_major_construction(major):
    # Check class construction
    assert major.name
    assert major.requirements


def test_major_contains(major):
    # Check __contains__
    assert "MIE451H1" in major, "CSC401H1 should be in " + major
    assert not "APS111H1" in major, "APS111H1 should not be in " + major


def test_major_progress(major):
    # Check Major completion
    # Check correct list
    correct_course_list = [
        "ESC499Y1",
        "MIE429H1",
        "MIE451H1",
        "ECE352H1",
        "CSC310H1",
        "CSC413H1",
    ]
    progress_list = major.check_progress(correct_course_list)
    for req in progress_list:
        assert req[1] == True, f"The Major requirement {req} should be fulfilled"

    # Check blank list
    incorrect_course_list1 = []
    progress_list = major.check_progress(incorrect_course_list1)
    for req in progress_list:
        assert req[1] == False, f"The Major requirement {req} should not be fulfilled"

    # Check incorrect list with course that fulfills multiple requirements
    incorrect_course_list2 = [
        "ESC499Y1",
        "MIE429H1",
        "MIE451H1",
        "ECE352H1",
        "CSC310H1",
    ]
    first_dupl_req = True
    progress_list = major.check_progress(incorrect_course_list2)
    for req in progress_list:
        if first_dupl_req and req[0] == [
            "CSC310H1",
            "CSC413H1",
            "CSC401H1",
            "CSC420H1",
            "CSC485H1",
            "CSC486H1",
            "MIE424H1",
            "MIE457H1",
            "MIE566H1",
            "ECE352H1",
            "ECE419H1",
        ]:
            assert req[1] == True, f"The Major requirement {req} should be fulfilled"
            first_dupl_req = False
        elif req[0] == [
            "CSC310H1",
            "CSC413H1",
            "CSC401H1",
            "CSC420H1",
            "CSC485H1",
            "CSC486H1",
            "MIE424H1",
            "MIE457H1",
            "MIE566H1",
            "ECE352H1",
            "ECE419H1",
        ]:
            assert (
                req[1] == False
            ), f"The Major requirement {req} should not be fulfilled"
        else:
            assert req[1] == True, f"The Major requirement {req} should be fulfilled"

    # assert not major.check_progress(
    #     incorrect_course_list2), "This course list should not fulfill major requirements"


def test_major_completion(major):
    # Check Major completion
    # Check correct list
    correct_course_list = [
        "ESC499Y1",
        "MIE429H1",
        "MIE451H1",
        "ECE352H1",
        "CSC310H1",
        "CSC413H1",
    ]
    assert major.check_completion(
        correct_course_list
    ), "This course list should fulfill major requirements"

    correct_course_list = [
        "ESC499Y1",
        "MIE429H1",
        "MIE451H1",
        "ECE352H1",
        "ECE419H1",
        "CSC413H1",
    ]
    assert major.check_completion(correct_course_list), (
        "This course list should fulfill major requirements"
        + "using core courses as electives"
    )

    # Check blank list
    incorrect_course_list1 = []
    assert not major.check_completion(
        incorrect_course_list1
    ), "This course list should not fulfill major requirements"

    # Check incorrect list with course that fulfills multiple requirements
    incorrect_course_list2 = [
        "ESC499Y1",
        "MIE429H1",
        "MIE451H1",
        "ECE352H1",
        "CSC310H1",
    ]
    assert not major.check_completion(
        incorrect_course_list2
    ), "This course list should not fulfill major requirements"
