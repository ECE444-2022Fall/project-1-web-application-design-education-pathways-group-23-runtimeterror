import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Test Function written by: Dean Yu
def test_mc_frontend():
    # Initialize student
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:3000/semester-viewer")

    time.sleep(0.5)

    element = driver.find_element(By.ID, "studentForm")
    select = Select(element.find_element(By.ID, "major"))
    select.select_by_visible_text("EngSci")
    select = Select(element.find_element(By.ID, "year"))
    select.select_by_visible_text("2024")
    element.find_element(By.XPATH, "//form/button").click()

    drag_container = driver.find_element(By.CLASS_NAME, "drag-container")
    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[3]/form/input"
    ).send_keys("JRE300H1")
    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[3]/form/button[1]"
    ).click()

    time.sleep(2)

    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[4]/form/input"
    ).send_keys("MIE369H1")
    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[4]/form/button[1]"
    ).click()

    time.sleep(1)

    driver.find_element(By.XPATH, "//div/div[2]/a[@class='nav-link']").click()

    assert driver.find_element(By.CLASS_NAME, "list-group").text == ""

    select = Select(driver.find_element(By.ID, "minor-select"))
    select.select_by_visible_text("Engineering Business")

    time.sleep(1)

    requirement_1 = driver.find_element(
        By.XPATH, "//div[@class='list-group']/div[1]/div/div"
    )

    assert (
        requirement_1.text
        == "Requirement 1\n"
        + "Select one from:\n"
        + "CHE294H1, CHE374H1, CME368H1, ECE472H1, MIE258H1"
    )

    requirement_1_check = driver.find_element(
        By.XPATH,
        "//div[@class='list-group']/div[1]/div/div[@class='single-requirement-check-container']/img",
    )
    assert (
        requirement_1_check.get_attribute("src")
        == "https://static.thenounproject.com/png/3557919-200.png"
    )

    requirement_2 = driver.find_element(
        By.XPATH, "//div[@class='list-group']/div[2]/div/div"
    )

    assert requirement_2.text == "Requirement 2\n" + "Must take:\n" + "JRE300H1"

    requirement_2_check = driver.find_element(
        By.XPATH,
        "//div[@class='list-group']/div[2]/div/div[@class='single-requirement-check-container']/img",
    )
    assert (
        requirement_2_check.get_attribute("src")
        == "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/800px-Sign-check-icon.png"
    )

    select = Select(driver.find_element(By.ID, "minor-select"))
    select.select_by_visible_text("Artificial Intelligence")

    time.sleep(1)

    requirement_1 = driver.find_element(
        By.XPATH, "//div[@class='list-group']/div[1]/div/div"
    )

    assert requirement_1.text == "Requirement 1\n" + "Must take:\n" + "APS360H1"

    requirement_1_check = driver.find_element(
        By.XPATH,
        "//div[@class='list-group']/div[1]/div/div[@class='single-requirement-check-container']/img",
    )
    assert (
        requirement_1_check.get_attribute("src")
        == "https://static.thenounproject.com/png/3557919-200.png"
    )

    requirement_3 = driver.find_element(
        By.XPATH, "//div[@class='list-group']/div[3]/div/div"
    )

    assert (
        requirement_3.text
        == "Requirement 3\n" + "Select one from:\n" + "CSC384H1, MIE369H1, ROB311H1"
    )

    requirement_3_check = driver.find_element(
        By.XPATH,
        "//div[@class='list-group']/div[3]/div/div[@class='single-requirement-check-container']/img",
    )
    assert (
        requirement_3_check.get_attribute("src")
        == "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/800px-Sign-check-icon.png"
    )

    driver.close()
