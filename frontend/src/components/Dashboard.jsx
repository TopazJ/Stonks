import React, {Component} from "react";
import StockTable from "./dashboard/StockTable.jsx";
import OwnedTable from "./OwnedTable.jsx";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state={accounts:[],stocks:{}, show_account:true, selected_account:null, account_balance:null,
            addMoneyForm:{CCName:'',CCNum:'',CCV:'',cashMoney:0}, buyStockForm:{symbol:'', quantity: ''},
            transactions:[], transaction_headers:['Exchange', 'Symbol', 'Company', 'Quantity', 'Price', 'Cost', 'Completed'], owns:[]};
        this.fetchAccounts();
    }

    fetchTransactions = () => {
        const values = {account_no: this.state.selected_account};
        console.log(values);
        fetch('http://127.0.0.1:8000/api/get-transactions/', {
            method: 'POST',
            body: JSON.stringify(values),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json())
        .then(data => {

            console.log(data);
            //TODO if statement here!
            this.setState({transactions:[]});
            data.data.map(x=>{
               this.setState(state => ({
                    transactions: [
                        ...state.transactions,
                        {exc: x.trade.exchange,
                            sym: x.trade.symbol,
                            company:x.trade.company_name,
                            quan:x.quantity,
                            price:x.trade.price,
                            completed:x.complete
                        }
                    ]
                }));
            });
        })
        .catch(err => console.error("Error:", err));
    };

    fetchAccounts = () =>{
        fetch('http://127.0.0.1:8000/api/get-accounts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json())
        .then(data => {
            const values = JSON.parse(data.data);
            values.map(x=>(
                this.setState(state => ({

                    accounts: [
                        ...state.accounts,
                        {accountNum: x.fields.account_no,
                        balance:x.fields.balance}
                    ]
                }))
            ));
        })
        .catch(err => console.error("Error:", err));
    };

    fetchOwns=()=>{
        fetch('http://127.0.0.1:8000/api/owns/', {
            method: 'POST',
            body: JSON.stringify({account_no:this.state.selected_account}),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json())
        .then(data => {
            const values = JSON.parse(data.data);
            values.map(x=>{
               this.setState(state => ({
                    owns: [
                        ...state.owns,
                        // {exc: x.trade.exchange,
                        //     sym: x.trade.symbol,
                        //     company:x.trade.company_name,
                        //     quan:x.quantity,
                        //     price:x.trade.price
                        // }
                    ]
                }));
            });
        })
        .catch(err => console.error("Error:", err));
    };

    handleBuyStockChange = (event) => {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState(state => ({
            buyStockForm: {
                ...state.buyStockForm,
                [name]: value
            }
        }))
    };

    handleClickStonks = (event, accountid, accountbalance) =>{
        const test = JSON.stringify({account_no:accountid});
        fetch('http://127.0.0.1:8000/api/owns/', {
            method: 'POST',
            body: test,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json()).then(data => {
            this.setState({show_account:false, selected_account:accountid, account_balance:accountbalance});
            this.fetchTransactions();
            this.fetchOwns();
        }).catch(err=> console.error("Error", err));

    };

    handleAddMoney=(event) => {
        if (event.target.checkValidity()) {
            event.preventDefault();
            const values = {
                account_no: this.state.selected_account,
                amount: parseInt(this.state.addMoneyForm.cashMoney)
            };
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
                    if (data.status === "success"){
                        this.setState(
                            {account_balance:parseInt(this.state.account_balance)+parseInt(this.state.addMoneyForm.cashMoney)});
                //         const accountNum =this.state.selected_account;
                //         const balance = this.state.account_balance;
                //         this.setState(state => ({
                //         accounts: [
                //             ...state.accounts,
                //             {[accountNum]:accountNum, [balance]:balance}
                //     ]
                // }));
                    }
                }).catch(err => console.error("Error:", err));
        }
    };

    handleMoneyInput = (event) =>{
       const target = event.target;
       const value = target.value;
       const name = target.name;
       this.setState(state => ({
            addMoneyForm: {
                ...state.addMoneyForm,
                [name]: value
            }
       }))
    };

    handleBuyStock=(event)=>{
        if (event.target.checkValidity()) {
            event.preventDefault();
            const values = {
                stock: this.state.buyStockForm.symbol,
                quantity: parseInt(this.state.buyStockForm.quantity)
            };
            console.log(values);
            fetch('http://127.0.0.1:8000/api/buy/', {
                method: 'POST',
                body: JSON.stringify(values),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            }).then(res => res.json())
                .then(data => {
                    this.fetchTransactions();
                    console.log(data);
                }).catch(err => console.error("Error:", err));
        }
    };

    handleSell=(symbol, quantity)=>{
        console.log(symbol, quantity);
        if (quantity>0) {
            fetch('http://127.0.0.1:8000/api/sell/', {
                method: 'POST',
                body: JSON.stringify({symbol: symbol, quantity: quantity}),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            }).then(res => res.json())
                .then(data => {

                    console.log(data);
                    //TODO If statement here!

                    this.setState({transactions: []});
                    this.fetchOwns();
                })
                .catch(err => console.error("Error:", err));
        }
        else{
            alert("Please enter a quantity greater than 0");
        }
    };

    displayList=()=>{
        return this.state.accounts.map(yeet =>
        {
            return <a key={yeet.accountNum} className="dropdown-item"
                      onClick={((event => this.handleClickStonks(event, yeet.accountNum, yeet.balance)))}>
                {yeet.accountNum+" - "+yeet.balance}</a>;
        })
    };

    render() {
        return<React.Fragment>
            <div className="container">
                <div className="row">
                    <div className="col-sm">
                        <div className="dropdown">
                            <button className="btn btn-warning dropdown-toggle" type="button" id="dropdownMenuButton"
                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Accounts
                            </button>
                            <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                {this.displayList()}
                            </div>
                        </div>
                        <p hidden={this.state.show_account}>
                            Selected Account Number: {this.state.selected_account}
                            <br/>
                            Selected Account Balance {this.state.account_balance}
                        </p>
                        <form className="px-4 py-3" onSubmit={this.handleBuyStock} hidden={this.state.show_account}>
                            <div className="form-group">
                                <label htmlFor="exampleDropdownStockSymbol">Stock Symbol</label>
                                <input onChange={this.handleBuyStockChange} type="text" className="form-control"
                                       name="symbol" id="exampleDropdownStockSymbol" pattern="[A-Z]{1,6}" required/>
                            </div>
                            <div className="form-group">
                                <label htmlFor="exampleQuantity">Quantity</label>
                                <input onChange={this.handleBuyStockChange}
                                      name="quantity" type="text" className="form-control" id="exampleQuantity" pattern="^[1-9][0-9]*$" required/>
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
            </div>
            <div className="container" hidden={this.state.show_account}>

                <OwnedTable headers = {['Exchange', 'Symbol', 'Company', 'Quantity', 'Price', 'Cost', 'Sell', 'Quantity Sell']}
                                  values = {this.state.owns} button = {this.handleSell}/>

                <StockTable headers = {this.state.transaction_headers} values={this.state.transactions}/>


            </div>
        </React.Fragment>;
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