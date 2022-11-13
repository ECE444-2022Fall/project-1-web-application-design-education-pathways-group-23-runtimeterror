# This is to prevent circular imports

import os
from pymongo import MongoClient
from flask_cors import CORS


app = None
db = None
course_collection = None
cors = None


def init_app(app_):
    global app
    app = app_
    return app


def init_db():
    global db
    global course_collection

    # Provide the mongodb atlas url to connect python to mongodb using pymongo

    CONNECTION_STRING = f"mongodb+srv://admin:{os.environ.get('MONGO_PASS')}@cluster0.o7bvcw3.mongodb.net/test"
    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Grab and store the test database and the course collection
    db = client['test']
    course_collection = db["courses"]

    return db


def init_cors(app):
    global cors
    
    # Temporary Hack to allow Flask Sessions
    CORS_ALLOW_ORIGIN="*,*"
    CORS_EXPOSE_HEADERS="*,*"
    CORS_ALLOW_HEADERS="content-type,*"
    cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)

    return cors
