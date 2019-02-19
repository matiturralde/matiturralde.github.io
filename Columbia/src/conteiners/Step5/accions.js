import {
    SAVE_STEP5_ACTION,
    MESSAGE_STEP5_ACTION
} from './constants';

export const saveDataAction = (payload) => {
    return {
        type: SAVE_STEP5_ACTION,
        payload
    };
}

export const messageAction = (payload) => {
    return {
        type: MESSAGE_STEP5_ACTION,
        payload
    }
}