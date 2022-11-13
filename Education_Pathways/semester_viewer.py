from datetime import date

from flask import jsonify, session
from flask_restful import Resource, reqparse

import config
from student import Student
from degree import Major, Minor

# Semester Viewer API
# SV API for loading student information
class LoadStudent(Resource):
    def get(self):
        if(session.get("student")):
            student = Student.deserialize(session.get("student"))
            resp = jsonify(student.serialize())
            resp.status_code = 200
            
        else:
            resp = jsonify({})
            resp.status_code = 204

        return resp

# SV API for creating new student
class CreateStudent(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('major', required=True)
        parser.add_argument('year', required=True)
        data = parser.parse_args()

        major = data['major']
        year = int(data["year"])

        student = Student(major, year)
        
        for i in range(year-4, year):
            if(i + 1 < date.today().year or (i < date.today().year and 4 < date.today().month)):
                status = ["complete"]*2
            elif(i > date.today().year or (i + 1 > date.today().year and 9 > date.today().month)):
                status = ["planned"]*2
            else:
                if(i == date.today().year):
                    status = ["in progress", "planned"]
                else:
                    status = ["complete", "in progress"]

            semester = "Fall {}".format(i)
            student.add_semester(semester, status[0])

            semester = "Winter {}".format(i+1)
            student.add_semester(semester, status[1])
            
        categories = [[] for _ in range(8)]

        session["student"] = student.serialize()
        session["categories"] = categories

        resp = jsonify(student.serialize())
        resp.status_code = 200
        return resp

# SV API for checking course category
class GetCourseCategory(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course', required=True)
        data = parser.parse_args()

        course = data['course']

        if(session.get("student")):
            student = Student.deserialize(session["student"])

            # Check if course code is valid
            if(config.course_collection.count_documents({"Code": course}, limit = 1) != 0):
                major = get_major()
                minor = get_minor()


                if(any(course in requirement for requirement in major.requirements.core_requirements)):
                    category = "core"
                elif(any(course in requirement for requirement in major.requirements.elective_requirements)):
                    category = "elective"
                elif(course in minor):
                    category = "minor"
                else:
                    category = "extra"

                resp = jsonify({"category": category})
                resp.status_code = 200

            else:
                resp = jsonify({})
                resp.status_code = 204
        
        else:
            resp = jsonify({})
            resp.status_code = 400

        return resp

# SV API for checking multiple course categories
class GetCourseCategories(Resource):
    def get(self):
        if(session.get("categories")):
            resp = jsonify({"categories": session["categories"]})
            resp.status_code = 200

        elif(session.get("student")):
            student = Student.deserialize(session["student"])

            categories = []

            major = get_major()
            minor = get_minor()

            for semester in student.semesters.values():
                semester_categories = []
                for course in semester.get_courses():
                    if(any(course in requirement for requirement in major.requirements.core_requirements)):
                        category = "core"
                    elif(any(course in requirement for requirement in major.requirements.elective_requirements)):
                        category = "elective"
                    elif(course in minor):
                        category = "minor"
                    else:
                        category = "extra"
                    
                    semester_categories.append(category)

                categories.append(semester_categories)
            
            session["categories"] = categories

            resp = jsonify({"categories": categories})
            resp.status_code = 200
        
        else:
            resp = jsonify({})
            resp.status_code = 400

        return resp
    
def get_major():
    # Temporarily hardcoded
    if(session.get("major")):
        major = Major.deserialize(session["major"])
    else:
        major_code = "AEESCBASEL"
        major = Major.load_from_collection(major_code)
        session["major"] = major.serialize()

    return major
    
def get_minor():
    # Temporarily hardcoded
    if(session.get("minor")):
        minor = Minor.deserialize(session["minor"])
    else:
        minor_code = "AEMINBUS"
        minor = Minor.load_from_collection(minor_code)
        session["minor"] = minor.serialize()

    return minor

# SV API for adding a course
class AddCourse(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('semester', required=True)
        parser.add_argument('course', required=True)
        parser.add_argument('category', required=True)
        data = parser.parse_args()

        course = data['course']
        semester = data["semester"]
        category = data["category"]

        if(session.get("student")):
            student = Student.deserialize(session["student"])
            student.get_semester(index=int(semester)).add_course(course)
            session["categories"][int(semester)].append(category)
            student.calculate_credits()
            session["student"] = student.serialize()


            resp = jsonify(student.serialize())
            resp.status_code = 200
        
        else:
            resp = jsonify({})
            resp.status_code = 400

        return resp

# SV API for removing a course
class RemoveCourse(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('semester', required=True)
        parser.add_argument('course', required=True)
        data = parser.parse_args()

        course = data['course']
        semester = data["semester"]

        if(session.get("student")):
            student = Student.deserialize(session["student"])

            index = student.get_semester(index=int(semester)).get_courses().index(course)
            del session["categories"][int(semester)][index]

            student.get_semester(index=int(semester)).remove_course(course)
            student.calculate_credits()
            session["student"] = student.serialize()
            
            resp = jsonify(student.serialize())
            resp.status_code = 200
        
        else:
            resp = jsonify({})
            resp.status_code = 400

        return resp

# SV API for swapping semesters for a course
class SwapSemester(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course', required=True)
        parser.add_argument('source_semester', required=True)
        parser.add_argument('target_semester', required=True)
        data = parser.parse_args()

        course = data["course"]
        source_semester = int(data['source_semester'])
        target_semester = int(data['target_semester'])

        if(session.get("student")):
            student = Student.deserialize(session["student"])

            
            index = student.get_semester(index=int(source_semester)).get_courses().index(course)
            category = session["categories"][int(source_semester)][index]
            del session["categories"][int(source_semester)][index]
            session["categories"][int(target_semester)].append(category)

            student.swap_course(course, indices=(source_semester, target_semester))
            student.calculate_credits()
            session["student"] = student.serialize()
            
            resp = jsonify(student.serialize())
            resp.status_code = 200
        
        else:
            resp = jsonify({})
            resp.status_code = 400

        return resp