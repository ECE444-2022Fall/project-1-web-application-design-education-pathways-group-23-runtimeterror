
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
        FASEAvailable (bool)                - Boolean for whether or not FASE is available
        MaybeRestricted (bool)              - Boolean value for whether or not enrollment for this course is restricted
        MajorsOutcomes (str)                - Major IDs for which this course satisfies a requirement
        MinorsOutcomes (str)                - Minor IDs for which this course satisfies a requirement
        AIPreReqs (str)                     - Not Sure tbh
    """
    def __init__(self, name, prerequisites=[]):
        self.Name = name
        self.Pre_requisites = prerequisites
        pass
        
# CourseList = {"ECE444":Course("ECE444"),"CSC343":Course("CSC343")}

def prerequisite_checker(CourseName, CourseList):
    
    try:
        CourseObject = CourseList[CourseName]
        #  Trigger some Front End Visual
        return CourseObject.Pre_requisites #2 Cases: (1) [] = No Pre-Req, (2) [...] = Yes Pre-Req
    except:
        return False
        # raise("Missing Courses -- meant for dev only - do not push to prod")
    
    
def prerequisite_tester():
    # Test 1: No Course
    CourseList = {}
    assert(prerequisite_checker("ECE444", CourseList) == False)
    
    # Test 2: No Pre-Requisites
    CourseList = {"ECE444":Course("ECE444"),"CSC343":Course("CSC343")}
    assert(prerequisite_checker("ECE444", CourseList) == [])
    
    # Test 3: 1 Pre-Requisite
    CourseList = {"ECE444":Course("ECE444", ["ECE345"]),"CSC343":Course("CSC343", ["ECE301"])}
    assert(prerequisite_checker("ECE444", CourseList) == ["ECE345"])
    
    # Test 4: Multiple Pre-Requisites
    CourseList = {"ECE444":Course("ECE444", ["ECE345", "ECE361"]),"CSC343":Course("CSC343", ["ECE301"])}
    assert(prerequisite_checker("ECE444", CourseList) == ["ECE345", "ECE361"])
    
prerequisite_tester()