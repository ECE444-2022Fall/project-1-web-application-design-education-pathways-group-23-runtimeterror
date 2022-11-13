import re
import config
from flask import jsonify, request
from flask_restful import Resource, reqparse
# route functions


def search_minor_requirements(minor_name=""):
    """
        Search for courses that match a given search_term in the given minor
        Inputs
        ------------------
        minor_name (str)   - The name of the minor to query requirements for

        Output
        ------------------
        res (dict): A dictionary containing the requirement information for the
                    minor

    """
    # return all the courses whose course code contains the str search_Term

    minor_info = list(config.minors_collection.find({
        "name": minor_name
    }))

    if len(minor_info) == 0:
        return []

    return minor_info


class SearchCourse(Resource):
    def get(self):
        minor_name = request.args.get('minor_name')

        minor_info = search_minor_requirements(minor_name=minor_name)

        if len(minor_info) == 0:
            resp = jsonify({'error': 'The requested minor resource not found'})
            resp.status_code = 404
            return resp

        print(minor_info)
        try:
            resp = jsonify(minor_info[0])
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': str(e)})
            resp.status_code = 500
            return resp

    def post(self):
        minor_name = request.args.get('minor_name')

        minor_info = search_minor_requirements(minor_name=minor_name)

        if len(minor_info) == 0:
            resp = jsonify({'error': 'The requested minor resource not found'})
            resp.status_code = 404
            return resp

        print(minor_info)
        try:
            resp = jsonify(minor_info[0])
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': str(e)})
            resp.status_code = 500
            return resp
