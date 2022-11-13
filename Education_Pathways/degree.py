from abc import ABC, abstractmethod
import config

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
        
    @classmethod
    def load_from_collection(cls, code):
        major_collection = config.db["majors"]
        major = list(major_collection.find({"code":code}))[0]
        major = cls(name=major["name"], requirements=(major["core_requirements"], major["elective_requirements"]))
        return major

    def serialize(self):
        """
            Returns a dictionary representation of major for jsonification purposes
        """
        return {
            "name" : self.name,
            "core_requirements" : self.requirements.core_requirements,
            "elective_requirements" :  self.requirements.elective_requirements
        }

    @classmethod
    def deserialize(cls, dict):
        major = cls(name=dict["name"], requirements=(dict["core_requirements"], dict["elective_requirements"]))
        return major

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

    @classmethod
    def load_from_collection(cls, code):
        minor_collection = config.db["minors"]
        minor = list(minor_collection.find({"code":code}))[0]
        minor = cls(name=minor["name"], requirements=minor["requirements"])
        return minor

    def serialize(self):
        """
            Returns a dictionary representation of minor for jsonification purposes
        """
        return {
            "name" : self.name,
            "requirements" : self.requirements
        }

    @classmethod
    def deserialize(cls, dict):
        minor = cls(name=dict["name"], requirements=dict["requirements"])
        return minor