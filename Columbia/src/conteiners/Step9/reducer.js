import {
    MESSAGE_STEP9_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_STEP9_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep9: action.payload
            })
        default:
            return state
    }
}

export default reducer;