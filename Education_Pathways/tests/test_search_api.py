import pytest
from flask import session
from index import create_app

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

# Valentina Manferrari
def test_search_api(client):
    with client:
        # Given
        input = "ECE444"
        minor = ""
        mse_theme = ""

        # Test
        response = client.post("/api/search", json={"input":input, "minor": minor, "mse_theme": mse_theme})
        assert response.status_code == 200
        
        assert len(response.json) == 1
        course = response.json[0]
        assert course['name'] == "Software Engineering"
        assert course['code'] == "ECE444H1"

def test_search_api_minor(client):
    with client:
        # Given
        input = "ECE344"
        minor = "AEMINAIEN"
        mse_theme = ""

        # Test
        response = client.post("/api/search", json={"input":input, "minor": minor, "mse_theme": mse_theme})
        assert response.status_code == 200
        
        assert len(response.json) == 1
        course = response.json[0]
        assert course['name'] == "Operating Systems"
        assert course['code'] == "ECE344H1"

def test_search_api_mse_theme(client):
    with client:
        # Given
        input = "mse343"
        minor = ""
        mse_theme = "Biomaterials"

        # Test
        response = client.post("/api/search", json={"input":input, "minor": minor, "mse_theme": mse_theme})
        assert response.status_code == 200
        
        assert len(response.json) == 1
        course = response.json[0]
        assert course['name'] == "Biomaterials"
        assert course['code'] == "MSE343H1"

def test_search_api_minor_and_theme(client):
    with client:
        # Given
        input = "mse343"
        minor = "AEMINBIO"
        mse_theme = "Biomaterials"

        # Test
        response = client.post("/api/search", json={"input":input, "minor": minor, "mse_theme": mse_theme})
        assert response.status_code == 200
        
        assert len(response.json) == 1
        course = response.json[0]
        assert course['name'] == "Biomaterials"
        assert course['code'] == "MSE343H1"

def test2_search_api_minor_and_theme(client):
    with client:
        # Given
        input = ""
        minor = "AEMINBIO"
        mse_theme = "Biomaterials"

        # Test
        response = client.post("/api/search", json={"input":input, "minor": minor, "mse_theme": mse_theme})
        assert response.status_code == 200
        
        assert len(response.json) == 5
    
