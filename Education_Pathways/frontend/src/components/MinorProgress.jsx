import React, { Component } from "react";
import { Form, ListGroup } from "react-bootstrap";
import "./css/minor-progress.css";

import API from "../api";

class MinorProgress extends Component {
  constructor() {
    super();

    this.checkIcon =
      "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/800px-Sign-check-icon.png";
    this.inprogressIcon =
      "https://static.thenounproject.com/png/3557919-200.png";
    this.minorList = ["Engineering Business", "Artificial Intelligence"];
    this.state = {
      minor_name: "",
      completion: [],
    };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();
    this.getData();
  }

  getData() {
    let ele = document.querySelector("#minor-select");
    this.setState({ minor_name: ele.options[ele.selectedIndex].text }, () => {
      this.getRequirements();
    });
  }

  getRequirements() {
    API.post("/api/get_minor_completion", {
      minor_name: this.state.minor_name,
    }).then((res) => {
      if (res.status == 200) {
        this.setState({ completion: res.data.completion });
      } else {
        alert("Minor not found");
      }
    });
  }

  getRequirementElements() {
    return this.state.completion.map((req, idx) => {
      let requirement_list = req[0];
      let satisfied = req[1];

      return (
        <ListGroup.Item key={idx}>
          <div class="single-requirement-container">
            <div class="single-requirement-courselist-container">
              <h3>Requirement {idx+1}</h3>
              {
                requirement_list.length == 1 ? (
                    <h4>Must take:</h4>
                ) : (
                    <h4>Select one from:</h4>
                )
              }
              <p>{requirement_list.join(", ")}</p>
            </div>

            <div class="single-requirement-check-container">
              <img src={satisfied? this.checkIcon : this.inprogressIcon}></img>
            </div>
          </div>
        </ListGroup.Item>
      );
    });
  }

  render() {
    return (
      <div>
        <div id="minor-select-container" class="section">
          <label for="minor">
            <b>Minor</b>
          </label>
          <Form.Select
            id="minor-select"
            name="minor"
            onChange={this.handleSubmit}
          >
            <option>Select Minor</option>
            {this.minorList.map((minor_name) => {
              return <option value={{ minor_name }}> {minor_name} </option>;
            })}
            {/* <option value="Engineering Business">Engineering Business</option>
                    <option value="Artificial Intelligence">Artificial Intelligence</option> */}
          </Form.Select>
        </div>
        <div id="requirements-container" class="section">
          <ListGroup>
            {/* <ListGroup.Item>
              <div class="single-requirement-container">
                <div class="single-requirement-">
                  <h3>Requirement One</h3>
                  <h4>Must take:</h4>
                  <p>APS360</p>
                </div>
                <div class="single-requirement-check-container">
                  <img src={this.checkIcon}></img>
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
            </ListGroup.Item> */}
            {this.getRequirementElements()}
          </ListGroup>
        </div>
      </div>
    );
  }
}
export default MinorProgress;
