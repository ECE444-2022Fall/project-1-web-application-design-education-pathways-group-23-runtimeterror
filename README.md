<a name="readme-top"></a>

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8523853&assignment_repo_type=AssignmentRepo)

# Maple

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#project-management">Project Management</a></li>
    <li><a href="#CI-CD">CI/CD</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Maple is a fork of the [Education Pathway project](https://github.com/ECE444-2022Fall/Assignment_1_starter_template) created by Team RuntimeTerror.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![React][React.js]][React-url]
* [![Flask][Flask]][Flask-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Make sure you have all the prerequisites installed
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/) (python-3.10.6)
* nodejs

To install nodejs, go to [nodejs download]( https://nodejs.org/en/download/). Add `npm` to `PATH` as global variable.
 
### Installation

#### 1. Clone the repository to your local machine
```sh
$ git clone https://github.com/ECE444-2022Fall/project-1-web-application-design-education-pathways-group-23-runtimeterror
```
#### 2. To run the app locally

+ Enter the repo directory
+ Create a virtual environment if you haven't done this before. Activate it. 
```powershell
# Windows
py -3 -m venv venv
venv\Scripts\activate

# For Mac and Linux, please check the link: https://flask.palletsprojects.com/en/2.2.x/installation/
```
+ Install dependencies (if you haven't done this before).
```powershell
pip install -r requirements.txt
```
+ Enter the `Education_Pathways/` directory, run the backend
```powershell
flask --app index --debug run
```
+ Enter the `Education_Pathways/frontend/` directory
+ Make sure the `baseURL` is set as `localhost:5000`
```javascript
# Education_Pathways/frontend/src/api.js
export default axios.create({
   baseURL: "http://localhost:5000/"
});
```
+ Make sure the proxy link in package.json is set as "http://localhost:5000/"
```json
// Part of Education_Pathways\frontend\package.json
"private": true,
"proxy": "http://localhost:5000/",
```

+ Build and run the frontend:
```powershell
npm run build
npm start
```
+ Then you will see the application at `localhost:3000`

#### 4. Build and Run with Docker

+ Change the proxy link in package. Remember to change it back to "http://localhost:5000/"
```json
// Part of Education_Pathways/frontend/package.json
"private": true,
"proxy": "http://host.docker.internal:5000/",
```

```powershell
# Under the root directory
docker compose up --build
```

#### 5. Deploy the project
+ Make sure the baseURL is set as [URL to your deployed project]
```javascript
// Education_Pathways/frontend/src/api.js
export default axios.create({
   baseURL: "[URL to your deployed project]" -- baseURL for deployment
});
```
+ Re-build the frontend to update the baseURL
```powershell
# Under the frontend/ directory
npm run build
```
+ Deploy your changes to heroku
```powershell
git push heroku main
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT MANAGEMENT -->
## Project Management

Maple uses [GitHub Projects](https://github.com/orgs/ECE444-2022Fall/projects/2/views/2) track progress on the implementation of User Stories and Bugfixes. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CI CD -->
## CI/CD
Maple uses [GitHub Actions](https://github.com/ECE444-2022Fall/project-1-web-application-design-education-pathways-group-23-runtimeterror/actions) for Continous Integration. Everytime a Pull Request is opened on the "develop" branch:
- [Python App](https://github.com/ECE444-2022Fall/project-1-web-application-design-education-pathways-group-23-runtimeterror/actions/workflows/python-app.yml) runs our Unit Tests and Integration tests on the Backend using Pytest
- [Docker Test](https://github.com/ECE444-2022Fall/project-1-web-application-design-education-pathways-group-23-runtimeterror/actions/workflows/docker.yml) builds the app using Docker and runs tests on the Frontend using Pytest and Selenium

Maple uses Heroku's GitHub integration to automatically deploy the main branch to: https://maple-course-selection.herokuapp.com/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* The ECE444 2022 teaching team for providing the [Assignment_1_starter_template](https://github.com/ECE444-2022Fall/Assignment_1_starter_template) for us to build upon
* This document was adapted from [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Flask]: https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff&style=for-the-badge
[Flask-url]: https://flask.palletsprojects.com/
