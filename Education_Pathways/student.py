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

