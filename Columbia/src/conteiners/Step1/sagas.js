import { all, takeLatest, put } from 'redux-saga/effects';
import randomize from 'randomatic';
import axios from 'axios';
import { SEND_ACTION, GET_DESTINATION_ACTION } from './constants';
import { addPinAction, getMessage, setDestination } from './accions';

//const airbase = require('../../utils/airtable').base('appzL6pfzYhxOdwsg'); dev
const airbase = require('../../utils/airtable').base('appHJKYgvmLkpv022');

function* sendSaga(action) {
    try {
        const pin = randomize('0', 4);

        yield put(addPinAction(pin))

        let message = 'done';

        yield airbase.table('Clientes')
                .selectOneByFormula('Email="' + action.payload.email + '"')
                .then(function (clientRecord) {
                    if (!clientRecord) {
                        airbase.table('Clientes')
                            .create({
                                'Destination': action.payload.destination,
                                'Email': action.payload.email,
                                'pin': pin,
                                'Step': '1',
                                'Monto': action.payload.amount,
                                'Plazo': action.payload.deadline,
                                'Referral': action.payload.referral,
                                'VendedorContrololador': action.payload.vendedor ? action.payload.vendedor : null
                            })
                            .then(function (clientRecord) {
                                axios.post('https://credility-web-dev.mybluemix.net/sendEmail', {
                                        email: action.payload.email,
                                        pin: pin
                                    })
                                    .then(function (response) {
                                        console.log(response);
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    })
                                
                                axios.post('https://credility-web-dev.mybluemix.net/sendEmailNuevo', {
                                        'destination': action.payload.destination,
                                        'email': action.payload.email,
                                        'amount': action.payload.amount,
                                        'deadline': action.payload.deadline,
                                        'cuit': '',
                                        'tipo': '',
                                        'nombre': '',
                                        'telefono': '',
                                        'seleccion': '' 
                                    })
                                    .then(function (response) {
                                        console.log(response);
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    })

                                return clientRecord;
                            });
                    } else {
                        message = 'Ya existe un usuario con ese email.'
                    }
                })

        yield put(getMessage(message))

    } catch (err) {
         console.log(err);
    }
}

function* destinationSaga () {
    try {
        let destinations = []

        yield airbase.table('Destino').selectAll({
            sort: [
                {
                    field: 'Orden Verdadero',
                    direction: 'asc'
                },
            ],
        }).then(function (destinos) {
            destinos.forEach((element, index) => {
                destinations.push({
                    key: index,
                    text: element.fields.Nombre,
                    value: element.fields.Nombre
                })
            })
        })

        yield put(setDestination(destinations))
        
    } catch (error) {
        console.log(error);
    }
}

function* watchSend() {
    yield takeLatest(SEND_ACTION, sendSaga)
}

function* watchDestination(){
    yield takeLatest(GET_DESTINATION_ACTION, destinationSaga)
}

export default function* step1Saga() {
    yield all([
        watchSend(),
        watchDestination()
    ]);
}
