import pytest
from flask import session
from index import create_app
from course import Course

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_search_api(client):
    with client:
        input = "ECE444"
        minor = ""
        mse_theme = ""

        response = client.get("/api/search")
        assert response.status_code == 204

        response = client.post("/api/search", json={"input":input, "minor": minor, "mse_theme": mse_theme})
        response = client.get("/api/search")
        assert response.status_code == 200

        course = Course.deserialize(response.json)

        assert course.name == "Software Engineering"
        assert course.code == "ECE444H1"
        

