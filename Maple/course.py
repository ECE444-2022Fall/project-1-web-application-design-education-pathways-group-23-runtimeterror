
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

    def __init__(self, mongo_db_doc):

        required_fields = ['_id', 'Code', 'Name', 'Division',
                           'Course Description', 'Department',
                           'Pre-requisites', 'Course Level',
                           'UTSC Breadth', 'APSC Electives',
                           'Campus', 'Term', 'Activity',
                           'Last updated', 'Exclusion',
                           'UTM Distribution', 'Corequisite',
                           'Recommended Preparation',
                           'Arts and Science Breadth',
                           'Arts and Science Distribution',
                           'Later term course details',
                           'Course', 'FASEAvailable',
                           'MaybeRestricted', 'MajorsOutcomes',
                           'MinorsOutcomes', 'AIPreReqs'
                           ]

        for field in required_fields:
            if field not in mongo_db_doc:
                raise Exception(f'Field missing from mongo_db_doc: {field}')

        self._id = mongo_db_doc["_id"]
        self.code = mongo_db_doc["Code"]
        self.name = mongo_db_doc["Name"]
        self.division = mongo_db_doc["Division"]
        self.course_description = mongo_db_doc["Course Description"]
        self.department = mongo_db_doc["Department"]
        self.prerequisites = mongo_db_doc["Pre-requisites"]
        self.course_level = mongo_db_doc["Course Level"]
        self.utsc_breadth = mongo_db_doc["UTSC Breadth"]
        self.apsc_electives = mongo_db_doc["APSC Electives"]
        self.campus = mongo_db_doc["Campus"]
        self.term = mongo_db_doc["Term"]
        self.activity = mongo_db_doc["Activity"]
        self.last_updated = mongo_db_doc["Last updated"]
        self.exclusion = mongo_db_doc["Exclusion"]
        self.utm_distribution = mongo_db_doc["UTM Distribution"]
        self.corequisite = mongo_db_doc["Corequisite"]
        self.recommended_preparation = mongo_db_doc["Recommended Preparation"]
        self.artsci_breadth = mongo_db_doc["Arts and Science Breadth"]
        self.artsci_distribution = mongo_db_doc["Arts and Science Distribution"]
        self.later_term_course_details = mongo_db_doc["Later term course details"]
        self.course = mongo_db_doc["Course"]
        self.fase_available = mongo_db_doc["FASEAvailable"]
        self.maybe_restricted = mongo_db_doc["MaybeRestricted"]
        self.majors_outcomes = mongo_db_doc["MajorsOutcomes"]
        self.minors_outcomes = mongo_db_doc["MinorsOutcomes"]
        self.ai_prereq = mongo_db_doc["AIPreReqs"]

    def __str__(self) -> str:
        return self.name

    def get_course_weight(self) -> float:
        """
            Check whether a the Minor requirements are fulfilled given a course list

            Inputs
            ------------------

            Output
            ------------------
            float: return the course weight, either 0.5 or 1.0
        """

        # We assume that a course code with a Y is a full year course
        # and worth 1.0 credits, while H is a half year course and
        # worth 0.5 credits
        if(self.code[-2:-1] == "Y"):
            return 1.0
        elif(self.code[-2] == "H"):
            return 0.5

