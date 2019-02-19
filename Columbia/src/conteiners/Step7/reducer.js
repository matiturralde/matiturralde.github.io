import {
    MESSAGE_STEP7_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_STEP7_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep7: action.payload
            })
        default:
            return state
    }
}

export default reducer;