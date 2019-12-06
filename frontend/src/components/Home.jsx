import React, {Component} from "react";


class Home extends Component {
    constructor(props) {
        super(props);

    }
    render() {
        const image={
            width:'100%',
        };

        return (<div>
            <img src="https://i.kym-cdn.com/photos/images/newsfeed/001/499/826/2f0.png" style={image}/>
            <div className="container">
                <h1 className="display-4">Invest Easy Today!</h1>
                <p>The best way to invest in stonks with no commissions </p>
            </div>
        </div>);
    }
}

export default Home;