import {
    MESSAGE_STEP4_ACTION,
    IS_SOCIETY,
    ADD_CUIT
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_STEP4_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep4: action.payload
            })
        case IS_SOCIETY:
            return Object.assign({}, state, {
                ...state,
                isSociety: action.payload
            })
        case ADD_CUIT:
            return Object.assign({}, state, {
                ...state,
                cuit: action.payload
            })
        default:
            return state
    }
}

export default reducer;