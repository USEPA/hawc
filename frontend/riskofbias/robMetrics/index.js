import React from "react";
import ReactDOM from "react-dom";
import {Provider} from "mobx-react";

import RobMetricsStore from "./store";
import Root from "./Root";

export default function(el, config) {
    const store = new RobMetricsStore(config);
    ReactDOM.render(
        <Provider store={store}>
            <Root />
        </Provider>,
        el
    );
}
