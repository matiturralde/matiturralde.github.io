import {
    SAVE_STEP10_ACTION,
    MESSAGE_STEP10_ACTION
} from './constants';

export const saveDataAction = (payload) => {
    return {
        type: SAVE_STEP10_ACTION,
        payload
    };
}

export const messageAction = (payload) => {
    return {
        type: MESSAGE_STEP10_ACTION,
        payload
    }
}