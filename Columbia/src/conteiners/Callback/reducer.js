import {
    SET_ISLOGGEDIN_ACTION,
    STEP_REDIRECT_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_ISLOGGEDIN_ACTION:
            return Object.assign({}, state, {
                ...state,
                isLoggerdIn: action.payload
            })
        case STEP_REDIRECT_ACTION:
            return Object.assign({}, state, {
                ...state,
                stepRedirect: action.payload
            })
        default:
            return state
    }
}

export default reducer;