class Course:
    """
        Class for representing and checking the requirements of a Course

        Attributes
        ----------------
        _id (str)                           - The MongoDB document ID
        Code (str)                          - The course code
        Name (str)                          - The course's name
        Division (str)                      - Which faculty/campus offers the course
        Course Description (str)            - The course's description
        Department (str)                    - The department that offers the course
        Pre-requisites (list)               - A list containing course codes that are pre-requisites for this course
        Course Level (str)                  - The course's level
        UTSC Breadth (list)                 - A list of which UTSC Breadth requirements this course satisfies
        APSC Electives (list)               - A list of which APSC elective requirements this course satisfies
        Campus (str)                        - The campus that offers this course
        Term (list)                         - A list containing the terms this course is offered e.g. ['Winter 2022']
        Activity (str)                      - An html string of the table element for this course
        Last updated (str)                  - A date string of the datetime this information was last updated
        Exclusion (list)                    - A list of course codes that cannot be taken with this course
        UTM Distribution (str)              - Which distribution at UTM offers this course
        Corequisite (list)                  - A list of course codes for courses that must be taken at the same time
        Recommended Preparation (list)      - A list of courses codes for courses that are recommended to take before this course
        Arts and Science Breadth (str)      - Which Arts and Sciences breadth requirements this course satisfies
        Arts and Science Distribution (str) - Which distribution in the Arts and Science Faculty requires this course
        Later term course details (str)     - A file path URL to the course that follows this course
        Course (str)                        - An HTML anchor tag for this course's dedicated page
        fase_available (bool)                - Boolean for whether or not FASE is available
        maybe_restricted (bool)              - Boolean value for whether or not enrollment for this course is restricted
        majors_outcomes (str)                - Major IDs for which this course satisfies a requirement
        minors_outcomes (str)                - Minor IDs for which this course satisfies a requirement
        ai_prereqs (str)                     - Not Sure tbh
    """

    def __init__(self, _id, code, name, division,
                 course_description, department, prerequisites,
                 course_level, utsc_breadth, apsc_electives,
                 campus, term, activity, last_updated, exclusion,
                 utm_distribution, corequisite, recommended_preparation,
                 artsci_breadth, artsci_distribution, later_term_course_details,
                 course, fase_available, maybe_restricted,
                 majors_outcomes, minors_outcomes, ai_prereqs):
        self._id = _id
        self.code = code
        self.name = name
        self.division = division
        self.course_description = course_description
        self.department = department
        self.prerequisites = prerequisites
        self.course_level = course_level
        self.utsc_breadth = utsc_breadth
        self.apsc_electives = apsc_electives
        self.campus = campus
        self.term = term
        self.activity = activity
        self.last_updated = last_updated
        self.exclusion = exclusion
        self.utm_distribution = utm_distribution
        self.corequisite = corequisite
        self.recommended_preparation = recommended_preparation
        self.artsci_breadth = artsci_breadth
        self.artsci_distribution = artsci_distribution
        self.later_term_course_details = later_term_course_details
        self.course = course
        self.fase_available = fase_available
        self.maybe_restricted = maybe_restricted
        self.majors_outcomes = majors_outcomes
        self.minors_outcomes = minors_outcomes
        self.ai_prereq = ai_prereqs

    def __str__(self) -> str:
        return self.name
