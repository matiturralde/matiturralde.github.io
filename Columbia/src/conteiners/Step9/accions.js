import {
    SAVE_STEP9_ACTION,
    MESSAGE_STEP9_ACTION
} from './constants';

export const saveDataAction = (payload) => {
    return {
        type: SAVE_STEP9_ACTION,
        payload
    };
}

export const messageAction = (payload) => {
    return {
        type: MESSAGE_STEP9_ACTION,
        payload
    }
}