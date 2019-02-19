import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import loginReducer from './conteiners/Login/reducer'
import step1Reducer from './conteiners/Step1/reducer'
import step2Reducer from './conteiners/Step2/reducer'
import step3Reducer from './conteiners/Step3/reducer'
import step4Reducer from './conteiners/Step4/reducer'
import step5Reducer from './conteiners/Step5/reducer'
import step6Reducer from './conteiners/Step6/reducer'
import step7Reducer from './conteiners/Step7/reducer'
import step9Reducer from './conteiners/Step9/reducer'
import step10Reducer from './conteiners/Step10/reducer'
import callbackReducer from './conteiners/Callback/reducer'

const rootReducer = combineReducers({
    loginReducer,
    step1Reducer,
    step2Reducer,
    step3Reducer,
    step4Reducer,
    step5Reducer,
    step6Reducer,
    step7Reducer,
    step9Reducer,
    step10Reducer,
    callbackReducer,
    routing: routerReducer
});

export default rootReducer;
