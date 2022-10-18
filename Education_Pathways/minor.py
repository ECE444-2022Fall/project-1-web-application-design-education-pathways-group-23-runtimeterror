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

class Minor:
    """
        Class for representing and checking the requirements of a Minor

        Attributes
        ----------------
        name (str)          - The name of a Minor
        requirements (list) - A nested list of minor requirements, entries in the top level list represent "And" requirements
                              while entries in the nested lists represents "Or" requirements
    """

    def __init__(self, name, requirements):
        self.name = name
        self.requirements = requirements

    def __str__(self):
        return self.name

    def __contains__(self, course):
        """
            Check whether a course is listed as a requirement for this Minor

            Inputs
            ------------------
            course (str)    - The course code for the course being checked

            Output
            ------------------
            bool:   Whether the course is a requirement for this Minor
        """
        is_in_minor = any(course in requirement for requirement in self.requirements)
        return is_in_minor

    def check_minor_completion(self, course_list):
        """
            Check whether a the Minor requirements are fulfilled given a course list

            Inputs
            ------------------
            course_list (list)  - A List of Courses taken by a studen

            Output
            ------------------
            bool:   Whether the Minor requirements are fulfilled
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
    assert robotics_minor.check_minor_completion(correct_course_list), "This course list should fulfill minor requirements"

    # Check blank list
    incorrect_course_list1 = []
    assert not robotics_minor.check_minor_completion(incorrect_course_list1), "This course list should not fulfill minor requirements"

    # Check incorrect list with course that fulfills multiple requirements
    incorrect_course_list2 = ["APS360H1", "ECE358H1", "ROB311H1", "CSC311H1", "CHE507H1"]   
    assert not robotics_minor.check_minor_completion(incorrect_course_list2), "This course list should not fulfill minor requirements"

    print("Minor Class is working as expected")

if __name__ == "__main__":
    test_minor()
