import {
    all,
    takeLatest,
    put
} from 'redux-saga/effects'
import {
    VALIDATE_ACTION
} from './constants'
import {
    setStepRedirectAction,
    setIsLoggedInAction
} from './accions'
import {
    addMailAction
} from '../Step1/accions'

//const airbase = require('../../utils/airtable').base('appzL6pfzYhxOdwsg'); dev
const airbase = require('../../utils/airtable').base('appHJKYgvmLkpv022');

function* validateSaga(action) {
    try {
        let message = 'done'
        let redirect = ''
        let email = ''

        yield airbase.table('Clientes')
            .selectOneByFormula('solicitudId="' + action.payload.solicitudId + '"')
            .then(function (clientRecord) {
                if (clientRecord) {
                    redirect = `/step${clientRecord.fields.Step}`

                    email = clientRecord.fields.Email
                }   
            })

        if (message === 'done') {
            console.log(email);
            
            yield put(setStepRedirectAction(redirect))

            yield put(addMailAction(email))

            yield put(setIsLoggedInAction(true))
        }

    } catch (err) {
        console.log(err);
    }
}

function* watchValidate() {
    yield takeLatest(VALIDATE_ACTION, validateSaga)
}

export default function* loginSaga() {
    yield all([
        watchValidate()
    ]);
}