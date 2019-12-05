import React, {Component} from "react";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state={accountNums:[], stocks:{}}
    }


    handleClickAccounts = () =>{
        fetch('http://127.0.0.1:8000/api/get-accounts/', {
            method: 'GET'
        }).then(res => res.json())
        .then(data => {
            console.log(data);
            const values = JSON.parse(data.data);
            values.map(x=>(
                this.setState(state => ({
                    accountNums: [
                        ...state.accountNums,
                        x.fields.account_no
                    ]
                }))
            ));
            console.log(this.state);
        })
        .catch(err => console.error("Error:", err));
    };

    handleClickStonks = () =>{
        fetch('http://127.0.0.1:8000/api/get-owns/', {
            method: 'GET',
            body: {account:this.state.accountNums[0]}
        }).then(res => res.json()).then(data => {
            console.log(data);
        }).catch(err=> console.error("Error", err));

    };

    render() {
        return <div>
            <p>
            Dashboard
            </p>
            <button onClick={this.handleClickAccounts}>Get STONKS</button>
            <button onClick={this.handleClickStonks}>Get STONKS</button>

        </div>;
    }
}

export default Dashboard;