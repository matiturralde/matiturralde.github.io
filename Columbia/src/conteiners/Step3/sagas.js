import { all, takeLatest, put } from 'redux-saga/effects';
import { SAVE_PASS_ACTION } from './constants';
import { messageAction } from './accions';
import { setIsLoggedInAction } from '../Login/accions'

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
                            'Password': action.payload.password,
                            'Step': '4'
                        }, function () {});
                    } else {
                        message = 'No se puede guardar la contraseña.'
                    }
                })

        yield put(messageAction(message))

        if (message === 'done') {
            yield put(setIsLoggedInAction(true))
        }

    } catch (err) {
         console.log(err);
    }
}

function* watchSave() {
    yield takeLatest(SAVE_PASS_ACTION, saveSaga)
}

export default function* step3Saga() {
    yield all([
        watchSave()
    ]);
}
