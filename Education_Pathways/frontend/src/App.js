import React from "react";
import BodyComp from "./components/Body.js";
import ReactComp from "./components/Footer.js";
import "./App.css";

function App() {
  return (
    <div>
      <div className="App">
        <BodyComp />
      </div>

      <div className="App">
        <ReactComp />
      </div>
    </div>
  );
}

export default App;
