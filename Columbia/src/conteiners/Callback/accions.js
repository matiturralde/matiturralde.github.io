import {
    SET_ISLOGGEDIN_ACTION,
    STEP_REDIRECT_ACTION,
    VALIDATE_ACTION,
} from './constants'

export const validationAction = (payload) => ({
    type: VALIDATE_ACTION,
    payload: payload
})

export const setIsLoggedInAction = (payload) => ({
    type: SET_ISLOGGEDIN_ACTION,
    payload: payload
})

export const setStepRedirectAction = (payload) => ({
    type: STEP_REDIRECT_ACTION,
    payload: payload
})