import { all, takeLatest, put } from 'redux-saga/effects'
import { SAVE_STEP9_ACTION } from './constants'
import { messageAction } from './accions'
import firebase from 'firebase'

const config = {
    apiKey: "AIzaSyBhYDVooIYZPL_6XTJhLhe84bdwpbaVPcA",
    authDomain: "credility-8f1b8.firebaseapp.com",
    databaseURL: "https://credility-8f1b8.firebaseio.com",
    projectId: "credility-8f1b8",
    storageBucket: "credility-8f1b8.appspot.com",
    messagingSenderId: "822672319174"
};
firebase.initializeApp(config);

//const airbase = require('../../utils/airtable').base('appzL6pfzYhxOdwsg'); dev
const airbase = require('../../utils/airtable').base('appHJKYgvmLkpv022')

function* saveSaga(action) {
    try {
        let message = 'done'
        let urlFile1 = ''
        let urlFile2

        if (!action.payload.checked) {
            const storageRef = firebase.storage().ref(`${action.payload.email}/${action.payload.fileEstatuto[0].name}`)
            const uploadTask = storageRef.put(action.payload.fileEstatuto[0])

            uploadTask.on('state_changed', function (snapshot) {
            }, function (error) {
            }, function () {
                uploadTask.snapshot.ref.getDownloadURL().then(function (downloadURL) {
                    urlFile1 = downloadURL
                });

                const storageRef2 = firebase.storage().ref(`${action.payload.email}/${action.payload.fileBalanceInput[0].name}`)
                const uploadTask2 = storageRef2.put(action.payload.fileBalanceInput[0])

                uploadTask2.on('state_changed', function (snapshot) {}, function (error) {}, function () {
                    uploadTask2.snapshot.ref.getDownloadURL().then(function (downloadURL1) {
                        urlFile2 = downloadURL1
                        airbase.table('Clientes')
                            .selectOneByFormula('Email="' + action.payload.email + '"')
                            .then(function (clientRecord) {
                                if (clientRecord) {
                                    airbase.table('Uploads')
                                        .create({
                                            'Attachments': [{
                                                    url: urlFile1
                                                },
                                                {
                                                    url: urlFile2
                                                }
                                            ],
                                            'Clientes': [clientRecord.id]
                                        })
                                    if (action.payload.isSociety) {
                                        clientRecord.updateFields({
                                            'Step': '10'
                                        }, function () {});
                                    } else {
                                        clientRecord.updateFields({
                                            'Step': '99'
                                        }, function () {});
                                    }

                                } else {
                                    message = 'Ya existe un usuario con ese email.'
                                }
                            })
                    });
                });
            });

            yield put(messageAction(message))

        } else {
            yield airbase.table('Clientes')
                .selectOneByFormula('Email="' + action.payload.email + '"')
                .then(function (clientRecord) {
                    if (clientRecord) {
                        if (action.payload.isSociety) {
                            clientRecord.updateFields({
                                'Step': '10'
                            }, function () {});
                        } else {
                            clientRecord.updateFields({
                                'Step': '99'
                            }, function () {});
                        }

                    } else {
                        message = 'Ya existe un usuario con ese email.'
                    }
                })

            yield put(messageAction(message))
        }

    } catch (err) {
         console.log(err);
    }
}

function* watchSave() {
    yield takeLatest(SAVE_STEP9_ACTION, saveSaga)
}

export default function* step5Saga() {
    yield all([
        watchSave()
    ]);
}