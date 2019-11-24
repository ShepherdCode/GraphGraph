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

def safe_get(dictionary,field,default):
    if not isinstance(dictionary,dict) or field is None or not field in dictionary:
        return default
    return dictionary.get(field)

def write_csv(timeline):
    with open('tweets.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id_str','created_at','screen_name',
            'retweet_count','favorite_count','full_text']
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for tweet in timeline:
            one_tweet=tweet.AsDict()
            #print(type(one_tweet))
            #print(dir(one_tweet.keys()))
            #print(one_tweet.keys())
            t_id = one_tweet['id_str']
            t_created = safe_get(one_tweet,'created_at','None')
            t_user = safe_get(one_tweet,'user','None')
            t_name = safe_get(t_user,'screen_name','None')
            t_retweet = safe_get(one_tweet,'retweet_count',0)
            t_favorite = safe_get(one_tweet,'favorite_count',0)
            t_text = safe_get(one_tweet,'full_text','None').replace('\n',' ')
            sub_dict={'id_str':t_id,'created_at':t_created,'screen_name':t_name,
                'retweet_count':t_retweet,'favorite_count':t_favorite,
                'full_text':t_text}
            writer.writerow(sub_dict)

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
    write_screen(timeline)
    write_json(timeline)
    write_csv(timeline)
