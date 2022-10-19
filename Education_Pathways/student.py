from collections import OrderedDict

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

    def __init__(self, name: str, status: str, courses: list):
        self.name = name
        self.status = status
        self.courses = courses

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.courses)

    def __contains__(self, course):
        return course in self.courses

    def add_course(self, course):
        """
            Adds a course to a Semester

            Inputs
            ------------------
            course  - The course to add to the Semester
        """
        self.courses.append(course)

    def remove_course(self, course):
        """
            Removes a course from a Semester

            Inputs
            ------------------
            course  - The course to remove from the Semester
        """
        self.courses.remove(course)

    def set_status(self, status):
        """
            Change status of a Semester

            Inputs
            ------------------
            status (str)    - The status ("complete", "in progress", "planned")
                              to change the semester to
        """
        self.status = status

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
        major ()                - What a student is majoring in
        year (int)              - What year a student is in
        minors (list)           - A list of minors (using the Minor class)
                                  a student is interested in
        semesters (OrderedDict) - A Dictionary of Semesters
                        
    """
    def __init__(self, major, year: int, minors: list, semesters: OrderedDict=OrderedDict()):
        self.major = major
        self.year = year
        self.minors = minors
        self.semesters = semesters

    def set_major(self, major):
        """
            Change the major of a student

            Inputs
            ------------------
            major (Major)   - The major to switch to
        """
        self.major = major

    def add_minor(self, minor):
        """
            Adds a minor to a student

            Inputs
            ------------------
            minor (Minor)   - The minor to add
        """
        self.minors.append(minor)
    
    def remove_minor(self, minor):
        """
            Removes a minor from a student

            Inputs
            ------------------
            minor (Minor)   - The minor to add
        """
        self.minors.remove(minor)

    def has_minor(self, minor) -> bool:
        """
            Check if a Student has a specific minor

            Inputs
            ------------------
            minor (Minor)   - The minor to check

            Output
            ------------------
            bool: Whether the Student has the specified minor
        """
        return minor in self.minors


    def get_semester(self, name: str):
        """
            Retrieves a Semester given a name

            Inputs
            ------------------
            name (str)  - The name of the Semester

            Output
            ------------------
            Semester: The corresponding Semester
        """
        return self.semesters[name]

    def add_semester(self, name: str, status: str, courses: list=[]):
        """
            Adds a Semester given a name and status

            Inputs
            ------------------
            name (str)      - The name of the Semester
            status (str)    - The status of the Semester
            courses (list)  - (Optional) A list of courses taken in the Semester
        """
        self.semesters[name] = Semester(name=name, status=status, courses=courses)

    def remove_semester(self, name):
        """
            Removes a Semester of a given name

            Inputs
            ------------------
            name (str)      - The name of the Semester
        """
        self.semesters.pop(name)

    def has_semester(self, name):
        """
            Check if a Student has a specific Semester

            Inputs
            ------------------
            name (str)  - The name of the Semester to check

            Output
            ------------------
            bool: Whether the Student has the specified Semester
        """
        return name in self.semesters.keys()
    
    def get_courses(self, status=["complete", "in progress", "planned"]) -> list:
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

        for semester in self.semesters.values():
            if(semester.status in status):
                courses += semester.get_courses()

        return courses

    def swap_course(self, course, name_1, name_2):
        """
            Swaps a course from one Semester to Another

            Inputs
            ------------------
            course  - The course to swap
            name_1  - The name of the Semester the course is being taken from
            name_2  - The name of the Semester the course is being swapped to
        """
        self.semesters[name_1].remove_course(course)
        self.semesters[name_2].add_course(course)



    def get_credits(self, status=["complete"]) -> float:
        """
            Returns a number of credits from applicable Semesters

            Inputs
            ------------------
            status (list) - Specifies which status Semesters credits should be
                            tallied from
                            Defaults to including "complete" Semesters
            Output
            ------------------
            credits (float) - The number of credits earned in applicable Semesters
        """
        credits = 0

        # Get unique courses from applicable Semesters
        courses = set(self.get_courses(status=status))
        for course in courses:
            # Assume H courses are weighted 0.5 credits and
            # Y courses are weighted 1.0 credits
            # Implementation of weighting may be moved to the Course
            # Class once that is complete

            if(course[-2:-1] == "Y"):
                credits += 1.0
            elif(course[-2:-1] == "H"):
                credits += 0.5

        return credits


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

    # Check adding and removing courses
    f2022.add_course("MIE451H1")
    f2022.remove_course("ECE454H1")
    assert "MIE451H1" in f2022, "This course should be in" + f2022
    assert not "ECE454H1" in f2022, "This course should not be in" + f2022


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
    courses_2 = ["ECE396Y1", "ECE344H1", "ECE354H1", "ECE352H1", "ECE368H1"]
    w2021 = Semester(name=name_2, status=status_2, courses=courses_2)

    semesters = OrderedDict()
    semesters[name_2] = w2021
    semesters[name_1] = f2022
    

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

    # Check get_credits
    assert test_student.get_credits() == 3, "There should be 3 credits"

    # Check adding and removing Semesters and minors
    test_student.add_minor("Biomedical Minor")
    test_student.remove_minor("Robotics and Mechatronics Minor")
    assert test_student.has_minor("Biomedical Minor"), "Should have this minor"
    assert not test_student.has_minor("Robotics and Mechatronics Minor"), \
                                      "Should not have this minor"

    test_student.add_semester("Winter 2022", "planned")
    test_student.remove_semester("Winter 2021")
    assert test_student.has_semester("Winter 2022"), "Should have this Semester"
    assert not test_student.has_semester("Winter 2021"), \
                                      "Should not have this Semester"

    # Test course swapping
    test_student.swap_course("ECE568H1", "Fall 2022", "Winter 2022")
    assert not "ECE568H1" in test_student.get_semester("Fall 2022"), \
                "Course should not be in this Semester"
    assert "ECE568H1" in test_student.get_semester("Winter 2022")

    print("Student Class is working as expected")

if __name__ == "__main__":
    test_semester()
    test_student()
