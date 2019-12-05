import React from "react";
import CSRFToken from './CSRFToken.jsx';

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
        fetch('http://127.0.0.1:8000/auth/login/', {
            method: 'POST',
            body: JSON.stringify(values),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken':event.target.csrfmiddlewaretoken.value
            }
        }).then(res => res.json())
        .then(data => {
            if (data.status==='success'){
                this.props.props.login();
            }
            else{
                alert(data.status);
            }
        }).catch(err => console.error("Error:", err));
    };



    render() {
        return (
            <React.Fragment>
                <form className="p-4" onSubmit={this.handleSubmit}>
                    <CSRFToken />
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
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
            </React.Fragment>
        );
    }
}

export default LoginForm;
