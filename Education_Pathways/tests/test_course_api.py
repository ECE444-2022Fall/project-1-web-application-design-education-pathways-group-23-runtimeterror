import pytest
from flask import session
from index import create_app
from student import Student



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


# Samir Khaki
def test_course_api(client):
    with client:
        # Given
        input = "ECE444"
        
        # Test
        response = client.post("/course/details", json={"code":input})
        assert response.status_code == 200 # Correct Response code
        assert len(response.json) == 1 # Should only return 1 course
        course = response.json['course'] #Extract code
        assert course['name'] == "Software Engineering" #Check correct course name
        assert course['code'] == "ECE444H1" # Check correct Course Code




def test_course_prereq_api(client):
    with client:
        # Given
        input = "ECE344" # Testing course

        # Test
        response = client.post("/course/details", json={"code":input})
        assert response.status_code == 200 # Correct Response code
        assert len(response.json) == 1 # Should only return 1 course
        course = response.json['course'] #Extract code
        real_pre_req = ["ECE243H1", "ECE244H1"] # List of actual Pre-req's
        assert len(course['prereq']) == len(real_pre_req) # Check the same number of Pre-reqs
        for i in real_pre_req:
            assert i in course['prereq'] # Check that all pre-reqs match perfect
        assert course['code'] == "ECE344H1" # Finally re-check the course code
        

       
        
def test_course_prereq_with_student_api(client):
    with client:
        # Given a student and input course pre-req!
        input = "ECE344"
        major = "EngSci"
        year = 2023
        course = "ECE243H1"
        response = client.post("/api/create_student", json={"major": major, "year": year})
        response = client.get("/api/load_student")
        response = client.post("/api/add_course", json={"course": course, "semester": 0, "category": "elective"})
        assert response.status_code == 200

        student = Student.deserialize(session.get("student"))
        # Test
        
        assert len(student.get_courses()) == 1 # Check student created properly
        response = client.post("/course/details", json={"code":input})
        assert response.status_code == 200 # Correct Response code
        assert len(response.json) == 1 # Should only return 1 course
        course = response.json['course'] #Extract code
        real_pre_req = ["ECE243H1", "ECE244H1"] # List of actual Pre-req's
        
        
        assert len(course['prereq']) == len(real_pre_req) # Check pre-req length matches
        assert len(course['takenreq']) == len(real_pre_req)-1 # Check correct number of taken reqs
        assert course['takenreq'] == ["ECE243H1"] # Check that it populates correctly from student
        assert "ECE243H1" in student.get_courses() # Check that it exists in student courses
        assert course['code'] == "ECE344H1" # Finally re-check the course code
        
        
