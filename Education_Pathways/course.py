
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


def test_course():

    # Test data
    mongodb_document_data = {"_id": {"$oid": "634f3057118119f6a8fcf71c"}, "Code": "ENGB29H3", "Name": "Shakespeare and Film", "Division": "University of Toronto Scarborough", "Course Description": "The history of Shakespeare and (on) film is long, illustriousŸ??and prolific: there have been at least 400 film and television adaptations and appropriations of Shakespeare over the past 120 years, from all over the world. But how and why do different film versions adapt Shakespeare? What are the implications of transposing a play by Shakespeare to a different country, era, or even language? What might these films reveal, illuminate, underscore, or re-imagine about Shakespeare, and why? In this course, we will explore several different Shakespearean adaptations together with the plays they adapt or appropriate. We will think carefully about the politics of adaptation and appropriation; about the global contexts and place of Shakespeare; and about the role of race, gender, sexuality, disability, empire and colonialism in our reception of Shakespeare on, and in, film.Pre-1900 course.", "Department": "English (UTSC)", "Pre-requisites": "['ENGA11H3', 'ENGA10H3', 'ENGB70H3']", "Course Level": {
        "$numberInt": "2"}, "UTSC Breadth": "Arts, Literature & Language", "APSC Electives": "Complementary Studies", "Campus": "Scarborough", "Term": "['2022 Winter']", "Activity": "['<table class=\"uif-tableCollectionLayout\" id=\"u172\">\\n<thead>\\n<tr>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c1_span\">\\n<label for=\"\" id=\"u202_c1\">\\r\\nActivity\\r\\n</label>\\n</span>\\n</th>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c2_span\">\\n<label for=\"\" id=\"u202_c2\">\\r\\nDay and Time\\r\\n</label>\\n</span>\\n</th>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c3_span\">\\n<label for=\"\" id=\"u202_c3\">\\r\\nInstructor\\r\\n</label>\\n</span>\\n</th>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c4_span\">\\n<label for=\"\" id=\"u202_c4\">\\r\\nLocation\\r\\n</label>\\n</span>\\n</th>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c5_span\">\\n<label for=\"\" id=\"u202_c5\">\\r\\nClass Size\\r\\n</label>\\n</span>\\n</th>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c6_span\">\\n<label for=\"\" id=\"u202_c6\">\\r\\nCurrent Enrolment\\r\\n</label>\\n</span>\\n</th>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c7_span\">\\n<label for=\"\" id=\"u202_c7\">\\r\\nOption to Waitlist\\r\\n</label>\\n</span>\\n</th>\\n<th class=\"infoline\" colspan=\"1\" rowspan=\"1\" scope=\"col\">\\n<span class=\"infoline\" id=\"u202_c8_span\">\\n<label for=\"\" id=\"u202_c8\">\\r\\nDelivery Mode\\r\\n</label>\\n</span>\\n</th>\\n</tr>\\n</thead>\\n<tbody>\\n<tr>\\n<td class=\"uif-field\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field\" id=\"u245_line0\">\\n<span id=\"u245_line0\">\\r\\nLec 01\\r\\n</span>\\n<!-- placeholder for dynamic field markers -->\\n<span id=\"u245_line0_markers\"></span>\\n<span id=\"u245_line0_info_message\"></span>\\n</div>\\n</td>\\n<td class=\"uif-field\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field\" id=\"u254_line0\">\\n<span id=\"u254_line0\">\\r\\nMONDAY 11:00-14:00 <br/>\\n</span>\\n<!-- placeholder for dynamic field markers -->\\n<span id=\"u254_line0_markers\"></span>\\n<span id=\"u254_line0_info_message\"></span>\\n</div>\\n</td>\\n<td class=\"uif-field\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field\" id=\"u263_line0\">\\n<span id=\"u263_line0\">\\r\\nU Chakravarty <br/>\\n</span>\\n<!-- placeholder for dynamic field markers -->\\n<span id=\"u263_line0_markers\"></span>\\n<span id=\"u263_line0_info_message\"></span>\\n</div>\\n</td>\\n<td class=\"uif-field\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field\" id=\"u272_line0\">\\n<span id=\"u272_line0\">\\r\\nSW 128 <br/>\\n</span>\\n<!-- placeholder for dynamic field markers -->\\n<span id=\"u272_line0_markers\"></span>\\n<span id=\"u272_line0_info_message\"></span>\\n</div>\\n</td>\\n<td class=\"uif-field\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field\" id=\"u281_line0\">\\n<span id=\"u281_line0\">\\r\\n100\\r\\n</span>\\n<!-- placeholder for dynamic field markers -->\\n<span id=\"u281_line0_markers\"></span>\\n<span id=\"u281_line0_info_message\"></span>\\n</div>\\n</td>\\n<td class=\"uif-field\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field\" id=\"u290_line0\">\\n<span id=\"u290_line0\">\\r\\n3\\r\\n</span>\\n<!-- placeholder for dynamic field markers -->\\n<span id=\"u290_line0_markers\"></span>\\n<span id=\"u290_line0_info_message\"></span>\\n</div>\\n</td>\\n<td class=\"uif-field uif-fieldGroup uif-horizontalFieldGroup\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field uif-fieldGroup uif-horizontalFieldGroup\" data-group=\"u302_line0\" data-parent=\"Activity-details\" id=\"u299_line0\">\\n<fieldset aria-labelledby=\"u299_line0_label\" id=\"u299_line0_fieldset\">\\n<legend style=\"display: none\"></legend>\\n<div class=\"uif-group uif-boxGroup uif-horizontalBoxGroup\" data-parent=\"u299_line0\" id=\"u302_line0\">\\n<div class=\"uif-validationMessages uif-groupValidationMessages\" data-messagesfor=\"u302_line0\" id=\"u304_line0\" style=\"display: none;\">\\n</div>\\n<div class=\"uif-boxLayout uif-horizontalBoxLayout clearfix\" id=\"u303_line0_boxLayout\">\\n<div class=\"uif-field uif-imageField uif-boxLayoutHorizontalItem uif-boxLayoutHorizontalItem\" id=\"u305_line0\" style=\";\">\\n<img alt=\"\" class=\"uif-image\" id=\"u308_line0\" src=\"../courseSearch/images/checkmark.png\"/>\\n</div>\\n<input data-for=\"u305_line0\" data-role=\"script\" name=\"script\" type=\"hidden\" value=\"createTooltip(\\'u305_line0\\', \\'Students have the option to waitlist for this course if filled\\', {position:\\'top\\',align:\\'left\\',alwaysVisible:false,tail:{ align:\\'left\\', hidden: false },themePath:\\'../krad/plugins/tooltip/jquerybubblepopup-theme/\\',themeName:\\'black\\',selectable:true}, true, false);\">\\n<input data-for=\"u305_line0\" data-role=\"script\" name=\"script\" type=\"hidden\" value=\"addAttribute(\\'u305_line0\\', \\'class\\', \\'uif-tooltip\\', true);\">\\n</input></input></div>\\n</div>\\n<input data-for=\"u302_line0\" data-role=\"dataScript\" name=\"script\" type=\"hidden\" value=\"jQuery(\\'#u302_line0\\').data(\\'validationMessages\\', {summarize:true,displayMessages:true,collapseFieldMessages:true,displayLabel:true,hasOwnMessages:false,pageLevel:false,forceShow:true,sections:[],order:[],serverErrors:[],serverWarnings:[],serverInfo:[]});\">\\n</input></fieldset>\\n</div>\\n</td>\\n<td class=\"uif-field\" colspan=\"1\" role=\"presentation\" rowspan=\"1\">\\n<div class=\"uif-field\" id=\"u314_line0\">\\n<span id=\"u314_line0\">\\r\\nINPER\\r\\n</span>\\n<!-- placeholder for dynamic field markers -->\\n<span id=\"u314_line0_markers\"></span>\\n<span id=\"u314_line0_info_message\"></span>\\n</div>\\n</td>\\n</tr>\\n</tbody>\\n</table>']", "Last updated": "2021-07-06 13:15:03.0", "Exclusion": "[]", "UTM Distribution": "", "Corequisite": "[]", "Recommended Preparation": "[]", "Arts and Science Breadth": "", "Arts and Science Distribution": "", "Later term course details": "", "Course": "<a href=/course/ENGB29H3>ENGB29H3</a>", "FASEAvailable": "False", "MaybeRestricted": "False", "MajorsOutcomes": "[]", "MinorsOutcomes": "[]", "AIPreReqs": "[]"}

    # Check class construction
    ENGB29H3_course = Course(mongodb_document_data)
    assert ENGB29H3_course._id
    assert ENGB29H3_course.code
    assert ENGB29H3_course.name
    assert ENGB29H3_course.division
    assert ENGB29H3_course.course_description
    assert ENGB29H3_course.department
    assert ENGB29H3_course.prerequisites
    assert ENGB29H3_course.course_level
    assert ENGB29H3_course.utsc_breadth
    assert ENGB29H3_course.apsc_electives
    assert ENGB29H3_course.campus
    assert ENGB29H3_course.term
    assert ENGB29H3_course.activity
    assert ENGB29H3_course.last_updated
    assert ENGB29H3_course.exclusion
    assert ENGB29H3_course.corequisite
    assert ENGB29H3_course.recommended_preparation
    assert ENGB29H3_course.course
    assert ENGB29H3_course.fase_available
    assert ENGB29H3_course.maybe_restricted
    assert ENGB29H3_course.majors_outcomes
    assert ENGB29H3_course.minors_outcomes
    assert ENGB29H3_course.ai_prereq

    # Check get_course_weight
    assert ENGB29H3_course.get_course_weight() == 0.5

    print("Minor Class is working as expected")


if __name__ == "__main__":
    test_course()
