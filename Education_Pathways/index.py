# this is the flask core

from flask import Flask, send_from_directory, jsonify, request, session
from flask_restful import Api,Resource, reqparse
from flask_cors import CORS
import os

import pandas as pd
df = pd.read_csv("resources/courses.csv")

from student import Student
import config
app = Flask(__name__, static_folder='frontend/build')
app.config['SECRET_KEY'] = "Totally a secret"
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

# MongoDB URI
# DB_URI = "mongodb+srv://Cansin:cv190499@a-star.roe6s.mongodb.net/A-Star?retryWrites=true&w=majority"
# app.config["MONGODB_HOST"] = DB_URI

config.init_app(app)
config.init_db(app)
config.init_cors(app)

# route functions
def search_course_by_code(s):
    # return all the courses whose course code contains the str s
    course_ids = df[df['Code'].str.contains(s.upper())].index.tolist()
    if len(course_ids) == 0:
        return []
    if len(course_ids) > 10:
        course_ids = course_ids[:10]
    res = []
    for i, course_id in enumerate(course_ids):
        d = df.iloc[course_id].to_dict()
        res_d = {
            '_id': i,
            'code': d['Code'],
            'name': d['Name'],
            'description': "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.",
            'syllabus': "Course syllabus here.",
            'prereq': ['APS101H1, ECE101H1'],
            'coreq': ['APS102H1, ECE102H1'],
            'exclusion': ['APS102H1, ECE102H1'] ,
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
        
    else:
        student = init_student()
        session["student"] = student.serialize()

    resp = jsonify(student.serialize())
    resp.status_code = 200
    return resp

# Temporary Solution for initializing students (will replace with more dynamic method)
default_semesters = ["Fall 2022", "Winter 2023", "Fall 2023", "Winter 2024", "Fall 2024", "Winter 2025", "Fall 2025", "Winter 2026"]
def init_student():
    student = Student("", 1, [] )

    for semester in default_semesters:
        student.add_semester(semester, "planned")

    return student

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
        student.get_semester(default_semesters[int(semester)]).add_course(course)
        session["student"] = student.serialize()
        
        resp = jsonify({
            "course": course
            })
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
        student.get_semester(default_semesters[int(semester)]).remove_course(course)
        session["student"] = student.serialize()

        resp = jsonify({
            "course": course
            })
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

    
    
