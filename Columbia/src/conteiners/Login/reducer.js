import {
    MESSAGE_LOGIN_ACTION,
    SET_ISLOGGEDIN_ACTION,
    STEP_REDIRECT_ACTION,
    CLEAN_MESSAGE_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_LOGIN_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageLogin: action.payload
            })
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
        case CLEAN_MESSAGE_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageLogin: ''
            })
        default:
            return state
    }
}

export default reducer;
