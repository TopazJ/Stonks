import React, {Component} from "react";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state={accountNums:[], stocks:{}};
        this.fetchAccounts();
    }


    fetchAccounts = () =>{
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

    handleClickStonks = (event, data) =>{
        const test = JSON.stringify({account_no:data});
        console.log(test);
        fetch('http://127.0.0.1:8000/api/owns/', {
            method: 'POST',
            body: test,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json()).then(data => {
            console.log(data);
        }).catch(err=> console.error("Error", err));

    };

    render() {
        return <div>
            <p>
            Dashboard
            </p>

            <div className="dropdown">
                <button className="btn btn-warning dropdown-toggle" type="button" id="dropdownMenuButton"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Accounts
                </button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    {this.state.accountNums.map(yeet =>
                    {
                        return <a key={yeet} className="dropdown-item"
                                  onClick={((event => this.handleClickStonks(event, yeet)))}>{yeet}</a>;
                    })}
                </div>
            </div>
            <button onClick={this.fetchAccounts}>Get Accounts</button>
            <button onClick={this.handleClickStonks}>Get STONKS</button>

        </div>;
    }


    getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

export default Dashboard;