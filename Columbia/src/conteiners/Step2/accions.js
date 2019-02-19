import { SET_MESSAGE_ACTION, GET_PIN_ACTION, SENT_PIN_ACTION } from './constants'

export const getPinAction = (payload) => {
    return {
        type: GET_PIN_ACTION,
        payload
    };
}

export const setMessageAction = (payload) => {
    return {
        type: SET_MESSAGE_ACTION,
        payload
    }
}

export const sentPinAction = (payload) => {
    return {
        type: SENT_PIN_ACTION,
        payload
    }
}