import { all, takeLatest, put } from 'redux-saga/effects';
import { SAVE_STEP4_ACTION } from './constants';
import { messageAction, addCuitAction, isSocietyAction } from './accions';

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
                            'CUIT': action.payload.cuit,
                            'Razón Social': action.payload.rsocial,
                            'Tipo': action.payload.valueCheckbox,
                            'Web': action.payload.website,
                            'Facebook': action.payload.fanPage,
                            'Linkedin': action.payload.linkedIn,
                            'Twitter': action.payload.twitter,
                            'Step': '5'
                        }, function () {})
                    } else {
                        message = 'No se puede guardar la informacion.'
                    }
                })

        yield put(messageAction(message))
        
        if (message === 'done') {
            
            yield put(addCuitAction(action.payload.cuit))

            if (action.payload.valueCheckbox === 'S.A. o S.R.L.') {
                yield put(isSocietyAction(true))
            } else {
                yield put(isSocietyAction(false))
            }
            
        }

    } catch (err) {
         console.log(err);
    }
}

function* watchSave() {
    yield takeLatest(SAVE_STEP4_ACTION, saveSaga)
}

export default function* step4Saga() {
    yield all([
        watchSave()
    ]);
}
