import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import createHistory from "history/createBrowserHistory";
import { ConnectedRouter } from "react-router-redux";
import App from './App';
import registerServiceWorker from './registerServiceWorker';

import configureStore from './configureStore';
import './index.css';

const history = createHistory();

const store = configureStore(history);

ReactDOM.render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <App />
        </ConnectedRouter>
    </Provider>, document.getElementById('root'));
registerServiceWorker();
