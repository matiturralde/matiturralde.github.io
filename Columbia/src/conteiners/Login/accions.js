import {
    VALIDATE_ACTION,
    MESSAGE_LOGIN_ACTION,
    SET_ISLOGGEDIN_ACTION,
    STEP_REDIRECT_ACTION,
    CLEAN_MESSAGE_ACTION
} from './constants'

export const validationAction = (payload) => ({
  type: VALIDATE_ACTION,
  payload: payload
})

export const messageAction = (payload) => ({
  type: MESSAGE_LOGIN_ACTION,
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

export const cleanMessageAction = () => ({
  type: CLEAN_MESSAGE_ACTION,
})



