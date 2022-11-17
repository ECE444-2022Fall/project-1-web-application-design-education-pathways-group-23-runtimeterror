import axios from "axios";

export default axios.create({
  baseURL: "https://dashboard.heroku.com/apps/maple-course-selection/deploy/github",
  withCredentials: true,
});
