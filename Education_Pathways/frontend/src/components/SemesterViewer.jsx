import React, { Component , useEffect} from "react";
import './css/semester-viewer.css';

import * as ReactDOM from 'react-dom';
import Dragula from 'react-dragula';
import API from '../api';

class SemesterViewer extends Component {
    constructor() {
        super();
        this.state = {
            major: "",
            year: 1,
            minors: [],
            semesters: [{name: ""},{name: ""},{name: ""},{name: ""},{name: ""},{name: ""},{name: ""},{name: ""}]
        };
        this.addCourseBox = this.addCourseBox.bind(this);
        }

    componentDidMount () {
        API.get("/api/load_student").then(res => {
            this.setState({
                major: res.data.major,
                year: res.data.year,
                minors: res.data.minors,
                semesters: res.data.semesters
            },
            this.restoreSemsterViewer
            );
        });
    }
    

    restoreSemsterViewer() {
        for(let i=0; i<this.state.semesters.length; i++){
            
            for(let j=0; j<this.state.semesters[i].courses.length; j++) {
                var newCourseBox = document.createElement("li");
                newCourseBox.className = "drag-item";

                var newCourseName = this.state.semesters[i].courses[j];
                newCourseBox.innerHTML = newCourseName;
                newCourseBox.id = String(newCourseName);

                var courseList = document.getElementById(i+1);
                courseList.appendChild(newCourseBox);
            }
        } 
        return;
    }

    addCourseBox(column_id) {
        var newCourseBox = document.createElement("li");
        newCourseBox.className = "drag-item";

        var newCourseName = document.getElementById("course_name_" + column_id).value;
        var isValid = (document.getElementById(newCourseName) === null) ? true : false;
        // console.log(isValid);
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
        if (coursesNumber > 6) {
            document.getElementById("notification-" + column_id).innerHTML = "You can add maximum 6 courses per semester.";
            return;
        } 
        
        API.post("/api/add_course", {semester: column_id-1, course: newCourseBox.id})
        courseList.appendChild(newCourseBox);
        document.getElementById("notification-" + column_id).innerHTML = "";
    }

    removeCourseBox(column_id){
        var CourseName = document.getElementById("course_name_" + column_id).value;
        var courseBox = document.getElementById(CourseName);
        var courseList = document.getElementById(column_id);

        if (courseBox === null)  {
            document.getElementById("notification-" + column_id).innerHTML = "This course does not exist.";
            return;
        }

        API.post("/api/remove_course", {semester: column_id-1, course: CourseName})
        courseList.removeChild(courseBox);
    }
    
    dragulaDecorator = (componentBackingInstance) => {
        if (componentBackingInstance) {
            let options = {};
            Dragula([componentBackingInstance], options)
            .on('drag', function (el) {
                // add 'is-moving' class to element being dragged
                el.classList.add('is-moving');
            })
            .on('dragend', function (el) {
                // remove 'is-moving' class from element after dragging has stopped
                el.classList.remove('is-moving');
                // add the 'is-moved' class for 600ms then remove it
                window.setTimeout(function () {
                    el.classList.add('is-moved');
                    window.setTimeout(function () {
                        el.classList.remove('is-moved');
                    }, 600);
                }, 100);
            });
        }
    };

    render() {
        return (
            <div>
                <section className="section">
                    <h1>Semester Viewer</h1>
                </section>
                <div className="drag-container">
                    <ul className="drag-list">
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[0].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={1} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_1" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_1" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('1')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('1')}>Remove</button>
                            </form>
                            <p className="notification" id="notification-1"> </p>
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[1].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={2} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_2" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_2" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('2')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('2')}>Remove</button>
                            </form>
                            <p className="notification" id="notification-2"> </p>
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[2].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={3} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_3" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_3" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('3')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('3')}>Remove</button>
                            </form>
                            <p className="notification" id="notification-3"> </p>
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[3].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={4} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_4" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_4" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('4')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('4')}>Remove</button>
                            </form>
                            <p className="notification" id="notification-4"> </p>
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[4].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={5} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_5" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_5" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('5')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('5')}>Remove</button>
                            </form>
                            <p className="notification" id="notification-5"> </p>
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[5].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={6} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_6" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_6" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('6')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('6')}>Remove</button>
                            </form>
                            <p className="notification" id="notification-6"> </p>
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[6].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={7} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_7" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_7" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('7')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('7')}>Remove</button>
                            </form>
                            <p className="notification" id="notification-7"> </p>
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[7].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={8} ref={this.dragulaDecorator}>
                            </ul>
                            <form className="add-course">
                                <label htmlFor="course_name_8" className="form-input">Course Name:</label>
                                <input type="text" className="form-input" id="course_name_8" />
                                <button type="button" className="form-button" onClick={() => this.addCourseBox('8')}>Add</button>
                                <button type="button" className="form-button" onClick={() => this.removeCourseBox('8')}>Remove</button>
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