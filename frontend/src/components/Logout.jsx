import React from "react";
import {Redirect} from "react-router-dom"

class Logout extends React.Component{

    constructor(props) {
        super(props);
        this.props.props.logout();
    }
    render() {
        return <p>{this.renderLogout()}</p>;
    }

    renderLogout(){
        if (this.props.props.user === 'anon'){
            return <Redirect to={'/'}/>;
        }
    }

}
export default Logout;