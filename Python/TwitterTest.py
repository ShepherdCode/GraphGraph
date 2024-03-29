#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Source at https://github.com/bear/python-twitter/blob/master/examples/get_all_user_tweets.py
# Docs at https://python-twitter.readthedocs.io/en/latest/

"""
Downloads all tweets from a given user.
Uses twitter.Api.GetUserTimeline to retreive the last 3,200 tweets from a user.
Twitter doesn't allow retreiving more tweets than this through the API, so we get
as many as possible.
t.py should contain the imported variables.
"""

from __future__ import print_function
import json
import sys
import twitter
from TwitterLogin import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


def get_tweets(api=None, screen_name=None):
    # Start with last 20 tweets from this user
    timeline = api.GetUserTimeline(
        screen_name=screen_name, count=20,
        include_rts=False, exclude_replies=False
    )
    # Find the oldest tweet based on field "id"
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)
    # In a loop, get next 20 tweets with older "id" until Twitter refuses.
    # Either user has no more tweets or we hit the API limit of 3200.
    total_loops = 3
    this_loop = 1
    while this_loop <= total_loops:
        this_loop += 1
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=20,
            include_rts=False, exclude_replies=False
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


if __name__ == "__main__":
    api = twitter.Api(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
        tweet_mode='extended'
    )
    screen_name="sergekoren"
    if len(sys.argv) > 1:
        screen_name = sys.argv[1]
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    with open('test_output.json', 'w+') as f:
        for tweet in timeline:
            print ("{} len {} -- {}\n\n".format(tweet.lang,len(tweet.full_text),tweet.full_text))
            f.write(json.dumps(tweet._json))
            f.write('\n')
