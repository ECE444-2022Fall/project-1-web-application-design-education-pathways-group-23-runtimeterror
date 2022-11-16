import json
import pytest
from index import create_app
from student import Student

partially_complete_student = Student("ECE", "2023")
partially_complete_student.add_semester("Fall 2019","complete", ["APS360H1"])

complete_student = Student("ECE", "2023")
complete_student.add_semester("Fall 2019","complete", ["APS360H1", "ECE345H1", "CSC384H1", "ECE421H1", "ECE368H1", "ECE344H1"])

incomplete_student = Student("ECE", "2023")
incomplete_student.add_semester("Fall 2019","complete", [])


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


def test_get_minor_completion_fail_when_no_student(client):
    with client:
        # Given
        minor_name = "Artificial Intelligence"
        
        # Test
        response = client.post('/api/get_minor_completion', json={"minor_name": minor_name})
        assert response.status_code == 204

def test_get_ai_minor_completion_with_partially_incomplete_student(client):
    with client.session_transaction() as session:
        session["student"] = partially_complete_student.serialize()
    with client:
        # Given
        
        minor_name = "Artificial Intelligence"
        expected = [
            [['APS360H1'], True],
             [['CSC263H1', 'ECE345H1', 'ECE358H1', 'MIE335H1'], False],
              [['CSC384H1', 'MIE369H1', 'ROB311H1'], False],
               [['CSC311H1', 'ECE421H1', 'MIE424H1', 'ROB313H1'], False],
                [['CHE507H1', 'CSC401H1', 'CHE507H1', 'CSC401H1', 'CSC420H1', 'CSC413H1', 'CSC485H1', 'CSC486H1', 'ECE368H1', 'HPS345H1', 'HPS346H1', 'MIE368H1', 'MIE451H1', 'MIE457H1', 'MIE562H1', 'MIE566H1', 'MSE403H1', 'ROB501H1'], False],
                 [['CHE507H1', 'CSC401H1', 'CHE507H1', 'CSC401H1', 'CSC420H1', 'CSC413H1', 'CSC485H1', 'CSC486H1', 'ECE368H1', 'HPS345H1', 'HPS346H1', 'MIE368H1', 'MIE451H1', 'MIE457H1', 'MIE562H1', 'MIE566H1', 'MSE403H1', 'ROB501H1', 'AER336H1', 'BME595H1', 'CHE322H1', 'CSC343H1', 'CSC412H1', 'ECE344H1', 'ECE353H1', 'ECE356H1', 'ECE367H1', 'ECE411H1', 'ECE419H1', 'ECE431H1', 'ECE444H1', 'ECE454H1', 'ECE470H1', 'ECE516H1', 'ECE532H1', 'ECE557H1', 'ECE568H1', 'MAT336H1', 'MAT389H1', 'STA302H1', 'STA410H1'], False]
                 ]
        
        # Test
        response = client.post('/api/get_minor_completion', json={"minor_name": minor_name})

        assert response.status_code == 200
        json_data = json.loads(response.get_data(as_text=True))
        course_completion_status = json_data["completion"]

        assert course_completion_status, \
            "The course completion response isn't provided"
        for i in range(len(expected)):
            assert course_completion_status[i] == expected[i], \
                f"Requirement {i+1} not correctly recognized as un/satisfied"

def test_get_ai_minor_completion_with_complete_student(client):
    with client.session_transaction() as session:
        session["student"] = complete_student.serialize()
    with client:
        # Given
        
        minor_name = "Artificial Intelligence"
        expected = [
            [['APS360H1'], True],
             [['CSC263H1', 'ECE345H1', 'ECE358H1', 'MIE335H1'], True],
              [['CSC384H1', 'MIE369H1', 'ROB311H1'], True],
               [['CSC311H1', 'ECE421H1', 'MIE424H1', 'ROB313H1'], True],
                [['CHE507H1', 'CSC401H1', 'CHE507H1', 'CSC401H1', 'CSC420H1', 'CSC413H1', 'CSC485H1', 'CSC486H1', 'ECE368H1', 'HPS345H1', 'HPS346H1', 'MIE368H1', 'MIE451H1', 'MIE457H1', 'MIE562H1', 'MIE566H1', 'MSE403H1', 'ROB501H1'], True],
                 [['CHE507H1', 'CSC401H1', 'CHE507H1', 'CSC401H1', 'CSC420H1', 'CSC413H1', 'CSC485H1', 'CSC486H1', 'ECE368H1', 'HPS345H1', 'HPS346H1', 'MIE368H1', 'MIE451H1', 'MIE457H1', 'MIE562H1', 'MIE566H1', 'MSE403H1', 'ROB501H1', 'AER336H1', 'BME595H1', 'CHE322H1', 'CSC343H1', 'CSC412H1', 'ECE344H1', 'ECE353H1', 'ECE356H1', 'ECE367H1', 'ECE411H1', 'ECE419H1', 'ECE431H1', 'ECE444H1', 'ECE454H1', 'ECE470H1', 'ECE516H1', 'ECE532H1', 'ECE557H1', 'ECE568H1', 'MAT336H1', 'MAT389H1', 'STA302H1', 'STA410H1'], True]
                 ]
        
        # Test
        response = client.post('/api/get_minor_completion', json={"minor_name": minor_name})

        assert response.status_code == 200
        json_data = json.loads(response.get_data(as_text=True))
        course_completion_status = json_data["completion"]

        assert course_completion_status, \
            "The course completion response isn't provided"
        for i in range(len(expected)):
            assert course_completion_status[i] == expected[i], \
                f"Requirement {i+1} not correctly recognized as un/satisfied"

def test_get_ai_minor_completion_with_incomplete_student(client):
    with client.session_transaction() as session:
        session["student"] = incomplete_student.serialize()
    with client:
        # Given
        
        minor_name = "Artificial Intelligence"
        expected = [
            [['APS360H1'], False],
             [['CSC263H1', 'ECE345H1', 'ECE358H1', 'MIE335H1'], False],
              [['CSC384H1', 'MIE369H1', 'ROB311H1'], False],
               [['CSC311H1', 'ECE421H1', 'MIE424H1', 'ROB313H1'], False],
                [['CHE507H1', 'CSC401H1', 'CHE507H1', 'CSC401H1', 'CSC420H1', 'CSC413H1', 'CSC485H1', 'CSC486H1', 'ECE368H1', 'HPS345H1', 'HPS346H1', 'MIE368H1', 'MIE451H1', 'MIE457H1', 'MIE562H1', 'MIE566H1', 'MSE403H1', 'ROB501H1'], False],
                 [['CHE507H1', 'CSC401H1', 'CHE507H1', 'CSC401H1', 'CSC420H1', 'CSC413H1', 'CSC485H1', 'CSC486H1', 'ECE368H1', 'HPS345H1', 'HPS346H1', 'MIE368H1', 'MIE451H1', 'MIE457H1', 'MIE562H1', 'MIE566H1', 'MSE403H1', 'ROB501H1', 'AER336H1', 'BME595H1', 'CHE322H1', 'CSC343H1', 'CSC412H1', 'ECE344H1', 'ECE353H1', 'ECE356H1', 'ECE367H1', 'ECE411H1', 'ECE419H1', 'ECE431H1', 'ECE444H1', 'ECE454H1', 'ECE470H1', 'ECE516H1', 'ECE532H1', 'ECE557H1', 'ECE568H1', 'MAT336H1', 'MAT389H1', 'STA302H1', 'STA410H1'], False]
                 ]
        
        # Test
        response = client.post('/api/get_minor_completion', json={"minor_name": minor_name})

        assert response.status_code == 200
        json_data = json.loads(response.get_data(as_text=True))
        course_completion_status = json_data["completion"]

        assert course_completion_status, \
            "The course completion response isn't provided"
        for i in range(len(expected)):
            assert course_completion_status[i] == expected[i], \
                f"Requirement {i+1} not correctly recognized as un/satisfied"