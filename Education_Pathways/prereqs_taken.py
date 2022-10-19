from pickle import FALSE
from student import Student
from prerequisite_checker import prerequisite_checker, Course

def prerequisite_match (courseName, courseList, student):
    prerequisites = set(prerequisite_checker(courseName, courseList))
    valid_courses = set(student.get_courses())

    return prerequisites.difference(valid_courses)

def unit_tests():
    student = Student() #expect courses to be populated
    courseList = {"ECE444":Course("ECE444"),"CSC343":Course("CSC343")}

    # Test 1: Student has taken prerequisites
    assert(prerequisite_match('ECE444', courseList, student) == []) #

    # Test 1: Student hasn't taken prerequisites
    assert(prerequisite_match('ECE1151', courseList, student) == ['ECE1121']) #To be completed


