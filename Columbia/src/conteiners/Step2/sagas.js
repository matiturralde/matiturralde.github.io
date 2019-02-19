import { all, takeLatest, put } from 'redux-saga/effects';
import axios from 'axios';
import { GET_PIN_ACTION, SENT_PIN_ACTION } from './constants';
import { setMessageAction } from './accions';

//const airbase = require('../../utils/airtable').base('appzL6pfzYhxOdwsg'); dev
const airbase = require('../../utils/airtable').base('appHJKYgvmLkpv022');

function* getSaga(action) {
    try {
        let message = 'done';

        yield airbase.table('Clientes')
                .selectOneByFormula('Email="' + action.payload.email + '"')
                .then(function (clientRecord) {
                    if (clientRecord) {
                        if (clientRecord.fields.pin !== action.payload.pin) {
                            message = 'El Pin ingresado es incorrecto.'
                        }
                    } else {
                        message = 'No se encontro Cliente.'
                    }
                })

        yield put(setMessageAction(message))

    } catch (err) {
         console.log(err);
    }
}

function* sentSaga(action) {

    yield airbase.table('Clientes')
        .selectOneByFormula('Email="' + action.payload.email + '"')
        .then(function (clientRecord) {
            if (clientRecord) {
                axios.post('https://credility-web-dev.mybluemix.net/sendEmail', {
                        email: action.payload.email,
                        pin: clientRecord.fields.pin
                    })
                    .then(function (response) {
                        console.log(response);
                    })
                    .catch(function (error) {
                        console.log(error);
                    })
            }
        })
}

function* watchGet() {
    yield takeLatest(GET_PIN_ACTION, getSaga)
}

function* watchSent() {
    yield takeLatest(SENT_PIN_ACTION, sentSaga)
}

export default function* step2Saga() {
    yield all([
        watchGet(),
        watchSent()
    ]);
}
