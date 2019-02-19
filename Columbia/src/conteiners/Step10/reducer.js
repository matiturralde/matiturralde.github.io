import {
    MESSAGE_STEP10_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_STEP10_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep10: action.payload
            })
        default:
            return state
    }
}

export default reducer;