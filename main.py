import tweet

r = tweet.searchtweet('hello')

for i in r:
    print(i.text)
