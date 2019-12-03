import React from "react";
import CSRFToken from './csrftoken.jsx';

class LoginForm extends React.Component {

    constructor(props){
        super(props);
        this.state = {form:{username: '', password: ''}};
    }

    handleInputChange = (event) => {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState(state => ({
            form: {
                ...state.form,
                [name]: value
            }
        }))
    };

    handleSubmit = (event) => {
        event.preventDefault();
        const values = this.state.form;
        console.log("Submit!");
        console.log(event.target);
        console.log(JSON.stringify(values));
        fetch('http://127.0.0.1:8000/login/', {
            method: 'POST',
            body: JSON.stringify(values),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken':event.target.csrfmiddlewaretoken.value
            }
        }).then(res => console.log(res));//res.json());
    // .then(data => console.log(data))
    // .catch(err => console.error("Error:", err));
    };

    handleClick = (event) =>{
        event.preventDefault();
        console.log("yeet");
    };

    render() {
        return (
            <React.Fragment>
                <form className="p-4" onSubmit={this.handleSubmit}>
                    <CSRFToken />
                    <div className="form-group">
                        <label htmlFor="username">Email address</label>
                        <input
                            type="text"
                            className="form-control"
                            id="username"
                            name="username"
                            placeholder="Username"
                            onChange={this.handleInputChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            name="password"
                            className="form-control"
                            id="password"
                            placeholder="Password"
                            onChange={this.handleInputChange}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Sign in
                    </button>
                </form>
                <button type="submit" onClick={this.handleClick}>
                    Test
                </button>
            </React.Fragment>
        );
    }
}

export default LoginForm;
