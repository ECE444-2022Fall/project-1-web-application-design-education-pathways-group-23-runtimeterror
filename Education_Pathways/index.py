import os

# this is the flask core
from flask import Flask, send_from_directory, jsonify, request, session
from flask_restful import Api, Resource, reqparse
from student import Student

import config
from search import SearchCourse, search_course
import semester_viewer as sv
import minor_completion as mc


class ShowCourse(Resource):
    def get(self):
        code = request.args.get('code')
        courses = search_course(code, "")
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {code} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            if(session.get("student")):
                student = Student.deserialize(session.get("student"))
                taken = student.get_courses()
                takenreq = []
                for i, course_id in enumerate(courses):
                    overall_prereq = []
                    for j in course_id["prereq"]:
                        if j in taken: 
                            takenreq.append(j)
                            continue
                        overall_prereq, takenreq = self.nested(j, taken, overall_prereq, takenreq)
                    courses[i]['prereq'] = overall_prereq  
                    courses[i]['takenreq'] = takenreq

            else:
                for i, course_id in enumerate(courses):
                    courses[i]['takenreq'] = []

            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 500
            return resp

    def nested(self, courses, taken, overall_prereq, takenreq):
        overall_prereq.append(courses)
        local = search_course(courses)[0]['prereq']
        for j in local:
            if j in taken: 
                takenreq.append(j)
                continue
            overall_prereq.append(j)
            sub_local = search_course(j)[0]['prereq']
            for k in sub_local:
                if k in taken: 
                    takenreq.append(k)
                    continue
                overall_prereq.append(k)
        return overall_prereq, takenreq


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
            if(session.get("student")):
                student = Student.deserialize(session.get("student"))
                taken = student.get_courses()
                takenreq = []
                for i, course_id in enumerate(courses):
                    overall_prereq = []
                    for j in course_id["prereq"]:
                        if j in taken: 
                            takenreq.append(j)
                            continue
                        overall_prereq, takenreq = self.nested(j, taken, overall_prereq, takenreq)
                    courses[i]['prereq'] = overall_prereq  
                    courses[i]['takenreq'] = takenreq
            else:
                for i, course_id in enumerate(courses):
                    courses[i]['takenreq'] = []
            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 500
            return resp


def create_app():
    app = Flask(__name__, static_folder='frontend/build')
    app.config['SECRET_KEY'] = "Totally a secret"
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True

    config.init_app(app)
    config.init_db()
    config.init_cors(app)

    # API Endpoints
    rest_api = Api(app)
    rest_api.add_resource(SearchCourse, '/api/search')
    rest_api.add_resource(ShowCourse, '/course/details')

    rest_api.add_resource(sv.LoadStudent, '/api/load_student')
    rest_api.add_resource(sv.CreateStudent, '/api/create_student')
    rest_api.add_resource(sv.GetCourseCategory, '/api/get_course_category')
    rest_api.add_resource(sv.GetCourseCategories, '/api/get_course_categories')
    rest_api.add_resource(sv.AddCourse, '/api/add_course')
    rest_api.add_resource(sv.RemoveCourse, '/api/remove_course')
    rest_api.add_resource(sv.SwapSemester, '/api/swap_semester')
    rest_api.add_resource(sv.GetColor, '/api/get_color')
    rest_api.add_resource(sv.SetColor, '/api/set_color')

    rest_api.add_resource(mc.CheckMinorRequirements,
                          '/api/get_minor_completion')

    @app.route("/", defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
