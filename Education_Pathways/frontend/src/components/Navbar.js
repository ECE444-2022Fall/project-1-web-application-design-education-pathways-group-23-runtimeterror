import React, { Component } from "react";
import "./css/navbar.css";
import "bootstrap/dist/css/bootstrap.css";
import logo from "./img/logo.png";
import { Navbar, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";

export default class NavbarComp extends Component {
	render() {
		return (
			<div>
				<Navbar bg="myBlue" variant="dark" sticky="top" expand="lg">
					<Navbar.Brand>
						<img src={logo} alt="" />{" "}
						<Nav.Link
							as={Link}
							to="/"
							style={{ color: "white", display: "inline" }}
						>
							Education Pathways
						</Nav.Link>
					</Navbar.Brand>

					<Navbar.Toggle />
					<Navbar.Collapse>
						<Nav>
							<Nav.Link as={Link} to="/semester-viewer">
								Semester Viewer
							</Nav.Link>
						</Nav>
						<Nav>
							<Nav.Link as={Link} to="/minor-progress">
								Minor Checker
							</Nav.Link>
						</Nav>
						<Nav>
							<Nav.Link as={Link} to="/about">
								About Us
							</Nav.Link>
						</Nav>
					</Navbar.Collapse>
				</Navbar>
			</div>
		);
	}
}
