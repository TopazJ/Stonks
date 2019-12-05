import React, {Component} from "react";
import StockTable from "./dashboard/StockTable.jsx";
import TransactionTable from "./TransactionTable.jsx";

class MarketMaker extends Component {

    constructor(props) {
        super(props);
        this.state = {transactions:[],headers:['ID','Exchange', 'Symbol', 'Company', 'Quantity', 'Price', 'Cost', 'Complete']};
        this.fetchTransactions();

    }

    completeTransaction = (id) => {
        console.log(id);
        fetch('http://127.0.0.1:8000/api/complete-transaction/', {
            method: 'POST',
            body: JSON.stringify({id:id}),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json())
        .then(data => {

            console.log(data);
            //TODO If statement here!

            this.setState({transactions:[]});
            this.fetchTransactions();
        })
        .catch(err => console.error("Error:", err));
    };

    fetchTransactions = () => {
        fetch('http://127.0.0.1:8000/api/get-mm-transactions/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        }).then(res => res.json())
        .then(data => {

            console.log(data);
            data.data.map(x=>{
               this.setState(state => ({
                    transactions: [
                        ...state.transactions,
                        {   id: x.id,
                            exc: x.trade.exchange,
                            sym: x.trade.symbol,
                            company:x.trade.company_name,
                            quan:x.quantity,
                            price:x.trade.price
                        }
                    ]
                }));
            });
        })
        .catch(err => console.error("Error:", err));
    };

    render() {
        return (
            <TransactionTable
            headers={this.state.headers}
            values={this.state.transactions}
            button={this.completeTransaction}
            />
        );
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

export default MarketMaker;