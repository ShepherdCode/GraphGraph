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

def get_tweets(api=None, hash_tag=None, goal=100):
    # GetSearch(self, term=None, raw_query=None, geocode=None, since_id=None, max_id=None, until=None, since=None, count=15, lang=None, locale=None, result_type='mixed', include_entities=None, return_json=False)
    # Return twitter search results for a given term. You must specify one >of term, geocode, or raw_query.
    bucket_size = 100
    all_tweets = api.GetSearch(count=bucket_size,term=hash_tag,lang="en")
    while len(all_tweets) < goal:
        earliest_id = min(all_tweets, key=lambda x: x.id).id
        earliest_id = earliest_id - 1
        print("{} so far. Get tweets before {}".format(len(all_tweets),earliest_id))
        more_tweets = api.GetSearch(count=bucket_size,term=hash_tag,lang="en",max_id=earliest_id)
        if not more_tweets:
            break
        all_tweets += more_tweets
    return all_tweets

def write_screen(timeline):
    for tweet in timeline:
        print ("Lan={} Len={}\n{}\n".format(tweet.lang,
            len(tweet.full_text),tweet.full_text.replace('\n','')))

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
            t_id = safe_get(one_tweet,'id_str','None')
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
    hash_tag="NeuralNetwork"
    if len(sys.argv) > 1:
        hash_tag = sys.argv[1]
    print(hash_tag)
    timeline = []
    if True:
        timeline = get_tweets(api=api, hash_tag=hash_tag, goal=2000)
    #write_screen(timeline)
    write_json(timeline)
    write_csv(timeline)
