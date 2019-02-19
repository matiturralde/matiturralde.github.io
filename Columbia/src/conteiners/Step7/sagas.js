import { all, takeLatest, put } from 'redux-saga/effects';
import { SAVE_STEP7_ACTION } from './constants';
import { messageAction } from './accions';

//const airbase = require('../../utils/airtable').base('appzL6pfzYhxOdwsg'); dev
const airbase = require('../../utils/airtable').base('appHJKYgvmLkpv022');

function* saveSaga(action) {
    try {
        let message = 'done';

        yield airbase.table('Clientes')
                .selectOneByFormula('Email="' + action.payload.email + '"')
                .then(function (clientRecord) {
                    if (clientRecord) {
                        clientRecord.updateFields({
                            'Factura Electronicamente': action.payload.factura,
                            'AFIP': action.payload.afip,
                            'AFIP RCEL': false,
                            'AFIP RECE': false,
                            'AFIP COMPROBANTES': action.payload.comprobantes,
                            'Step': '8'
                        }, function () {});
                    } else {
                        message = 'No se puede guardar la informacion.'
                    }
                })

        yield put(messageAction(message))

    } catch (err) {
         console.log(err);
    }
}

function* watchSave() {
    yield takeLatest(SAVE_STEP7_ACTION, saveSaga)
}

export default function* step5Saga() {
    yield all([
        watchSave()
    ]);
}