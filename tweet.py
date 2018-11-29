import nltk
import fs
import re
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import json
import tweepy
import time
import datetime
import random

# Variables that contains the user credentials to access Twitter API
access_token = "127884553-TqitaQ5yWajIsxoJRXB0zMFCvqsLkVsIUtX0j4EA"
access_token_secret = "JQkefONCrcDDFezZvICbX3Sw8FUYpyQs9bqoIVIEzi1Du"
consumer_key = "QnDUp41BaQPi9buXTMmJVQ7Vg"
consumer_secret = "2eYxYHmbrxUIbbZNF0sBtlOARlwmG04DfisJEpJeNgmTGLPH0z"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

sesi_t = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


def createid():
    strid = ""
    randid = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    for j in randid:
        strid += str(j)
    return strid


def tweetstruct(text, pol, loc, t):
    data = {
        'text': text,
        'polarity': pol,
        'location': loc,
        'sentiment': sentiment(pol),
        'time': t,
    }
    return data


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def blobtweet(tweet):
    global teks
    cleaned = clean_tweet(tweet)
    blob = TextBlob(cleaned)

    return blob


def sentiment(pol):
    if pol > 0:
        return 1
    elif pol == 0:
        return 0
    else:
        return -1


def searchtweet(q, c=100):
    api = tweepy.API(auth)
    search_result = api.search(q=q, count=c)
    tweets = [status._json for status in search_result]

    return tweets


def analyzesearch(q, c=100):
    global sesi_t
    sesi_t = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    sesi = q + "_" + sesi_t
    fs.sesi_ref.add({}, sesi)
    data = []
    api = tweepy.API(auth)
    search_result = [status for status in tweepy.Cursor(api.search, q=q).items(c)]
    tweets = [status._json for status in search_result]
    for i in tweets:
        teks = blobtweet(i['text'])
        temp = tweetstruct(str(teks), teks.sentiment.polarity, i['user']['location'], i['created_at'])
        data.append(temp)
        fs.storetweet(sesi, i["id_str"], temp)
    return data, sesi


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        global sesi_t
        all_data = json.loads(data)
        if 'text' in all_data:
            id_str = all_data["id_str"]
            tweet = all_data["text"]
            created_at = all_data["created_at"]
            user_location = all_data["user"]["location"]

            teks = blobtweet(tweet)

            data = tweetstruct(str(teks), teks.sentiment.polarity, user_location, created_at)

            fs.lasttweet(fs.storetweet(sesi_t, id_str, data))
            return True
        else:
            return True

    def on_error(self, status):
        print(status)


def stream(q, t=None):
    global sesi_t
    l = StdOutListener()
    stream = Stream(auth, l)
    sesi_t = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    fs.sesi_ref.add({}, sesi_t)

    try:
        stream.filter(track=[q], is_async=True)
    except:
        print("error")

    if t is not None:
        time.sleep(t)
        stream.disconnect()
