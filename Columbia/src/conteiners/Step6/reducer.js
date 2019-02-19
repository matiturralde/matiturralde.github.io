import {
    MESSAGE_STEP6_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_STEP6_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep6: action.payload
            })
        default:
            return state
    }
}

export default reducer;