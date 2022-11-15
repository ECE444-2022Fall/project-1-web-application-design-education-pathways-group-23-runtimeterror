import pytest
from student import Semester, Student
from degree import Major
from collections import OrderedDict

@pytest.fixture
def semester():
    # Test data
    name = "Fall 2022"
    status = "in progress"
    courses = ["ECE496Y1", "ECE444H1", "ECE454H1", "ECE552H1", "ECE568H1"]

    return Semester(name=name, status=status, courses=courses)

def test_semester_construction(semester):
    # Check class construction
    assert semester.name
    assert semester.status
    assert semester.courses
    
def test_semester_get_courses(semester):
    # Check get_courses
    courses = ["ECE496Y1", "ECE444H1", "ECE454H1", "ECE552H1", "ECE568H1"]
    assert semester.get_courses() == courses, "The incorrect courses were returned"

def test_semester_add_remove_courses(semester):
    # Check adding and removing courses
    semester.add_course("MIE451H1")
    semester.remove_course("ECE454H1")
    assert "MIE451H1" in semester, "This course should be in" + semester
    assert not "ECE454H1" in semester, "This course should not be in" + semester

@pytest.fixture
def student():
    # Test data
    major = "Electrical and Computer Engineering"
    year = 2024
    minors = ["Robotics and Mechatronics Minor"]

    name_1 = "Fall 2022"
    status_1 = "in progress"
    courses_1 = ["ECE496Y1", "ECE444H1", "ECE454H1", "ECE552H1", "ECE568H1"]
    f2022 = Semester(name=name_1, status=status_1, courses=courses_1)

    name_2 = "Winter 2021"
    status_2 = "complete"
    courses_2 = ["ECE396Y1", "ECE344H1", "ECE354H1", "ECE352H1", "ECE368H1"]
    w2021 = Semester(name=name_2, status=status_2, courses=courses_2)

    semesters = OrderedDict()
    semesters[name_2] = w2021
    semesters[name_1] = f2022
    
    return Student(major=major, year=year, minors=minors,
                           semesters=semesters)

def test_student_construction(student):
    # Check class construction
    assert student.major
    assert student.year
    assert student.minors
    assert student.semesters
    
def test_student_get_courses(student):
    # Check get_courses
    courses_1 = ["ECE496Y1", "ECE444H1", "ECE454H1", "ECE552H1", "ECE568H1"]
    courses_2 = ["ECE396Y1", "ECE344H1", "ECE354H1", "ECE352H1", "ECE368H1"]

    assert student.get_courses(status=["planned"]) == [], \
           "There should be no planned courses"
    assert student.get_courses(status=["in progress"]) == courses_1, \
           "The courses in progress should match courses_1"
    assert student.get_courses(status=["complete", "in progress"]) \
            == courses_2 + courses_1, \
           "The courses in progress should match the sum of course_2" \
           + "and courses_1"

def test_student_get_credits(student):
    # Check get_credits and calculate_credits()
    assert student.get_credits() == 3, "There should be 3 credits"

    student.calculate_credits()
    assert student.earned_credits == 6, "There should be 6 credits"
    assert student.planned_credits == 0, "There should be 0 credits"

def test_student_add_remove_minor(student):
    # Check adding and removing minors
    student.add_minor("Biomedical Minor")
    student.remove_minor("Robotics and Mechatronics Minor")
    assert student.has_minor("Biomedical Minor"), "Should have this minor"
    assert not student.has_minor("Robotics and Mechatronics Minor"), \
                                      "Should not have this minor"

def test_student_add_remove_semester(student):
    # Check adding and removing Semester
    student.add_semester("Winter 2022", "planned")
    student.remove_semester("Winter 2021")
    assert student.has_semester("Winter 2022"), "Should have this Semester"
    assert not student.has_semester("Winter 2021"), \
                                      "Should not have this Semester"

def test_student_course_swap(student):
    # Test course swapping
    student.swap_course("ECE568H1", ("Fall 2022", "Winter 2021"))
    assert not "ECE568H1" in student.get_semester("Fall 2022"), \
                "Course should not be in this Semester"
    assert "ECE568H1" in student.get_semester("Winter 2021"), \
                "Course should be in this Semester"

    student.swap_course("ECE396Y1", indices=(0, 1))
    assert not "ECE396Y1" in student.get_semester(index=0)
    assert "ECE396Y1" in student.get_semester(index=1)


def test_check_major_status():
    # Test Student
    major = "Test Major"
    year = 2023
    minors = [""]

    student = Student(major, year, minors)

    # Test Major
    name = "Test Major"
    core_requirements = [
        ["ESC499Y1"],
        ["MIE429H1"],
        ["MIE451H1"],
    ]
    elective_requirements = [
        ["ECE444H1"],
        ["ECE419H1"]
    ]
    requirements = (core_requirements, elective_requirements)

    major = Major(name=name, requirements=requirements)

    student.check_major_status(major)
    assert student.major_status == "Incomplete"

    name = "Fall 2021"
    status = "complete"
    courses = ["ESC499Y1", "ECE444H1", "MIE451H1", "ECE552H1", "ECE568H1"]
    student.add_semester(name=name, status=status, courses=courses)

    student.check_major_status(major)
    assert student.major_status == "Incomplete"

    name = "Fall 2022"
    status = "planned"
    courses = ["MIE429H1", "ECE424H1", "ECE526H1", "CSC413H1", "ECE419H1"]
    student.add_semester(name=name, status=status, courses=courses)
    
    student.check_major_status(major)
    assert student.major_status == "On-Track"

    student.get_semester("Fall 2022").status = "in progress"
    
    student.check_major_status(major)
    assert student.major_status == "Complete"