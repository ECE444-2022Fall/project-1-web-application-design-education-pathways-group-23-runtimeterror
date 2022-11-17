import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


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
        By.XPATH, "//ul[@class='drag-list']/li[3]/form/input").send_keys("APS105H1")
    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[3]/form/button[1]").click()

    time.sleep(2)

    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[3]/form/input").clear()

    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[3]/form/input").send_keys("ECE244H1")
    drag_container.find_element(
        By.XPATH, "//ul[@class='drag-list']/li[3]/form/button[1]").click()

    time.sleep(1)

    driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[1]/div/nav/span").click()

    drag_container = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[1]/form/div[1]/input[1]").send_keys("ECE")
    select = Select(driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[1]/form/div[2]/select[1]"))
    select.select_by_visible_text("Artificial Intelligence")

    driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[1]/form/div[1]/input[2]").click()

    time.sleep(2)

    course = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[3]/a/div/div[1]/h5").text
    assert course == "ECE297H1"

    courseType = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[3]/a/div/div[2]/h5").text
    assert courseType == "Software Design and Communication"

    division = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[3]/a/div/div[3]").text
    assert division == "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."

    faculty = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[3]/a/div/div[4]").text
    assert faculty == "Faculty of Applied Science & Engineering"

    prereq_check = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[2]/div[3]/a/div/div[5]/img")
    assert prereq_check.get_attribute("src") \
        == "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAuCAYAAABu3ppsAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAVXSURBVHgBzVrNchtFEO6ZWQmqsCnByZQDXt9yi3KBkCKOfOMW5wki3ygItvwEdp4gtqFSuWEfOdlvYNlQKcMl4gmyhrjwjQXiqpS0O53u1a60Wu+fpFWi76KZ3fFs/8z0fN1jARPCta8e1lAIk5oVgdh6+euPTZgABBSMT+48XFFC/kTNSuRDlkZ8dP7LD3tQIBQUiGtLa5tSiKfUfD/mdUUIsTL72ef//v/n76dQEArzwFytYRpavwg9smnpHCIJjkJWBaAZvEDHuXn+7EkLCoABBUEhbgZtBNG6lGLZbm7b3O8qhwfUrHJfKPWYfpahABTigaj1nXZ78eL0qRUew5sapDzqPdB6uYiNLaEADFgfcS8qPMMTFrHZeyDEJhSAsRVg69Narwd9t9N5lDiYolCvLURt/va3VRgTYyuQx/oBrnhBqXUYE2MpMJT1A4S8QGG1PnfrGxPGwMgKVGqNSknjUV+udOsHiHpBlcsHPBeMiJEU4IgyQ8JjKLbnsr4PR6lV+vFCLIXB6qzWz0f1RGYYZet80G6btF6rgrkN4l3egOExZP0NogjbMATm73zfoPkew+BETZr72EXdUgj2K8NoBWdJLgU8YV13hdxyVwtBpyeYEOE0EdjY5TdDCZ+qRMw3SLGWx6UAjqNcqqcAhzRplA7CyyIVZC2n01nNs+7TwIFAab1FgjzIM95TxHHuB1REBJPQSfoc4q1tY5fXtMi9Z2Tx1qVSh1muHRYsQ8l1qsSbamScBehS8aRzwiY+tcxKeAp8urT+ImR5FmxH8DrsOC1rTAuPC5M2t2MYJuUWVRByPSCF7Im/TnYXRZijkKUtt91evnjHQifhykohPiVJ+FpvBK3raRWecdHctuhnP+izVwbOAYoIZzD96O09krciJWJ/M3KMn3YIcSNoUkCxpVRqL/SyxmkhTCk82RBXgj6d/ofKtk5ff7jwxUfUv+U/r1Ef/jv77RimCL5ht4I+c6+/nz3Z9/aAISW/COeoW9PkiSvCc8qq1Aa3vaoEe+HjxS9/prLH19Sd88dNhSdihQ/l272yyjQqkSU8Y6Au1FNC6+u0oa/7j2tF13LyICo8LfrDSyXvRylMIp2eX1rbCxEsmyoNN9/WIRetchBD2D8/2a3HjU1MaEpSNqC/sStGudyAt4TBGhNYScIzEhWw2FVab4Qe5aK7RUCEYr3QejVtbGpKyfkr8Q3L71bma42xyyBZ8MilT9bY+lnFr8ycWITPB9eduAJC9HMS+vYfWeOHSuo1YKFJTPw3RF8BxH+yxmcrgP0UkxNtmDRct+/xSPEgDnk80Fs2XCWACaNULltBG7tFhVSkKhCuXfIpWHQeHAeOfqHAAYu3v1tIG5+qgFTSDNqUI09++QTfCgWOtpKp9wipCvDNSn9WkRkRCgPiWf+zIjXypd/QcPaD6DWpWtaEIRBU9ISUlTwVtjC4dEOCB10zbayRMZMZNKUyLMgACz2j9TqpXKcT1ASjOz09g9mlNYue7xGn2s/kVByJ/L8lNW7AqArQZuI73u5EjlPJEpyoB/OlShxD9CPKFkWZOjHNVEXYa0GbzoVUz6WHUcReHoBS3YMYwZn2znSZ4xYMVvb4wy2/lG7HKHJEtdE6xH1WqT7vogIbpCC1Oh29mOM8lNy7U9La7pRKK6J7zzXgGQ63QrsbUQ7jCSvkpojUXoML8FKn4413y+/REsQ+8824DMwsr0fygkQw8YIcN/FJiiRg5+XJbiqNz3XNSstkm36S7rNGKrFnKZKWxISR+56YP0iD76Efl2lzW3wZ8UrK7XFOaH/eB/4/hoBXBUfcyXuH/AZ43bXkyxrnZgAAAABJRU5ErkJggg=="
