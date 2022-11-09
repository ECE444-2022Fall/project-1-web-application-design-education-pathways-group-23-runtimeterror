# This is to prevent circular imports

from flask_mongoengine import MongoEngine
from flask_cors import CORS

app = None
db = None
cors = None

def init_app(app_):
    global app
    app = app_
    return app

def init_db(app):
    global db
    db = MongoEngine(app)
    return db

def init_cors(app):
    global cors
    
    # Temporary Hack to allow Flask Sessions
    CORS_ALLOW_ORIGIN="*,*"
    CORS_EXPOSE_HEADERS="*,*"
    CORS_ALLOW_HEADERS="content-type,*"
    cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)

    return cors