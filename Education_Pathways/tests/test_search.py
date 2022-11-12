import pytest
import config
from search import search_course

@pytest.fixture
def initialize_db():
    config.init_db()

def test_search_code(initialize_db):
    # Course name, no minor
    assert search_course("Software Engineering", "")[0]["code"] == "ECE444H1", \
        "Incorrect course code"

def test_search_name(initialize_db):
    # Course code, no minor
    assert search_course("ECE444", "")[0]["name"] == "Software Engineering", \
        "Incorrect course name"

def test_search_name_minor(initialize_db):
    # Course name, minor
    assert search_course("Algorithms and Data Structures", "AEMINAIEN")[0]["code"] == "ECE345H1", \
        "Incorrect course found or course not found"

def test_search_code_minor(initialize_db):
    # Course code, minor
    assert search_course("ECE345", "AEMINAIEN")[0]["code"] == "ECE345H1", \
        "Incorrect course found or course not found"