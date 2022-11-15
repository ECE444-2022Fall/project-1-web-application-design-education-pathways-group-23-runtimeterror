import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.color import Color

def test_frontend():
    driver = webdriver.Chrome()
    driver.get("http://localhost:3000/semester-viewer")

    time.sleep(0.5)

    # Test Initialization Form
    element = driver.find_element(By.ID, "studentForm")

    assert element.is_displayed()

    element.find_element(By.XPATH, "//form/button").click()
    notification = element.find_element(By.ID, "notification-form").text

    assert notification == "Please select a major."

    select = Select(element.find_element(By.ID, "major"))
    select.select_by_visible_text("EngSci")
    element.find_element(By.XPATH, "//form/button").click()
    notification = element.find_element(By.ID, "notification-form").text

    assert notification == "Please select a graduation year."

    select = Select(element.find_element(By.ID, "year"))
    select.select_by_visible_text("2024")
    element.find_element(By.XPATH, "//form/button").click()

    time.sleep(0.5)

    assert not element.is_displayed()

    student_info = driver.find_element(By.CLASS_NAME, "drag-column")
    assert student_info.find_element(By.XPATH,"//table/tr[1]/td[2]").text == "Your Major is: EngSci"
    assert student_info.find_element(By.XPATH,"//table/tr[2]/td[1]").text == "Earned Credits: 0"

    drag_container = driver.find_element(By.CLASS_NAME, "drag-container")
    assert drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/span/h2").text == "FALL 2020"

    # Test course addition and removal
    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/form/input").send_keys("InvalidCourse")
    drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/form/button[1]").click()

    time.sleep(1)

    notification = drag_container.find_element(By.ID, "notification-1").text
    assert notification == "Please enter a valid course name."

    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/form/input").clear()
    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/form/input").send_keys("ECE444H1")
    drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/form/button[1]").click()

    time.sleep(1)

    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/form/input").clear()
    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/form/input").send_keys("MIE451H1")
    drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/form/button[1]").click()

    time.sleep(1)
    
    course = drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/ul/li[1]").text
    color = drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/ul/li[1]").value_of_css_property("color")
    color = Color.from_string(color).hex.upper()
    assert course == "ECE444H1"
    assert color == "#70A1D7"

    course = drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/ul/li[2]").text
    color = drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/ul/li[2]").value_of_css_property("color")
    color = Color.from_string(color).hex.upper()
    assert course == "MIE451H1"
    assert color == "#F47C7C"
    
    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[4]/form/input").clear()
    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[4]/form/input").send_keys("ECO101H1")
    drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[4]/form/button[1]").click()

    time.sleep(1)

    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[4]/form/input").clear()
    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[4]/form/input").send_keys("ECE444H1")
    drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[4]/form/button[1]").click()

    time.sleep(1)

    course = drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[4]/ul/li[1]").text
    assert course == "ECO101H1"
    notification = drag_container.find_element(By.ID, "notification-2").text
    assert notification == "You have already added this course."

    drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[4]/form/button[2]").click()

    notification = drag_container.find_element(By.ID, "notification-2").text
    assert notification == "This course is not in this semester."

    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/form/input").clear()
    drag_container.find_element(By.XPATH,"//ul[@class='drag-list']/li[3]/form/input").send_keys("ECE444H1")
    drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/form/button[2]").click()


    course = drag_container.find_element(By.XPATH, "//ul[@class='drag-list']/li[3]/ul/li[1]").text
    assert not course == "ECE444H1"

    driver.close()