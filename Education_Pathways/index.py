# this is the flask core

import config
from flask import Flask, send_from_directory, jsonify, request, session
from flask_restful import Api, Resource, reqparse

import os
from datetime import date

# import pandas as pd
# df = pd.read_csv("resources/courses.csv")

from student import Student
from search import SearchCourse, search_course
from degree import Major, Minor
import config

app = Flask(__name__, static_folder='frontend/build')
app.config['SECRET_KEY'] = "Totally a secret"
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

config.init_app(app)
config.init_db()
config.init_cors(app)

class ShowCourse(Resource):
    def get(self):
        code = request.args.get('code')
        courses = search_course(code, "")
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {code} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 500
            return resp

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True)
        data = parser.parse_args()
        code = data['code']
        courses = search_course(code, "")
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {code} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 500
            return resp


# API Endpoints
rest_api = Api(app)
rest_api.add_resource(SearchCourse, '/api/search')
rest_api.add_resource(ShowCourse, '/course/details')


# Semester Viewer API
# SV API for loading student information
@app.route("/api/load_student", methods=["GET", "POST"])
def load_student():
    if(session.get("student")):
        student = Student.deserialize(session.get("student"))
        resp = jsonify(student.serialize())
        resp.status_code = 200
        
    else:
        resp = jsonify({})
        resp.status_code = 204

    return resp

# SV API for creating new student
@app.route("/api/create_student", methods=["POST"])
def create_student():
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
@app.route("/api/get_course_category", methods=["POST"])
def get_course_category():
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
@app.route("/api/get_course_categories", methods=["GET"])
def get_course_categories():
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

    return major
    
def get_minor():
    # Temporarily hardcoded
    if(session.get("minor")):
        minor = Minor.deserialize(session["minor"])
    else:
        minor_code = "AEMINBUS"
        minor = Minor.load_from_collection(minor_code)

    return minor

# SV API for adding a course
@app.route("/api/add_course", methods=["POST"])
def add_course():
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
@app.route("/api/remove_course", methods=["POST"])
def remove_course():
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
@app.route("/api/swap_semester", methods=["POST"])
def swap_semester():
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

@app.route("/", defaults={'path': ''})

@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, extra_files=['app.py', 'controller.py', 'model.py'])
    app.run(threaded=True, port=5000)
    # with open("test.json") as f:
    #     data = json.load(f)
    # for i in range(75):
    #     i = str(i)
    #     Course(name=data["name"][i], code=data["code"][i], description=data["description"][i], prereq=data["prereq"][i], coreq=data["coreq"][i], exclusion=data["exclusion"][i]).save()
