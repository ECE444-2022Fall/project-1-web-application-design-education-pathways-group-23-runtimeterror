import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";
import {
  BrowserRouter as Router,
  Route,
  Switch,
  useLocation,
} from "react-router-dom";
import Navbar from "./Navbar";
import About from "./About";
import CourseDescriptionPage from "./CourseDescription";
import SearchResultDisplay from "./ResultDisplay";
import SemesterViewer from "./SemesterViewer";
import MinorProgress from "./MinorProgress";

function CourseDescription(props) {
  let query = useQuery();
  return <CourseDescriptionPage code={query.get("code")} />;
}

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

export default class Body extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: localStorage.getItem("username"),
      login: false,
    };
  }

  componentDidMount() {
    if (localStorage.getItem("username") !== "") {
      this.setState({ username: localStorage.getItem("username") });
    }
  }

  logOut = () => {
    localStorage.setItem("username", "");
    this.setState({ username: "" });
  };

  render() {
    return (
      <Router>
        <div>
          <Navbar />
        </div>
        <div>
          <Switch>
            <Route path="/about">
              <About />
              {/* <SearchResultDisplay /> */}
            </Route>
            <Route path="/search">
              <SearchResultDisplay />
            </Route>
            <Route
              exact
              path="/courseDetails/:code"
              render={(props) => <CourseDescriptionPage {...props} />}
            ></Route>
            <Route path="/semester-viewer">
              <SemesterViewer />
            </Route>
            <Route path="/minor-progress">
              <MinorProgress />
            </Route>
            <Route path="/">
              <SearchResultDisplay />
            </Route>
          </Switch>
        </div>
      </Router>
    );
  }
}
