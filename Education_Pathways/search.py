import re
import config
from flask import jsonify, request
from flask_restful import Resource, reqparse
# route functions


def search_course(search_term, minor):
    """
        Search for courses that match a given search_term in the given minor
        Inputs
        ------------------
        search_term (str)   - A search term that will be matched to course
                              names or codes
        minor (str)         - An optional minor to restrict the search
                              ("" means no minor selected)

        Output
        ------------------
        res (dict): A dictionary containing the information of courses
                    that match the query

    """
    # return all the courses whose course code contains the str s
    regx = re.compile(f'.*{search_term.upper()}.*', re.IGNORECASE)
    query_object = {
        "$and": [
            {
                "$or": [
                    {"Code": regx},
                    {"Name": regx}
                ],
            }
        ]
    }

    # TODO: Handle whatever unhappy message is sent for minor when not needed
    if minor != "":
        query_object["$and"].append(
            {
                "MinorsOutcomes": minor
            }
        )

    course_ids = list(config.course_collection.find(query_object))
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
        minor = request.args.get('minor')

        courses = search_course(input, minor)
        # courses =[{'_id': 1, 'code': 'ECE444', 'name': 'SE'}]
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
        parser.add_argument('minor', required=True)
        data = parser.parse_args()
        input = data['input']
        minor = data['minor']
        courses = search_course(input, minor)
        if len(courses) > 0:
            try:
                resp = jsonify(courses)
                resp.status_code = 200
                return resp
            except Exception as e:
                resp = jsonify({'error': 'something went wrong'})
                resp.status_code = 400
                return resp


if __name__ == '__main__':
    config.init_db()

    # Course name, no minor
    assert search_course("Software Engineering", "")[0]["code"] == "ECE444H1", \
        "Incorrect course code"

    # Course code, no minor
    assert search_course("ECE444", "")[0]["name"] == "Software Engineering", \
        "Incorrect course name"

    # Course name, minor
    assert search_course("Algorithms and Data Structures", "AEMINAIEN")[0]["code"] == "ECE345H1", \
        "Incorrect course found or course not found"

    # Course code, minor
    assert search_course("ECE345", "AEMINAIEN")[0]["code"] == "ECE345H1", \
        "Incorrect course found or course not found"
