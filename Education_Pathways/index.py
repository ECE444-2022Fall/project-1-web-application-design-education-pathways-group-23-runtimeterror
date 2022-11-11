# this is the flask core

import re
import config
from flask import Flask, send_from_directory, jsonify, request
from pymongo import MongoClient
from flask_restful import Api, Resource, reqparse

import os
from datetime import date

# import pandas as pd
# df = pd.read_csv("resources/courses.csv")

from student import Student
import config

app = Flask(__name__, static_folder='frontend/build')
app.config['SECRET_KEY'] = "Totally a secret"
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = f"mongodb+srv://admin:{os.environ.get('MONGO_PASS')}@cluster0.o7bvcw3.mongodb.net/test"

# Create a connection using MongoClient.
client = MongoClient(CONNECTION_STRING)

# Grab and store the test database and the course collection
db = client['test']
course_collection = db["courses"]

config.init_app(app)
config.init_db(app)
config.init_cors(app)

# route functions
def search_course_by_code(s):
    # return all the courses whose course code contains the str s
    regx = re.compile(f'.*{s.upper()}.*', re.IGNORECASE)
    course_ids = list(course_collection.find({'Code': regx}))
    print(len(course_ids))
    if len(course_ids) == 0:
        return []
    if len(course_ids) > 10:
        course_ids = course_ids[:10]
    res = []
    for i, course_id in enumerate(course_ids):
        res_d = {
            '_id': i,
            'code': course_id['Code'],
            'name': course_id['Name'],
            'description': "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.",
            'syllabus': "Course syllabus here.",
            'prereq': ['APS101H1, ECE101H1'],
            'coreq': ['APS102H1, ECE102H1'],
            'exclusion': ['APS102H1, ECE102H1'],
        }
        res.append(res_d)
    return res


class SearchCourse(Resource):
    def get(self):
        input = request.args.get('input')
        courses = search_course_by_code(input)
        # courses =[{'_id': 1, 'code': 'ECE444', 'name': 'SE'}, {'_id': 2,'code': 'ECE333', 'name': 'ur mom'}]
        if len(courses) > 0:
            try:
                resp = jsonify(courses)
                resp.status_code = 200
                return resp
            except Exception as e:
                resp = jsonify({'error': str(e)})
                resp.status_code = 400
                return resp

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('input', required=True)
        data = parser.parse_args()
        input = data['input']
        courses = search_course_by_code(input)
        if len(courses) > 0:
            try:
                resp = jsonify(courses)
                resp.status_code = 200
                return resp
            except Exception as e:
                resp = jsonify({'error': 'something went wrong'})
                resp.status_code = 400
                return resp


class ShowCourse(Resource):
    def get(self):
        code = request.args.get('code')
        courses = search_course_by_code(code)
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
            resp.status_code = 400
            return resp

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True)
        data = parser.parse_args()
        code = data['code']
        courses = search_course_by_code(code)
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
            resp.status_code = 400
            return resp


# API Endpoints
rest_api = Api(app)
# rest_api.add_resource(controller.SearchCourse, '/searchc')
rest_api.add_resource(SearchCourse, '/searchc')
# rest_api.add_resource(controller.ShowCourse, '/course/details')
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
        
    session["student"] = student.serialize()

    resp = jsonify(student.serialize())
    resp.status_code = 200
    return resp

# SV API for adding a course
@app.route("/api/add_course", methods=["POST"])
def add_course():
    parser = reqparse.RequestParser()
    parser.add_argument('semester', required=True)
    parser.add_argument('course', required=True)
    data = parser.parse_args()

    course = data['course']
    semester = data["semester"]

    if(session.get("student")):
        student = Student.deserialize(session["student"])
        student.get_semester(index=int(semester)).add_course(course)
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
