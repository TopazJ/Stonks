import React, { Component } from "react";
import { HashLink } from "./hashLink.js";
import {Router} from "react-router-dom";

class NavBar extends Component {
    render() {
        const topButtonStyle = {
            position: "fixed",
            bottom: "2vh",
            right: "2vw"
        };

        return (
            <React.Fragment>
                <nav className="navbar navbar-expand-lg bg-success navbar-light">
                    <a className="navbar-brand" href="#">Stonks</a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText"
                            aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarText">
                        <ul className="navbar-nav mr-auto">
                            {this.renderNavLinks()}
                        </ul>
                    </div>
                </nav>
                <button
                    className="btn btn-success rounded float-right"
                    style={topButtonStyle}
                    onClick={() => window.scrollTo(0, 0)}
                >
                    Top
                </button>
            </React.Fragment>
        );
    }

    renderNavLinks() {
        return this.props.navLinks.map(l => (
            <li className="nav-item">
                 <a key={l.id}
                    className="nav-link"
                    href={"#" + l.id}
                 >
                {l.text}
                </a>
            </li>

        ));
    }
}

export default NavBar;