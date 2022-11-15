import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.color import Color

def test_course_frontend():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:3000/courseDetails/ECE444H1")

    time.sleep(1)

    assert driver.find_element(By.CLASS_NAME, "course-title").text == "ECE444H1 : Software Engineering"
    assert driver.find_element(By.CLASS_NAME, "course-description").text  == \
        "Course Description\n" \
        + "The software development process. Software requirements and " \
        + "specifications. Software design techniques. Techniques for " \
        + "developing large software systems; CASE tools and software " \
        + "development environments. Software testing, documentation and maintenance."

    prerequisites = driver.find_element(By.XPATH, "//div[@class='col-item course-requisite row']/div[2]/div[1]")
    assert prerequisites.text == "Pre-Requisites\n" \
        + "ECE344H1, ECE353H1"

    driver.close()
