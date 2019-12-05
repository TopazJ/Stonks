import React, {Component} from "react";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state={accountNums:[], stocks:{}, show_account:true, selected_account:null,
            addMoneyForm:{CCName:'',CCNum:'',CCV:'',cashMoney:0}, buyStockForm:{symbol:'', quantity: ''}};
        this.fetchAccounts();
    }


    fetchAccounts = () =>{
        fetch('http://127.0.0.1:8000/api/get-accounts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
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

    handleBuyStockChange = (event) => {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        console.log(value);
        this.setState(state => ({
            buyStockForm: {
                ...state.buyStockForm,
                [name]: value
            }
        }))
    };

    handleClickStonks = (event, accountid) =>{
        const test = JSON.stringify({account_no:accountid});
        fetch('http://127.0.0.1:8000/api/owns/', {
            method: 'POST',
            body: test,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json()).then(data => {
            this.setState({show_account:false, selected_account:accountid});
            console.log(data);
        }).catch(err=> console.error("Error", err));

    };

    handleAddMoney=(event) => {
        if (event.target.checkValidity()) {
            event.preventDefault();
            console.log(this.state.addMoneyForm);
            const values = {
                account_no: this.state.selected_account,
                amount: parseInt(this.state.addMoneyForm.cashMoney)
            };
            console.log(values);
            fetch('http://127.0.0.1:8000/api/add-money/', {
                method: 'POST',
                body: JSON.stringify(values),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            }).then(res => res.json())
                .then(data => {
                    console.log(data);
                }).catch(err => console.error("Error:", err));
        }
    };

    handleMoneyInput = (event) =>{
       const target = event.target;
       const value = target.value;
       const name = target.name;
       console.log(value);
       this.setState(state => ({
            addMoneyForm: {
                ...state.addMoneyForm,
                [name]: value
            }
       }))
    };

    handleBuyStock=(event)=>{
        if (event.target.checkValidity()) {
            console.log(event.target);
            event.preventDefault();
            console.log("Trying to buy a stock");
        }
    };

    render() {
        return <div className="container">
            <div className="row">
                <div className="col-sm">
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
                    <p hidden={this.state.show_account}>
                        Selected Account Number: {this.state.selected_account}
                    </p>
                    <form className="px-4 py-3" onSubmit={this.handleBuyStock} hidden={this.state.show_account}>
                        <div className="form-group">
                            <label htmlFor="exampleDropdownStockSymbol">Stock Symbol</label>
                            <input onChange={this.handleBuyStockChange} type="text" className="form-control"
                                   id="exampleDropdownStockSymbol" pattern="[A-Z]{1,6}" required/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="exampleQuantity">Quantity</label>
                            <input onChange={this.handleBuyStockChange}
                                type="text" className="form-control" id="exampleQuantity" pattern="^[1-9][0-9]*$" required/>
                        </div>
                        <button type="submit" className="btn btn-primary">Purchase Stocks</button>
                    </form>

                </div>
                <div className="col-sm" hidden={this.state.show_account}>
                    <form className="px-4 py-3" onSubmit={this.handleAddMoney}>
                        <div className="form-group">
                            <label htmlFor="exampleDropdownFormName">Name on Credit Card</label>
                            <input type="text" className="form-control" id="exampleDropdownFormName" name="CCName"
                                    pattern="[A-Z, ,a-z]{1,32}" required onChange={this.handleMoneyInput}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="exampleDropdownFormEmail1">Credit Card Number</label>
                            <input type="text" className="form-control" id="exampleDropdownFormEmail1" name="CCNum"
                                   pattern="[0-9]{16}" required onChange={this.handleMoneyInput}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="exampleDropdownFormPassword1">CCV</label>
                            <input type="text" className="form-control" id="exampleDropdownFormPassword1" name="CCV"
                                   pattern="[0-9]{3}" required onChange={this.handleMoneyInput}/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="fundAmount">Deposit Amount</label>
                            <input type="text" className="form-control" id="fundsAmount" name="cashMoney"
                                   placeholder="0" pattern="^[1-9][0-9]*$" onChange={this.handleMoneyInput} required/>
                        </div>
                        <button type="submit" className="btn btn-primary">Add Funds</button>
                    </form>
                </div>
            </div>
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