import pytest
from flask import session
from index import create_app
from student import Student

# Test template from https://flask.palletsprojects.com/en/2.2.x/testing/
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

def test_create_student(client):
    with client:
        major = "EngSci"
        year = 2023

        response = client.post("/api/create_student", json={"major": major, "year": year})

        assert response.status_code == 200

        student = Student.deserialize(session.get("student"))

        assert student.major == major
        assert int(student.year) == year
        assert student.get_semester(index=0).name == "Fall 2019"
        assert student.get_semester(index=0).status == "complete"
        
        assert student.get_semester("Fall 2022").status == "in progress"

        assert student.get_semester(index=-1).name == "Winter 2023"
        assert student.get_semester(index=-1).status == "planned"

def test_load_student(client):
    with client:
        major = "EngSci"
        year = 2023

        response = client.get("/api/load_student")

        assert response.status_code == 204

        response = client.post("/api/create_student", json={"major": major, "year": year})
        response = client.get("/api/load_student")
        assert response.status_code == 200

        student = Student.deserialize(response.json)

        assert student.major == major
        assert int(student.year) == year
        assert student.get_semester(index=0).name == "Fall 2019"
        assert student.get_semester(index=0).status == "complete"
        
        assert student.get_semester("Fall 2022").status == "in progress"

        assert student.get_semester(index=-1).name == "Winter 2023"
        assert student.get_semester(index=-1).status == "planned"

def test_get_course_category(client):
    with client:
        major = "EngSci"
        year = 2023

        response = client.post("/api/create_student", json={"major": major, "year": year})

        response = client.post("/api/get_course_category", json={"course": "Fake Course"})
        assert response.status_code == 204

        response = client.post("/api/get_course_category", json={"course": "ESC101H1"})
        assert response.status_code == 200
        assert response.json["category"] == "core"

        response = client.post("/api/get_course_category", json={"course": "ECE444H1"})
        assert response.status_code == 200
        assert response.json["category"] == "elective"
        
        response = client.post("/api/get_course_category", json={"course": "JRE420H1"})
        assert response.status_code == 200
        assert response.json["category"] == "minor"

        response = client.post("/api/get_course_category", json={"course": "ECE344H1"})
        assert response.status_code == 200
        assert response.json["category"] == "extra"

def test_add_remove_course(client):
    with client:
        major = "EngSci"
        year = 2023
        course = "ECE444H1"
        semester = 0

        response = client.post("/api/create_student", json={"major": major, "year": year})
        response = client.post("/api/add_course", json={"course": course, "semester": semester, "category": "elective"})

        assert response.status_code == 200

        student = Student.deserialize(session.get("student"))
        assert course in student.get_semester(index=semester).get_courses()

        response = client.post("/api/remove_course", json={"course": course, "semester": 0})

        assert response.status_code == 200

        student = Student.deserialize(session.get("student"))
        assert not course in student.get_semester(index=semester).get_courses()

def test_swap_semester(client):
    with client:
        major = "EngSci"
        year = 2023
        course = "ECE444H1"
        source_semester = 0
        target_semester = -1

        response = client.post("/api/create_student", json={"major": major, "year": year})
        response = client.post("/api/add_course", json={"course": course, "semester": source_semester, "category": "elective"})

        response = client.post("/api/swap_semester", json={"course": course, "source_semester": source_semester, "target_semester": target_semester})

        assert response.status_code == 200

        student = Student.deserialize(session.get("student"))
        assert course in student.get_semester(index=target_semester).get_courses()
        assert not course in student.get_semester(index=source_semester).get_courses()

def test_get_course_categories(client):
    with client:
        major = "EngSci"
        year = 2023
        courses = ["ESC101H1","ECE444H1","JRE420H1","ECE244H1"]
        categories = [""]*4
        source_semester = 0
        target_semester = -1

        response = client.post("/api/create_student", json={"major": major, "year": year})
        for i in range(4):
            response = client.post("/api/get_course_category", json={"course": courses[i]})
            categories[i] = response.json["category"]
            response = client.post("/api/add_course", json={"course": courses[i], "semester": source_semester, "category": categories[i]})

        response = client.post("/api/swap_semester", json={"course": courses[0], "source_semester": source_semester, "target_semester": target_semester})

        response = client.post("/api/remove_course", json={"course": courses[2], "semester": source_semester})
        response = client.post("/api/add_course", json={"course": courses[3], "semester": target_semester, "category": categories[i]})

        response = client.get("/api/get_course_categories")

        assert response.status_code == 200

        expected_categories = [[] for _ in range(8)]
        expected_categories[0].append(categories[1])
        expected_categories[0].append(categories[3])
        expected_categories[-1].append(categories[0])
        expected_categories[-1].append(categories[3])

        assert response.json["categories"] == expected_categories

def test_color(client):
    with client:
        DEFAULT_COLORS = {"core": "#F47C7C", "elective": "#70A1D7", "minor": "#A1DE93", "extra": "#F7F48B"}

        response = client.get("/api/get_color")

        assert response.status_code == 200
        assert response.json["color"]  == DEFAULT_COLORS

        color = DEFAULT_COLORS
        color["core"] = "#FFFFFF"

        response = client.post("/api/set_color", json={"color": color})
        assert response.status_code == 200

        response = client.get("/api/get_color")
        assert response.status_code == 200
        assert response.json["color"]["core"] == "#FFFFFF"