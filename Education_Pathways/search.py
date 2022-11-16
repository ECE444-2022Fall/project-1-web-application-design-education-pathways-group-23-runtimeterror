import re
import config
from flask import jsonify, request, session
from flask_restful import Resource, reqparse
from student import Student

# route functions


def search_course(search_term, minor="", mse_theme=""):
    """
    Search for courses that match a given search_term in the given minor
    Inputs
    ------------------
    search_term (str)   - A search term that will be matched to course
                          names or codes
    minor (str)         - An optional minor to restrict the search
                          ("" means no minor selected)
    mse_theme (str)     - An optional theme to restrict the search
                          ("" means no theme selected)

    Output
    ------------------
    res (dict): A dictionary containing the information of courses
                that match the query

    """
    # return all the courses whose course code contains the str search_Term
    regx = re.compile(f".*{search_term.upper()}.*", re.IGNORECASE)
    query_object = {
        "$and": [
            {
                "$or": [{"Code": regx}, {"Name": regx}],
            }
        ]
    }

    if minor != "":
        query_object["$and"].append({"MinorsOutcomes": minor})

    if mse_theme != "":
        query_object["$and"].append({"MSE Themes": mse_theme})

    course_ids = list(config.course_collection.find(query_object))
    if len(course_ids) == 0:
        return []
    if len(course_ids) > 10:
        course_ids = course_ids[:10]

    res = []
    for i, course_id in enumerate(course_ids):
        res_d = {
            "_id": i,
            "code": course_id["Code"],
            "name": course_id["Name"],
            "division": course_id["Division"],
            "department": course_id["Department"],
            "description": course_id["Course Description"],
            "syllabus": "Course syllabus here.",
            "prereq": course_id["Pre-requisites"],
            "coreq": course_id["Corequisite"],
            "exclusion": course_id["Exclusion"],
        }
        res.append(res_d)
    return res


class SearchCourse(Resource):
    def get(self):
        input = request.args.get("input")
        minor = request.args.get("minor")
        mse_theme = request.args.get("mse_theme")

        courses = search_course(input, minor, mse_theme)
        # courses =[{'_id': 1, 'code': 'ECE444', 'name': 'SE'}]
        try:
            if session.get("student"):
                student = Student.deserialize(session.get("student"))
                taken = student.get_courses()

                for id, course in enumerate(courses):
                    count = len(course["prereq"])
                    for j in taken:
                        if j in course["prereq"]:
                            count -= 1
                    if count <= 0:
                        courses[id]["starred"] = True
                    else:
                        courses[id]["starred"] = False

            resp = jsonify(courses)
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({"error": str(e)})
            resp.status_code = 500
            return resp

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("input", required=True)
        parser.add_argument("minor", required=True)
        parser.add_argument("mse_theme", required=True)

        data = parser.parse_args()
        input = data["input"]
        minor = data["minor"]
        mse_theme = data["mse_theme"]

        courses = search_course(input, minor, mse_theme)
        try:

            if session.get("student"):
                student = Student.deserialize(session.get("student"))
                taken = student.get_courses()

                for id, course in enumerate(courses):
                    count = len(course["prereq"])
                    for j in taken:
                        if j in course["prereq"]:
                            count -= 1
                    if count <= 0:
                        courses[id]["starred"] = True
                    else:
                        courses[id]["starred"] = False

            resp = jsonify(courses)
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({"error": "something went wrong"})
            resp.status_code = 500
            return resp
