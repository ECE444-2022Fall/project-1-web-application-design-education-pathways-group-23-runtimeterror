import React, { Component } from "react";
import "./css/semester-viewer.css";

class About extends Component {
  render() {
    return (
      <div className="body_text">
        <p>
          Welcome to CARTE's in-development tool for course selection at UofT.
          Maple allows for more intelligent course searching, by matching not
          just the terms you search, but ones relevant to them. The more terms
          you search for, the more relevant your results will be! Even try
          searching across disciplines for the courses that best cover each.
          <br></br>
          Whatever year you are looking for, Maple will also suggest courses in
          earlier years that will best help you to prepare. To get the most out
          of this, try searching for courses in a later year and see what is
          suggested for your current one.<br></br>
          We are looking for feedback to improve Maple and make it more useful
          for students. If you have ideas or suggestions, please{" "}
          <a href="mailto:alex.olson@utoronto.ca"> email us! </a> <br></br>
        </p>
        <p>
          <b>Development Team: </b>
        </p>
        <p>
          Alexander Olson <a href="https://carte.utoronto.ca/"> (CARTE)</a>{" "}
        </p>
        <p>
          Student team from{" "}
          <a href="https://shuiblue.github.io/UofT-ECE444/">ECE444-Fall2022</a>{" "}
          : Dean Yu, Ani Srikanth, Valentina Manferrari, Samir Khaki, Komila
          Rasulova, Mehak Kalra
        </p>
      </div>
    );
  }
}
export default About;
