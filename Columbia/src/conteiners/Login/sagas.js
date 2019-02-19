import { all, takeLatest, put } from 'redux-saga/effects'
import { VALIDATE_ACTION } from './constants'
import { messageAction, setStepRedirectAction, setIsLoggedInAction } from './accions'
import { addMailAction } from '../Step1/accions'
import { isSocietyAction, addCuitAction } from '../Step4/accions'
import sha1 from 'crypto-js/sha256'
import Base64 from 'crypto-js/enc-base64'

//const airbase = require('../../utils/airtable').base('appzL6pfzYhxOdwsg'); dev
const airbase = require('../../utils/airtable').base('appHJKYgvmLkpv022');

function* validateSaga(action) {
    try {
        let message = 'done'
        let redirect = ''
        let cuit = ''
        let isSociety = false

        yield airbase.table('Clientes')
                .selectOneByFormula('Email="' + action.payload.email + '"')
                .then(function (clientRecord) {
                    if (clientRecord) {
                        const hashDigest = sha1(action.payload.password);

                        const hmacDigest = Base64.stringify(hashDigest);

                        if (clientRecord.fields.Password !== hmacDigest) {
                            message = 'Contraseña incorrecta.'
                        } else {
                            redirect = `step${clientRecord.fields.Step}`

                            cuit = clientRecord.fields.CUIT

                            if (clientRecord.fields.Tipo === 'S.A. o S.R.L.') {
                                isSociety = true     
                            }

                        }
                    } else {
                        message = 'No se encontro Cliente.'
                    }
                })

        yield put(messageAction(message))

        if (message === 'done') {
            yield put(setStepRedirectAction(redirect))

            yield put(addMailAction(action.payload.email))

            yield put(setIsLoggedInAction(true))

            yield put(isSocietyAction(isSociety))

            yield put(addCuitAction(cuit))
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
