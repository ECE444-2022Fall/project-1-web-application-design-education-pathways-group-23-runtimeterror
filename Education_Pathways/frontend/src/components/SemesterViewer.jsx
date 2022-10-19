import React, { Component } from "react";
import './css/semester-viewer.css'

class SemesterViewer extends Component {
    addCourseBox(column_id) {
        var newCourseBox = document.createElement("li");
        newCourseBox.setAttribute("class", "drag-item");

        var newCourseName = document.getElementById("course_name_" + column_id).value;
        var isValid = (document.getElementById(newCourseName) === null) ? true : false;
        console.log(isValid);
        if (!isValid) {
            document.getElementById("notification-" + column_id).innerHTML = "You have already added this course.";
            return;
        }
        if (newCourseName == "") {
            document.getElementById("notification-" + column_id).innerHTML = "Please enter a valid course name.";
            return;
        }

        newCourseBox.innerHTML = newCourseName;
        newCourseBox.id = String(newCourseName);
        var courseList = document.getElementById(column_id);
        var coursesNumber = courseList.childElementCount;
        if (coursesNumber < 6) {
            courseList.appendChild(newCourseBox);
        } else {
            document.getElementById("notification-" + column_id).innerHTML = "You can add maximum 6 courses per semester.";
        }
    }

    render() {
        return (
            <div>
                <section className="section">
                    <h1>Semester Viewer</h1>
                </section>
                <div className="drag-container">
                    <ul className="drag-list">
                        <li className="drag-column drag-column-1">
                            <span className="drag-column-header">
                                <h2>Fall 2022</h2>
                            </span>
                            <ul className="drag-inner-list" id={1}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_1" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_1" />
                                <button type="button" className="form-button" onclick="addCourseBox(1)">Add</button>
                                <button type="button" className="form-button" onclick="removeCourseBox(1)">Remove</button>
                            </form>
                            <p className="notification" id="notification-1"> </p>
                        </li>
                        <li className="drag-column drag-column-2">
                            <span className="drag-column-header">
                                <h2>Winter 2023</h2>
                            </span>
                            <ul className="drag-inner-list" id={2}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_2" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_2" />
                                <button type="button" className="form-button" onclick="addCourseBox(2)">Add</button>
                                <button type="button" className="form-button" onclick="removeCourseBox(2)">Remove</button>
                            </form>
                            <p className="notification" id="notification-2"> </p>
                        </li>
                        <li className="drag-column drag-column-3">
                            <span className="drag-column-header">
                                <h2>Fall 2023</h2>
                            </span>
                            <ul className="drag-inner-list" id={3}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_3" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_3" />
                                <button type="button" className="form-button" onclick="addCourseBox(3)">Add</button>
                                <button type="button" className="form-button" onclick="removeCourseBox(3)">Remove</button>
                            </form>
                            <p className="notification" id="notification-3"> </p>
                        </li>
                        <li className="drag-column drag-column-4">
                            <span className="drag-column-header">
                                <h2>Winter 2024</h2>
                            </span>
                            <ul className="drag-inner-list" id={4}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_4" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_4" />
                                <button type="button" className="form-button" onclick="addCourseBox(4)">Add</button>
                                <button type="button" className="form-button" onclick="removeCourseBox(4)">Remove</button>
                            </form>
                            <p className="notification" id="notification-4"> </p>
                        </li>
                    </ul>
                </div>
            </div>
        );
    }
}
export default SemesterViewer;