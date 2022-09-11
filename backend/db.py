import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyADsDVA25fMn60raxMtpCt5QNWy_2aUazI",
    "authDomain": "siakad-6e707.firebaseapp.com",
    "databaseURL": "https://siakad-6e707-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "siakad-6e707",
    "storageBucket": "siakad-6e707.appspot.com",
    "messagingSenderId": "707193481424",
    "appId": "1:707193481424:web:c2d772390c6cafe77356d5"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN