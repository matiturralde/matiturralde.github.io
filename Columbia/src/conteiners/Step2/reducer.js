import {
    SET_MESSAGE_ACTION
} from './constants';

const initialState = {};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_MESSAGE_ACTION:
            return Object.assign({}, state, {
                ...state,
                messageStep2: action.payload
            })
        default:
            return state
    }
}

export default reducer;