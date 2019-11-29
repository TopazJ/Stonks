import React, { Component } from "react";
import LoginForm from "./LoginForm.jsx"

class App extends Component {
	render() {
		return (
			<React.Fragment>

				<LoginForm/>
				<p>This is a test.</p>
				<p>This is devel branch.</p>
			</React.Fragment>
		);
	}
}

export default App;
