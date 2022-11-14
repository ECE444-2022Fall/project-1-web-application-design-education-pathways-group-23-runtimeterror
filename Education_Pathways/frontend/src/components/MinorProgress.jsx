import React, { Component } from "react";
import { Form, ListGroup } from "react-bootstrap";
import './css/minor-progress.css';


import API from '../api';

class MinorProgress extends Component{
    constructor() {
        super()

        this.checkIcon = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/800px-Sign-check-icon.png"
        this.inprogressIcon = "https://static.thenounproject.com/png/3557919-200.png"
        this.minorList = ["Engineering Business", "Artificial Intelligence"]
    }

    componentDidMount(){
        API.get()
    }

    render(){
        return (
        <div>
            <div id="minor-select-container" class="section">
                <label for="minor"><b>Minor</b></label>
                <Form.Select name="minor" onSubmit={this.handleSubmit}>
                    <option>Select Minor</option>
                    {this.minorList.map((minor_name) => {
                        return <option value={{minor_name}}> {minor_name} </option>
                    })}
                    {/* <option value="Engineering Business">Engineering Business</option>
                    <option value="Artificial Intelligence">Artificial Intelligence</option> */}
                </Form.Select>
            </div>
            <div id="requirements-container" class="section">
                <ListGroup>
                    <ListGroup.Item>
                        <div class="single-requirement-container">
                            <div class="single-requirement-">
                                <h3>Requirement One</h3>
                                <h4>Must take:</h4>
                                <p>APS360</p>
                            </div>
                            <div class="single-requirement-check-container">
                                <img src={ this.checkIcon }></img>
                            </div>
                        </div>
                    </ListGroup.Item>
                    <ListGroup.Item>
                        <div class="single-requirement-container">
                            <div class="single-requirement-">
                                <h3>Requirement Two</h3>
                                <h4>Select one from:</h4>
                                <p>CSC263H1, ECE345H1, ECE358H1, MIE335H1</p>
                            </div>
                            <div class="single-requirement-check-container">
                                <img src={this.inprogressIcon}></img>
                            </div>
                        </div>
                    </ListGroup.Item>
                </ListGroup>
            </div>
        </div>
        )
    }
}
export default MinorProgress;


