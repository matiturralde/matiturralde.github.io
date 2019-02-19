import { all } from 'redux-saga/effects';
import loginSaga from './conteiners/Login/sagas'
import step1Saga from './conteiners/Step1/sagas'
import step2Saga from './conteiners/Step2/sagas'
import step3Saga from './conteiners/Step3/sagas'
import step4Saga from './conteiners/Step4/sagas'
import step5Saga from './conteiners/Step5/sagas'
import step6Saga from './conteiners/Step6/sagas'
import step7Saga from './conteiners/Step7/sagas'
import step9Saga from './conteiners/Step9/sagas'
import step10Saga from './conteiners/Step10/sagas'
import callback from './conteiners/Callback/sagas'

export default function* rootSaga() {
    yield all([
        loginSaga(),
        step1Saga(),
        step2Saga(),
        step3Saga(),
        step4Saga(),
        step5Saga(),
        step6Saga(),
        step7Saga(),
        step9Saga(),
        step10Saga(),
        callback(),
    ]);
}