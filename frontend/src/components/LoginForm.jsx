import React from 'react';
import DjangoCSRFToken from 'django-react-csrftoken'
import {Form} from 'react-bootstrap'

class LoginForm extends React.Component {

  handleSubmit(event){
    event.preventDefault();
    console.log("Submit!");
  }

  render(){
    return (
        <React.Fragment>
          <form className="p-4" onSubmit={this.handleSubmit}>
            <DjangoCSRFToken/>
            <div className="form-group">
              <label htmlFor="loginFormUsername">Email address</label>
              <input type="text" className="form-control" id="loginFormUsername"
                     placeholder="Username"/>
            </div>
            <div className="form-group">
              <label htmlFor="loginFormPassword">Password</label>
              <input type="password" className="form-control" id="loginFormPassword" placeholder="Password"/>
            </div>
            <button type="submit" className="btn btn-primary">Sign in</button>
          </form>
        </React.Fragment>
    )
  }
}

export default LoginForm;