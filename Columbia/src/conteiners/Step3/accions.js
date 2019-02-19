import {
    SAVE_PASS_ACTION,
    MESSAGE_STEP3_ACTION
} from './constants';

export const savePassAction = (payload) => {
    return {
        type: SAVE_PASS_ACTION,
        payload
    };
}

export const messageAction = (payload) => {
    return {
        type: MESSAGE_STEP3_ACTION,
        payload
    }
}