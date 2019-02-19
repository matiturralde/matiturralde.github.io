import { all, takeLatest, put } from 'redux-saga/effects'
import axios from 'axios'
import { SEND_EMAIL_MAIL } from './constants'
import { messageAction } from './accions'

//const airbase = require('../../utils/airtable').base('appzL6pfzYhxOdwsg'); dev
const airbase = require('../../utils/airtable').base('appHJKYgvmLkpv022');

function* sendSaga(action) {
    try {
        let message = ''

        yield airbase.table('Clientes')
                .selectOneByFormula('Email="' + action.payload.email + '"')
                .then(function (clientRecord) {
                    if (clientRecord) {
                        axios.post('https://credility-web-dev.mybluemix.net/sendEmailNuevo', {
                                'destination': clientRecord.fields.Destination,
                                'email': clientRecord.fields.Email,
                                'amount': clientRecord.fields.Monto,
                                'deadline': clientRecord.fields.Plazo,
                                'cuit': clientRecord.fields.CUIT,
                                'tipo': clientRecord.fields.Tipo,
                                'nombre': clientRecord.fields.Nombre,
                                'telefono': clientRecord.fields.Telefono,
                                'seleccion': action.payload.seleccion
                            })
                            .then(function (response) {
                                console.log(response);
                            })
                            .catch(function (error) {
                                console.log(error);
                            })

                            clientRecord.updateFields({
                                'Step': '7'
                            }, function () {});

                            message = action.payload.seleccion
                    } else {
                        message = 'No se pudo enviar email.'
                    }
                })

        yield put(messageAction(message))

    } catch (err) {
         console.log(err);
    }
}

function* watchSend() {
    yield takeLatest(SEND_EMAIL_MAIL, sendSaga)
}

export default function* step6Saga() {
    yield all([
        watchSend()
    ]);
}
