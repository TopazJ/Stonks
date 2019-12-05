import React, {Component} from "react";
import CSRFToken from "./CSRFToken.jsx";
import {Redirect} from "react-router";

class CreateAccount extends Component{
    constructor(props) {
        super(props);
        this.state = {form:{email:'', username: '', password: ''}, created:false};
    }

    handleSubmit =(event)=>{
         event.preventDefault();
        const values = this.state.form;
        fetch('http://127.0.0.1:8000/api/create-account/', {
            method: 'POST',
            body: JSON.stringify(values),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken':event.target.csrfmiddlewaretoken.value
            }
        }).then(res => res.json())
        .then(data => {
            if (data.status!=='success'){
                alert(data.message);
            }
            else{
                this.setState({created:true});
            }
        })
        .catch(err => console.error("Error:", err));
    };


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

    checkRedirect(){
        if(this.state.created===true) {
            return <Redirect to={'/'}/>;
        }
    }

    render(){
        return <React.Fragment>
                <form className="p-4" onSubmit={this.handleSubmit}>
                    <CSRFToken />
                    <div className="form-group">
                        <label htmlFor="username">Email</label>
                        <input
                            type="email"
                            className="form-control"
                            id="email"
                            name="email"
                            placeholder="example@example.com"
                            onChange={this.handleInputChange}
                            required
                        />
                    </div>
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
                        Create Account
                    </button>
                </form>
            <p>{this.checkRedirect()}</p>
            </React.Fragment>

    }

}

export default CreateAccount;