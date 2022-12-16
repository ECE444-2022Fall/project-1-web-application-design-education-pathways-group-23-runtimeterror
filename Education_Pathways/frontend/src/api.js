import axios from "axios";

export default axios.create({
  baseURL: "https://maple-course-selection.onrender.com/",
  withCredentials: true,
});
