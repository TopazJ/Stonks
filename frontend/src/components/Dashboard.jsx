import React, {Component} from "react";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state={accounts:{}, stocks:{}}
    }


    handleClick = (event) =>{
        console.log("yeet");
        fetch('http://127.0.0.1:8000/api/get-accounts/', {
            method: 'GET'
        }).then(res => res.json())
        .then(data => console.log(data))
        .catch(err => console.error("Error:", err));

    };

    render() {
        return <div>
            <p>
            Dashboard
            </p>
            <button onClick={this.handleClick}>Get STONKS</button>
        </div>;
    }
}

export default Dashboard;