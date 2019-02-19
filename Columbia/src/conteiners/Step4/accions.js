import {
    SAVE_STEP4_ACTION,
    MESSAGE_STEP4_ACTION,
    IS_SOCIETY,
    ADD_CUIT
} from './constants';

export const saveDataAction = (payload) => {
    return {
        type: SAVE_STEP4_ACTION,
        payload
    };
}

export const messageAction = (payload) => {
    return {
        type: MESSAGE_STEP4_ACTION,
        payload
    }
}

export const addCuitAction = (payload) => {
    return {
        type: ADD_CUIT,
        payload
    }
}

export const isSocietyAction = (payload) => {
    return {
        type: IS_SOCIETY,
        payload
    }
}