#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Source at https://github.com/bear/python-twitter/blob/master/examples/get_all_user_tweets.py
# Docs at https://python-twitter.readthedocs.io/en/latest/

from __future__ import print_function
import json
import sys
import twitter
from TwitterLogin import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
import csv

def get_tweets(api=None, screen_name=None):
    # GetUserTimeline(self, user_id=None, screen_name=None, since_id=None, max_id=None, count=None, include_rts=True, trim_user=False, exclude_replies=False)
    # Fetch the sequence of public Status messages for a single user.

    # Start with last 20 tweets from this user
    timeline = api.GetUserTimeline(
        screen_name=screen_name, count=20,
        include_rts=False, exclude_replies=False
    )
    return timeline

def write_screen(timeline):
    for tweet in timeline:
        print ("Lan={} Len={}\n{}\n\n".format(tweet.lang,len(tweet.full_text),tweet.full_text))
        #print (dir(tweet))
        #print (tweet.__dict__.items())
        #print (vars(tweet))

def write_json(timeline):
    with open('tweets.json', 'w') as f:
        for tweet in timeline:
            f.write(json.dumps(tweet._json,indent=4))
            f.write('\n')

def write_csv(timeline):
    with open('tweets.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['created_at']
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for tweet in timeline:
            tweet_dict=tweet.AsDict()
            print(tweet_dict.keys())
            #writer.writerow(tweet_dict['created_at'])

if __name__ == "__main__":
    api = twitter.Api(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
        tweet_mode='extended'
    )
    screen_name="ShepherdU"
    if len(sys.argv) > 1:
        screen_name = sys.argv[1]
    print(screen_name)
    timeline = []
    if True:
        timeline = get_tweets(api=api, screen_name=screen_name)
    #write_screen(timeline)
    write_json(timeline)
    write_csv(timeline)
