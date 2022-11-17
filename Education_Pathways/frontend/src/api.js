import axios from "axios";

export default axios.create({
  baseURL: "https://maple-course-selection.herokuapp.com/",
  withCredentials: true,
});
