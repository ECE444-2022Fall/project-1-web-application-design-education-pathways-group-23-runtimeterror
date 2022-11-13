import pytest
import config
from minor import search_minor_requirements


@pytest.fixture
def initialize_db():
    config.init_db()


def test_search_minor(initialize_db):
    # Course name, no minor
    res = search_minor_requirements("Engineering Business")
    assert len(res) == 1
    res = res[0]
    assert res["name"] == "Engineering Business", \
        "Incorrect minor name"
    assert res["code"] == "AEMINBUS", \
        "Incorrect minor code"
    assert res["requirements"] == [
        ["CHE294H1", "CHE374H1", "CME368H1", "ECE472H1", "MIE258H1"],
        ["JRE300H1"],
        ["JRE410H1"],
        ["JRE420H1"],
        ["APS500H1", "APS502H1", "ECE488H1", "ECO101H1", "FOR308H1", "MIE488H1", "MSE488H1", "MIE354H1", "PHL295H1", "TEP234H1", "TEP343H1", "TEP444H1", "TEP445H1", "APS510H1", "APS420H1", "APS511H1", "CHE488H1", "CIV488H1", "ECO102H1",
         "GGR251H1", "GGR252H1", "HPS283H1", "MIE540H1", "TEP343H1", "TEP432H1", "TEP442H1", "TEP447H1", "TEP448H1"],
        ["APS500H1", "APS502H1", "ECE488H1", "ECO101H1", "FOR308H1", "MIE488H1", "MSE488H1", "MIE354H1", "PHL295H1", "TEP234H1", "TEP343H1", "TEP444H1", "TEP445H1", "APS510H1",
         "APS420H1", "APS511H1", "CHE488H1", "CIV488H1", "ECO102H1", "GGR251H1", "GGR252H1", "HPS283H1", "MIE540H1", "TEP343H1", "TEP432H1", "TEP442H1", "TEP447H1", "TEP448H1"]
    ], \
        "Incorrect requirement list"
