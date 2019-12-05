import React, {Component} from "react";

class TransactionTable extends Component {


    renderHeaders=()=>{
        return this.props.headers.map(head => {
            return <th key={head} scope="col">{head}</th>;}
        );
    };

    renderRows=()=>{
      return this.props.values.map((val, index) => {

          return <tr key={val.exc+val.sym+val.quan}>
              {/*<th scope="row">{index}</th>*/}
              <td>{val.id}</td>
              <td>{val.exc}</td>
              <td>{val.sym}</td>
              <td>{val.company}</td>
              <td>{val.quan}</td>
              <td>{val.price}</td>
              <td>{val.quan * val.price}</td>
              <td><button onClick={() => this.props.button(val.id)} className="btn btn-success">Complete</button></td>
          </tr>;
      })
    };

    render() {
        return <table className="table">
            <thead>
            <tr>
                {this.renderHeaders()}
            </tr>
            </thead>
            <tbody>
                {this.renderRows()}
            </tbody>
        </table>;
    }
}

export default TransactionTable;