import {
    SAVE_STEP7_ACTION,
    MESSAGE_STEP7_ACTION
} from './constants';

export const saveDataAction = (payload) => {
    return {
        type: SAVE_STEP7_ACTION,
        payload
    };
}

export const messageAction = (payload) => {
    return {
        type: MESSAGE_STEP7_ACTION,
        payload
    }
}