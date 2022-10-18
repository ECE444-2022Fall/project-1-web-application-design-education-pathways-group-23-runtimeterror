class Semester:
    """
        Class for storing the name, status, and courses of a Semester

        Attributes
        ----------------
        name (str)      - The Semester name (ex. "Fall 2022")
        status (str)    - The status ("complete", "in progress", "planned")
                          of the Semester
        courses (list)  - The courses that a student has taken, is taking
                          or plans to take that Semester
    """

    def __init__(self, name, status, courses):
        self.name = name
        self.status = status
        self.courses = courses

    def __str__(self):
        return self.name

    def __contains__(self, course):
        return course in self.courses

    def get_courses(self):
        """
            Returns a list of courses for a given Semester
        """
        return self.courses

class Student:
    """
        Class for storing the major, year, minors, and courses of a student

        Attributes
        ----------------
        major (str)     - What a student is majoring in
        year (int)      - What year a student is in
        minors (list)   - A list of minors (using the Minor class) a student is
                          interested in
        semesters (list)  - A nested list of Semesters
                        
    """
    def __init__(self, major, year, minors, semesters):
        self.major = major
        self.year = year
        self.minors = minors
        self.semesters = semesters

    def get_courses(self, status=["complete", "in progress", "planned"]):
        """
            Returns a list of courses from applicable Semesters

            Inputs
            ------------------
            status (list) - Specifies which status Semesters courses should be
                            retrieved from
                            Defaults to including Semesters of all statuses
            Output
            ------------------
            courses (list)  - A list of courses from applicable Semesters
        """
        courses = []

        for semester in self.semesters:
            if(semester.status in status):
                courses += semester.get_courses()

        return courses

# Unit Tests are in if __name__ = main until we've decided on a test suite
def test_semester():
    # Test data
    name = "Fall 2022"
    status = "in progress"
    courses = ["ECE496Y1", "ECE444H1", "ECE454H1", "ECE552H1", "ECE568H1"]

    # Check class construction
    f2022 = Semester(name=name, status=status, courses=courses)
    assert f2022.name
    assert f2022.status
    assert f2022.courses
    
    # Check get_courses
    assert f2022.get_courses() == courses, "The incorrect courses were returned"

    print("Semester Class is working as expected")

# Unit Tests are in if __name__ = main until we've decided on a test suite
def test_student():
    # Test data
    major = "Electrical and Computer Engineering"
    year = 4
    minors = ["Robotics and Mechatronics Minor"]

    name_1 = "Fall 2022"
    status_1 = "in progress"
    courses_1 = ["ECE496Y1", "ECE444H1", "ECE454H1", "ECE552H1", "ECE568H1"]
    f2022 = Semester(name=name_1, status=status_1, courses=courses_1)

    name_2 = "Winter 2021"
    status_2 = "complete"
    courses_2 = ["ECE496Y1", "ECE444H1", "ECE454H1", "ECE552H1", "ECE568H1"]
    w2021 = Semester(name=name_2, status=status_2, courses=courses_2)
    semesters = [w2021, f2022]
    

    # Check class construction
    test_student = Student(major=major, year=year, minors=minors,
                           semesters=semesters)
    assert test_student.major
    assert test_student.year
    assert test_student.minors
    assert test_student.semesters
    
    # Check get_courses
    assert test_student.get_courses(status=["planned"]) == [], \
           "There should be no planned courses"
    assert test_student.get_courses(status=["in progress"]) == courses_1, \
           "The courses in progress should match courses_1"
    assert test_student.get_courses(status=["complete", "in progress"]) \
            == courses_2 + courses_1, \
           "The courses in progress should match the sum of course_2" \
           + "and courses_1"

    print("Student Class is working as expected")

if __name__ == "__main__":
    test_semester()
    test_student()
