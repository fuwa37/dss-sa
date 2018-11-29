import google.cloud.exceptions
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Firestore
cred = credentials.Certificate('kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
tweet_ref = db.collection('tweet')
last_ref = db.collection("lasttweet")


def storetweet(id, input):
    try:
        ref = tweet_ref.document(id)
        ref.set(input)
        return ref
    except google.cloud.exceptions.exceptions:
        print(google.cloud.exceptions.exceptions)


def lasttweet(ref):
    try:
        i = last_ref.document("tweet").get().get("total")

        last_ref.document('last').set({'ref': ref})
        last_ref.document("tweet").update({"total": i + 1})
    except google.cloud.exceptions.exceptions:
        print(google.cloud.exceptions.exceptions)
