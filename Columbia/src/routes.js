import React from 'react';
import { Route, Switch, Redirect } from "react-router"
import Login from './conteiners/Login'
import Step1 from './conteiners/Step1'
import Step2 from './conteiners/Step2'
import Step3 from './conteiners/Step3'
import Step4 from './conteiners/Step4'
import Step5 from './conteiners/Step5'
import Step6 from './conteiners/Step6'
import Step7 from './conteiners/Step7'
import Step8 from './conteiners/Step8'
import Step9 from './conteiners/Step9'
import Step10 from './conteiners/Step10'
import Thank from './conteiners/Thank'
import Greeting from './conteiners/Greeting'
import Callback from './conteiners/Callback'

import withTracker from './utils/analytics'

export default (props) => {
    const {
        isLoggerdIn
    } = props

    const PrivateRoute = ({ component: Component, ...rest }) => (
        <Route
            {...rest}
            render={props =>
                isLoggerdIn ? (
                    <Component {...props} />
                ) : (
                    <Redirect
                        to={{
                            pathname: '/'
                        }}
                    />
                )
            }
        />
    )

    return (
        <Switch>
            <Route exact path="/" component={Step1} />
            <Route exact path="/mariva/:monto?/:plazo?" component={Step1} />
            <Route exact path="/login" component={withTracker(Login)} />
            <Route exact path="/step2" component={withTracker(Step2)} />
            <Route exact path="/step3" component={withTracker(Step3)} />
            <Route exact path="/step4" component={withTracker(Step4)} />
            <Route exact path="/step5" component={withTracker(Step5)} />
            <Route exact path="/step6" component={withTracker(Step6)} />
            <Route exact path="/step7" component={withTracker(Step7)} />
            <Route exact path="/step8" component={withTracker(Step8)} />
            <Route exact path="/step9" component={withTracker(Step9)} />
            <Route exact path="/step10" component={withTracker(Step10)} />
            <Route exact path="/greeting" component={withTracker(Greeting)} />
            <Route exact path="/thank" component={withTracker(Thank)} />
            <Route exact path="/callback/:solicitudId" component={withTracker(Callback)} />
        </Switch>
    )
}