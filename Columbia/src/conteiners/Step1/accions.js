import {
    SEND_ACTION,
    ADD_MAIL,
    PIN_ACTION,
    MESSAGE_ACTION,
    GET_DESTINATION_ACTION,
    SET_DESTINATION_ACTION
} from './constants';

export const sendAction = (payload) => {
    return {
        type: SEND_ACTION,
        payload
    };
}

export const addMailAction = (payload) => {
    return {
        type: ADD_MAIL,
        payload
    }
}

export const addPinAction = (payload) => {
    return {
        type: PIN_ACTION,
        payload
    }
}

export const getMessage = (payload) => {
    return {
        type: MESSAGE_ACTION,
        payload
    }
}

export const getDestination = () => {
    return {
        type: GET_DESTINATION_ACTION
    }
}

export const setDestination = (payload) => {
    return{
        type: SET_DESTINATION_ACTION,
        payload
    }
}
