import React, { Component } from "react";
import axios from "axios";
import Result from "./Results";
import "./css/Result.css";
import Label from "./Label";
import "./css/styles.css";
import API from "../api";

class SearchResultDisplay extends Component {
  constructor() {
    super();
    this.state = {
      input: "",
      results: [],
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ input: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    this.getData(this.state.input);
  }

  getData = (input) => {
    var minor = document.getElementById("minor").value;
    var mse_theme = document.getElementById("mse_theme").value;
    API.post("/api/search", {
      input: input,
      minor: minor,
      mse_theme: mse_theme,
    }).then((res) => {
      if (res.status === 200) {
        this.setState({ results: [] });
        console.log(res.data.length);
        if (res.data.length > 0) {
          let len = res.data.length;
          let result_temp = [];
          result_temp.push(<Label></Label>);
          for (let i = 0; i < len; i++) {
            result_temp.push(
              <Result
                key={res.data[i]._id}
                course_code={res.data[i].code}
                course_name={res.data[i].name}
                division={res.data[i].department}
                faculty={res.data[i].division}
                starred={res.data[i].starred}
              ></Result>
            );
          }
          this.setState({ results: result_temp });
        } else if (res.data.length === 0) {
          alert("No courses found");
        } else {
          let result_temp = [];
          result_temp.push(<Label></Label>);
          result_temp.push(
            <Result
              key={res.data.course._id}
              course_code={res.data.course.code}
              course_name={res.data.course.name}
              division={res.data.department}
              faculty={res.data.division}
              starred={res.data.starred}
            ></Result>
          );
          this.setState({ results: result_temp });
        }
      } else if (res.status === 400) {
        alert("System Error. Please refresh");
      }
    });
  };

  render() {
    return (
      <div className="SearchQuery">
        <div style={{ marginTop: "7%" }}>
          <h1 style={{ fontSize: "350%" }}>MAPLE</h1>
          <form onSubmit={this.handleSubmit} className={"search"}>
            <div class="container">
              <input
                placeholder={"Search for course code or course name"}
                className={"text-input"}
                type="text"
                value={this.state.input}
                onChange={this.handleChange}
              />
              <input type="submit" value="Search" className={"submit-button"} />
            </div>
            <div class="filters-box container">
              <p>Filter by</p>
              <label for="minor" class="filter-label">
                Minor
              </label>
              <select id="minor" name="minor" class="filter-dropdown">
                <option value="" class="filter-default">
                  {" "}
                  -- select a minor --{" "}
                </option>
                <option value="AEMINENV">Environmental Engineering</option>
                <option value="AEMINADVM">Advanced Manufacturing</option>
                <option value="AEMINAIEN">Artificial Intelligence</option>
                <option value="AEMINBIO">Bioengineering</option>
                <option value="AEMINBUS">Engineering Business</option>
                <option value="AEMINMUSP">Engineering Music Performance</option>
                <option value="AEMINGLOB">Global Leadership</option>
                <option value="AEMINNANO">Nanoengineering</option>
                <option value="AEMINRAM">Robotics and Mechantronics</option>
                <option value="AEMINENR">Sustainable Energy</option>
              </select>
              <label for="mse-theme" class="filter-label">
                MSE Theme
              </label>
              <select id="mse_theme" name="mse-theme" class="filter-dropdown">
                <option value="" class="filter-default">
                  {" "}
                  -- select a theme --{" "}
                </option>
                <option value="Biomaterials">Biomaterials</option>
                <option value="Design of Materials">Design of Materials</option>
                <option value="Sustainable Materials Processing">
                  Sustainable Materials Processing
                </option>
                <option value="Manufacturing with Materials">
                  Manufacturing with Materials
                </option>
              </select>
            </div>
          </form>
        </div>

        <div className={"search-result-display"}>{this.state.results}</div>
      </div>
    );
  }
}

export default SearchResultDisplay;
