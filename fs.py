import google.cloud.exceptions
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# Firestore
cred = credentials.Certificate('kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
tweet_ref = db.collection('tweet')
sesi_ref = db.collection('session')


def storetweet(sesi, id, input):
    try:
        ref = sesi_ref.document(sesi).collection('tweet').document(id)
        ref.set(input)
        return ref
    except google.cloud.exceptions.exceptions:
        print(google.cloud.exceptions.exceptions)


def lasttweet(ref):
    try:
        i = tweet_ref.document("0_lasttweet").get().get("total")

        tweet_ref.document("0_lasttweet").set({'ref': ref})
        tweet_ref.document("0_lasttweet").update({"total": i + 1})
    except google.cloud.exceptions.exceptions:
        print(google.cloud.exceptions.exceptions)
