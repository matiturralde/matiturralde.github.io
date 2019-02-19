import {
    MESSAGE_STEP5_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_STEP5_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep5: action.payload
            })
        default:
            return state
    }
}

export default reducer;