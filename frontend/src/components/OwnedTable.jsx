import React, {Component} from "react";

class OwnedTable extends Component {

    constructor(props) {
        super(props);
        this.state={form:{quantity:0}};
    }


    renderHeaders=()=>{
        return this.props.headers.map(head => {
            return <th key={head} scope="col">{head}</th>;}
        );
    };

    renderRows=()=>{
      return this.props.values.map((val) => {

          return <tr key={val.exc+val.sym+val.quan}>
              <td>{val.exc}</td>
              <td>{val.sym}</td>
              <td>{val.company}</td>
              <td>{val.quan}</td>
              <td>{val.price}</td>
              <td>{val.quan * val.price}</td>
              <td><button onClick={() => this.props.button(val.sym, this.state.form.quantity)} className="btn btn-primary">Sell</button></td>
              <td><input
                            type="number"
                            name="quantity"
                            className="form-control"
                            id="quantity"
                            placeholder="Sell Quantity"
                            min="1"
                            onChange={this.handleInputChange}
                            required
                        /></td>
          </tr>;
      })
    };

    handleInputChange = (event) => {
        const target = event.target;
        const value = target.value;
        this.setState({form:{quantity:value}})
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

export default OwnedTable;