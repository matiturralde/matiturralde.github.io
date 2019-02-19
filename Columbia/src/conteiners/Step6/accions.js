import {
    SEND_EMAIL_MAIL,
    MESSAGE_STEP6_ACTION
    
} from './constants'

export const sendEmailAction = (payload) => {
    return {
        type: SEND_EMAIL_MAIL,
        payload
    };
}

export const messageAction = (payload) => {
    return {
        type: MESSAGE_STEP6_ACTION,
        payload
    }
}