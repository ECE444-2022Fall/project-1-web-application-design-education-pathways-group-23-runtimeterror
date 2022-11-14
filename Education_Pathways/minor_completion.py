import sys
from flask import jsonify, session
from flask_restful import Resource, reqparse

import config
from student import Student
from degree import Minor

# Minor Completion API
# MC API for receiving minor completion for a student


class CheckMinorRequirements(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('minor_name', type=str)
        data = parser.parse_args()
        minor_name = data['minor_name'] if data['minor_name'] else ""

        if not session.get("student"):
            resp = jsonify(
                {'error': 'Student course list has not been set'})
            resp.status_code = 400
            return resp

        if minor_name == "":
            resp = jsonify(
                {'error': 'Minor has not been provided'})
            resp.status_code = 400
            return resp
        student = Student.deserialize(session["student"])

        minor_collection = config.db["minors"]
        minor_db_object = list(
            minor_collection.find({"name": minor_name}))

        if len(minor_db_object) == 0:
            resp = jsonify(
                {'error': 'Could not find minor in list'})
            resp.status_code = 500
            return resp

        minor = Minor(
            name=minor_db_object["name"], requirements=minor_db_object[""]
        )
        completion = minor.check_progress(student.get_courses)
        resp = jsonify({'completion': completion})
        resp.status_code = 200

        return resp

    def post(self, minor_name=""):
        parser = reqparse.RequestParser()
        parser.add_argument('minor_name', type=str)
        data = parser.parse_args()
        minor_name = data['minor_name'] if data['minor_name'] else ""

        if not session.get("student"):
            resp = jsonify(
                {'error': 'Student course list has not been set'})
            resp.status_code = 400
            return resp

        if minor_name == "":
            resp = jsonify(
                {'error': 'Minor has not been provided'})
            resp.status_code = 400
            return resp
        student = Student.deserialize(session["student"])

        minor_collection = config.db["minors"]
        minor_db_object = list(
            minor_collection.find({"name": minor_name}))

        if len(minor_db_object) == 0:
            resp = jsonify(
                {'error': 'Either minor or student course list hasn\'t been set'})
            resp.status_code = 400
            return resp

        minor_db_object = minor_db_object[0]
        minor = Minor(
            name=minor_db_object["name"], requirements=minor_db_object["requirements"]
        )
        completion = minor.check_progress(student.get_courses())
        resp = jsonify({'completion': completion})
        resp.status_code = 200

        return resp
