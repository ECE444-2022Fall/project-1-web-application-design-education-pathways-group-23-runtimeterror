import React, { Component } from "react";
import './css/semester-viewer.css';

import * as ReactDOM from 'react-dom';
import Dragula from 'react-dragula';
import API from '../api';

class SemesterViewer extends Component {
    constructor() {
        super();
        this.state = {
            major: "",
            year: 2022,
            minors: [],
            semesters: [{name: ""},{name: ""},{name: ""},{name: ""},{name: ""},{name: ""},{name: ""},{name: ""}],
            earned_credits: 0.0,
            planned_credits: 0.0
        };
        this.addCourseBox = this.addCourseBox.bind(this);
        this.closeForm = this.closeForm.bind(this);
        }

    componentDidMount () {
        //Initialize Dragula
        const container = Array.from(
            document.getElementsByClassName('drag-inner-list')
          );
        var drake = Dragula(container);
        drake.on('drop', (el, target, source) => {
            API.post("/api/swap_semester", {course: el.id, source_semester: source.id-1, target_semester: target.id-1}).then(res => {
                this.setState({
                    semesters: res.data.semesters,
                    earned_credits: res.data.earned_credits,
                    planned_credits: res.data.planned_credits
                },
                );
            });
         });

        //Load Student from backend
        API.get("/api/load_student").then(res => {
            if(res.status === 200) {
                this.setState({
                    major: res.data.major,
                    year: res.data.year,
                    minors: res.data.minors,
                    semesters: res.data.semesters,
                    earned_credits: res.data.earned_credits,
                    planned_credits: res.data.planned_credits
                },
                this.restoreSemsterViewer
                );
            }
            else if(res.status === 204) {
                this.openForm()
            }
        });
    }

    openForm() {
        if(document.getElementById("studentForm")){
            document.getElementById("studentForm").style.display = "block";
        }
    }
      
    closeForm() {
        if(document.getElementById("major").value === "true") {
            document.getElementById("notification-form").innerHTML = "Please select a major.";
            return;
            }
        if(document.getElementById("year").value === "true") {
            document.getElementById("notification-form").innerHTML = "Please select a graduation year.";
            return;
            }

        if(document.getElementById("studentForm")){
            document.getElementById("studentForm").style.display = "none";
        }
        // store info in backend here
        var major = document.getElementById("major").value;
        var year = document.getElementById("year").value;
        API.post("/api/create_student", {major:major, year:year}).then(res => {
            console.log(res)
            this.setState({
                major: res.data.major,
                year: res.data.year,
                minors: res.data.minors,
                semesters: res.data.semesters,
                earned_credits: res.data.earned_credits,
                planned_credits: res.data.planned_credits
                },
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
        
        API.post("/api/add_course", {semester: column_id-1, course: newCourseBox.id}).then(res => {
            this.setState({
                earned_credits: res.data.earned_credits,
                planned_credits: res.data.planned_credits
            },
            );
        });
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

        API.post("/api/remove_course", {semester: column_id-1, course: CourseName}).then(res => {
            this.setState({
                earned_credits: res.data.earned_credits,
                planned_credits: res.data.planned_credits
            },
            );
        });
        courseList.removeChild(courseBox);
    }

    render() {
        return (
            <div>
                <div class="form-popup" id="studentForm">
                    <form onSubmit={this.handleSubmit} class="form-container">
                        <label for="major"><b>Major</b></label>
                        <select id="major" name="major" required>
                            <option disabled selected value> -- select an option -- </option>
                            <option value="Chemical">Chemical</option>
                            <option value="Civil">Civil</option>
                            <option value="Electrical & Computer">Electrical & Computer</option>
                            <option value="Industrial">Industrial</option>
                            <option value="Materials">Materials</option>
                            <option value="Mechanical">Mechanical</option>
                            <option value="Mineral">Mineral</option>
                            <option value="EngSci">EngSci</option>
                        </select>

                        <label for="year"><b>Graduation Year</b></label>
                        <select id="year" name="year" required>
                            <option disabled selected value> -- select a year -- </option>
                            <option value="2023">2023</option>
                            <option value="2024">2024</option>
                            <option value="2025">2025</option>
                            <option value="2026">2026</option>
                            <option value="2027">2027</option>
                            <option value="2028">2028</option>
                        </select>
                        <p> By pressing Submit, you consent to the use of cookies </p>
                        <p className="notification" id="notification-form"> </p>
                        <button type="button" class="btn" onClick={this.closeForm}>Submit</button>
                    </form>
                </div>
                
                <section className="section">
                    <h1>Semester Viewer</h1>
                </section>

                <div className="drag-container">
                    <ul className="drag-list">
                        <li className="drag-column">
                            {/* For Dean to add student info from backend */}              
                            <table>
                                <tr>
                                    <td rowspan="2"><span className="student-info-header"><h2>Current Status</h2></span></td>
                                    <td className="student-info">Your Major is: {this.state.major}</td>
                                </tr>
                                <tr>
                                    <td className="student-info">Earned Credits: {this.state.earned_credits}</td>
                                    <td className="student-info">Planned Credits: {this.state.planned_credits}</td>
                                </tr>
                            </table>
                            
                        </li>
                        <li className="drag-column">
                            <span className="drag-column-header">
                                <h2>{this.state.semesters[0].name}</h2>
                            </span>
                            <ul className="drag-inner-list" id={1}>
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
                            <ul className="drag-inner-list" id={2}>
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
                            <ul className="drag-inner-list" id={3}>
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
                            <ul className="drag-inner-list" id={4}>
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
                            <ul className="drag-inner-list" id={5}>
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
                            <ul className="drag-inner-list" id={6}>
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
                            <ul className="drag-inner-list" id={7}>
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
                            <ul className="drag-inner-list" id={8}>
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