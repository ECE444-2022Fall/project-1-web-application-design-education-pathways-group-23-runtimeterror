# using hard-coded data for testing purpose, should be fetch in database later on
engineering_minor_list = {
    'Artificial Intelligence Minor' : [],
    'Advanced Manufacturing Minor' : [],
    'Bioengineering Minor' : [],
    'Environmental Engineering Minor' : [],
    'Sustainable Energy Minor' : [],
    'Engineering Business Minor' : [],
    'Robotics and Mechatronics Minor' : [],
    'Biomedical Engineering Minor' : ["CHE353H1F", "BME331H1S", "BME440H1", "MIE439H1S", "BME530H1S", "BME499Y1Y", "BME498Y1Y"],
    'Nanoengineering Minor' : [],
    'Music Performance Minor' : [],
}

# Calcualting the percentage of minor fulfillment
def check_course_in_minor(course):
    minor = None
    for i in engineering_minor_list:
        if course in engineering_minor_list[i]:
            minor = i

    return minor

from abc import ABC, abstractmethod

class Degree(ABC):
    """
        Abstract base class for Degree Requirements (Majors and Minors)
    """
    def __init__(self, name: str, requirements):
        self.name = name
        self.requirements = requirements
        super().__init__()

    def __str__(self):
        return self.name

    @abstractmethod
    def __contains__(self, course) -> bool:
        pass

    @abstractmethod
    def check_completion(self, course_list) -> bool:
        pass

class Major(Degree):
    """
        Class for representing and checking the requirements of a Major

        Attributes
        ----------------
        name (str)              - The name of a Major
        requirements (tuple)    - First Entry: Core Requirements
                                - Second Entry: Elective Requirements 
    """

    class Requirements:
        """
            Class for representing the requirements of a Major

            Attributes
            ----------------
            core_requirements (list)        - A nested list of core requirements, entries in
                                              the top level list represent "And" requirements
                                              while entries in the nested lists represents "Or"
                                              requirements
            elective_requirements (list)    - A nested list of elective requirements, entries
                                              in the top level list represent "And" requirements
                                              while entries in the nested lists represents "Or" 
                                              requirements
        """
        def __init__(self, core_requirements: list, elective_requirements: list):
            self.core_requirements = core_requirements
            self.elective_requirements = elective_requirements

        def __contains__(self, course) -> bool:
            """
                Check whether a course fulfills a core or elective requirement
                Inputs
                ------------------
                course (str)    - The course code for the course being checked

                Output
                ------------------
                bool:   Whether the course fulfills a core or elective requirement
            """
            return any(course in requirement for requirement in self.core_requirements
                       + self.elective_requirements)

        def check_core(self, course_list) -> bool:
            """
                Check whether the core requirements are fulfilled given a course list

                Inputs
                ------------------
                course_list (list)  - A List of Courses taken by a student

                Output
                ------------------
                bool:   Whether the corerequirements are fulfilled
            """
            core_courses = []
            # Check all "And" Requirements in core requirements
            for requirement in self.core_requirements:
                if(set(requirement).isdisjoint(course_list)):
                    return False

                else:
                    eligible_courses = set(requirement) & set(course_list)
                    course = eligible_courses.pop()
                    core_courses.append(course)
                    course_list.remove(course)

            return True

        def check_elective(self, course_list):
            """
                Check whether the elective requirements are fulfilled given a course list

                Inputs
                ------------------
                course_list (list)  - A List of Courses taken by a student

                Output
                ------------------
                bool:   Whether the corerequirements are fulfilled
            """
            elective_courses = []
            # Check all "And" Requirements in elective requirements
            for requirement in self.elective_requirements:
                if(set(requirement).isdisjoint(course_list)):
                    return False

                else:
                    eligible_courses = set(requirement) & set(course_list)
                    course = eligible_courses.pop()
                    elective_courses.append(course)
                    course_list.remove(course)

            return True

    def __init__(self, name: str, requirements: tuple):
        requirements = self.Requirements(*requirements)
        super(Major, self).__init__(name, requirements)

    def __contains__(self, course) -> bool:
        """
            Check whether a course fulfills a requirement for this Major

            Inputs
            ------------------
            course (str)    - The course code for the course being checked

            Output
            ------------------
            bool:   Whether the course fulfills a requirement for this Major
        """
        return self.requirements.__contains__(course)

    def check_completion(self, course_list) -> bool:
        """
            Check whether the Major's requirements are fulfilled given a course list

            Inputs
            ------------------
            course_list (list)  - A List of Courses taken by a student

            Output
            ------------------
            bool:   Whether the Major's requirements are fulfilled
        """
        if(self.requirements.check_core(course_list)):
            if(self.requirements.check_elective(course_list)):
                return True

        return False
        

class Minor(Degree):
    """
        Class for representing and checking the requirements of a Minor

        Attributes
        ----------------
        name (str)          - The name of a Minor
        requirements (list) - A nested list of minor requirements, entries in the top level list represent "And" requirements
                              while entries in the nested lists represents "Or" requirements
    """

    def __init__(self, name: str, requirements: list):
        super(Minor, self).__init__(name, requirements)
    
    def __contains__(self, course) -> bool:
        """
            Check whether a course is listed as a requirement for this Minor

            Inputs
            ------------------
            course (str)    - The course code for the course being checked

            Output
            ------------------
            bool:   Whether the course is a requirement for this Minor
        """
        return any(course in requirement for requirement in self.requirements)

    def check_completion(self, course_list) -> bool:
        """
            Check whether the Minor's requirements are fulfilled given a course list

            Inputs
            ------------------
            course_list (list)  - A List of Courses taken by a student

            Output
            ------------------
            bool:   Whether the Minor's requirements are fulfilled
        """
        minor_courses = []
        # Check all "And" Requirements in Minor
        for requirement in self.requirements:
            if(set(requirement).isdisjoint(course_list)):
                return False

            else:
                # Fulfill the requirement with the first eligible course
                # The way this is designed, we need to sort requirements in
                # descending order of strictness
                eligible_courses = set(requirement) & set(course_list)
                course = eligible_courses.pop()
                minor_courses.append(course)
                course_list.remove(course)

        return True

# Unit Tests are in if __name__ = main until we've decided on a test suite
def test_minor():
    # Test data
    name = "Robotics and Mechatronics Minor"
    requirements = [
        ["APS360H1"],
        ["CSC263H1", "ECE345H1", "ECE358H1", "MIE335H1"],
        ["CSC384H1", "MIE369H1", "ROB311H1"],
        ["CSC311H1", "ECE421H1", "MIE424H1", "ROB313H1"],
        ["CHE507H1", "CSC401H1", "CHE507H1", "CSC401H1", "CSC420H1", "CSC413H1",
         "CSC485H1", "CSC486H1", "ECE368H1", "HPS345H1", "HPS346H1", "MIE368H1",
         "MIE451H1", "MIE457H1", "MIE562H1", "MIE566H1", "MSE403H1", "ROB501H1"],
        ["CHE507H1", "CSC401H1", "CHE507H1", "CSC401H1", "CSC420H1", "CSC413H1",
         "CSC485H1", "CSC486H1", "ECE368H1", "HPS345H1", "HPS346H1", "MIE368H1",
         "MIE451H1", "MIE457H1", "MIE562H1", "MIE566H1", "MSE403H1", "ROB501H1",
         "AER336H1", "BME595H1", "CHE322H1", "CSC343H1", "CSC412H1", "ECE344H1",
         "ECE353H1", "ECE356H1", "ECE367H1", "ECE411H1", "ECE419H1", "ECE431H1",
         "ECE444H1", "ECE454H1", "ECE470H1", "ECE516H1", "ECE532H1", "ECE557H1",
         "ECE568H1", "MAT336H1", "MAT389H1", "STA302H1", "STA410H1"]
    ]

    # Check class construction
    robotics_minor = Minor(name=name, requirements=requirements)
    assert robotics_minor.name
    assert robotics_minor.requirements

    # Check __contains__
    assert "CSC401H1" in robotics_minor, "CSC401H1 should be in " + robotics_minor
    assert not "APS111H1" in robotics_minor, "APS111H1 should not be in " + robotics_minor

    # Check minor completion
    # Check correct list
    correct_course_list = ["APS360H1", "ECE358H1", "ROB311H1", "CSC311H1", "CSC485H1", "CHE322H1"]
    assert robotics_minor.check_completion(correct_course_list), "This course list should fulfill minor requirements"

    # Check blank list
    incorrect_course_list1 = []
    assert not robotics_minor.check_completion(incorrect_course_list1), "This course list should not fulfill minor requirements"

    # Check incorrect list with course that fulfills multiple requirements
    incorrect_course_list2 = ["APS360H1", "ECE358H1", "ROB311H1", "CSC311H1", "CHE507H1"]   
    assert not robotics_minor.check_completion(incorrect_course_list2), "This course list should not fulfill minor requirements"

    print("Minor Class is working as expected")

# Unit Tests are in if __name__ = main until we've decided on a test suite
def test_major():
    # Test data
    name = "Engineering Science - Machine Intelligence"
    core_requirements = [
        ["ESC499Y1"],
        ["MIE429H1"],
        ["MIE451H1"],
        ["ECE352H1","ECE419H1"],
    ]
    elective_requirements = [
        ["CSC310H1", "CSC413H1", "CSC401H1", "CSC420H1", "CSC485H1", "CSC486H1",
         "MIE424H1", "MIE457H1", "MIE566H1","ECE352H1","ECE419H1"],
         ["CSC310H1", "CSC413H1", "CSC401H1", "CSC420H1", "CSC485H1", "CSC486H1",
         "MIE424H1", "MIE457H1", "MIE566H1","ECE352H1","ECE419H1"]
    ]

    requirements = (core_requirements, elective_requirements)

    # Check class construction
    engsci = Major(name=name, requirements=requirements)
    assert engsci.name
    assert engsci.requirements

    # Check __contains__
    assert "MIE451H1" in engsci, "CSC401H1 should be in " + engsci
    assert not "APS111H1" in engsci, "APS111H1 should not be in " + engsci

    # Check Major completion
    # Check correct list
    correct_course_list = ["ESC499Y1", "MIE429H1", "MIE451H1", "ECE352H1", "CSC310H1", "CSC413H1"]
    assert engsci.check_completion(correct_course_list), "This course list should fulfill major requirements"
    
    correct_course_list = ["ESC499Y1", "MIE429H1", "MIE451H1", "ECE352H1", "ECE419H1", "CSC413H1"]
    assert engsci.check_completion(correct_course_list), "This course list should fulfill major requirements" \
                                                         + "using core courses as electives"

    # Check blank list
    incorrect_course_list1 = []
    assert not engsci.check_completion(incorrect_course_list1), "This course list should not fulfill minor requirements"

    # Check incorrect list with course that fulfills multiple requirements
    incorrect_course_list2 = ["ESC499Y1", "MIE429H1", "MIE451H1", "ECE352H1", "CSC310H1"]   
    assert not engsci.check_completion(incorrect_course_list2), "This course list should not fulfill minor requirements"

    print("Major Class is working as expected")

if __name__ == "__main__":
    test_minor()
    test_major()
