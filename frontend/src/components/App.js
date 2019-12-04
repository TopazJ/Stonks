import React, { Component } from "react";
import {Switch, Route, BrowserRouter} from "react-router-dom";
import LoginForm from "./LoginForm.jsx"
import "./App.css"
import NavBar from "./navigation/NavBar.jsx";
import Dashboard from "./Dashboard.jsx";

class App extends Component {
	state = {
		homeLinks:[
			{id:'about',text:'About'},
			{id:'contact', text:'Contact'},
			{id:'test', text:'Test'}],
		navLinks:[
			{id:'dashboard', text:'Dashboard', component:Dashboard},
			{id:'login', text:'Login', component:LoginForm}
		]
	};

	render() {
		return (
			<BrowserRouter>
			<React.Fragment>
				<NavBar navLinks={this.state.homeLinks}/>
				<LoginForm/>
				<Switch>
					{this.state.navLinks.map(link => (
						<Route
							key={link.id}
							path={"/" + link.id}
							render={() => (
								<link.component/>
							)}
						/>
					))}
				</Switch>
			</React.Fragment>
			</BrowserRouter>
		);
	}
}

export default App;
