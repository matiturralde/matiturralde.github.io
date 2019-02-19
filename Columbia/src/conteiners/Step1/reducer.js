import {
    ADD_MAIL,
    PIN_ACTION,
    MESSAGE_ACTION,
    SET_DESTINATION_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_MAIL:
            return Object.assign({}, state, {
                ...state,
                email: action.payload
            })
        case PIN_ACTION:
            return Object.assign({}, state, {
                ...state,
                pin: action.payload
            })
        case MESSAGE_ACTION:
            return Object.assign({}, state, {
                ...state,
                message: action.payload
            })
        case SET_DESTINATION_ACTION:
            return Object.assign({}, state, {
                ...state,
                destinos: action.payload
            })
        default:
            return state
    }
}

export default reducer;