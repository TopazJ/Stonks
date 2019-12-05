import {Component} from "react";

class Dashboard extends Component {

    handleClick = (event) =>{
        console.log("yeet");
        fetch('http://127.0.0.1:8000/auth/status/', {
            method: 'GET'
        }).then(res => res.json())
        .then(data => console.log(data))
        .catch(err => console.error("Error:", err));

    };


    render() {
        <p>Dashboard</p>
    }
}

export default Dashboard;