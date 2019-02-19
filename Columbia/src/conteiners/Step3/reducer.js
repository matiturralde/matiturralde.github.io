import {
    MESSAGE_STEP3_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case MESSAGE_STEP3_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep3: action.payload
            })
        default:
            return state
    }
}

export default reducer;