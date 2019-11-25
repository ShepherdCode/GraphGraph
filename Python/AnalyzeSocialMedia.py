import sys
import os
import csv
import TwitterHashtag

def read_csv(filename):
    database=[]
    with open(filename, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            database.append(row)
    return database

def download_from_twitter(csv,json):
    print("Initialize Twitter API...")
    api=TwitterHashtag.twitter_initialize()
    GOAL = 10   # change to 2000 when ready
    hash_tag="NeuralNetwork"
    if len(sys.argv) > 1:
        hash_tag = sys.argv[1]
    if len(sys.argv) > 2:
        GOAL = sys.argv[2]
    print("Download {} tweets with hashtag {}.".format(hash_tag,GOAL))
    timeline = []
    if True:
        timeline = TwitterHashtag.get_tweets(api=api, hash_tag=hash_tag, goal=GOAL)
    #TwitterHashtag.write_screen(timeline)
    TwitterHashtag.write_json(timeline,json)
    TwitterHashtag.write_csv(timeline,csv)

if __name__ == "__main__":
    CSV_FILENAME="tweets.csv"
    JSON_FILENAME="tweets.json"
    if not os.path.exists(CSV_FILENAME):
        download_from_twitter(CSV_FILENAME,JSON_FILENAME)
    tweets=read_csv(CSV_FILENAME)
    num_rows_initial = len(tweets)
    print("Number of Rows initially: {}".format(num_rows_initial))
