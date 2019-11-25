import sys
import os
import csv
import TwitterHashtag
import nltk
from nltk.tokenize import word_tokenize

TOKEN_SEPARATOR=' '

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
    GOAL = 10
    hash_tag="NeuralNetwork"
    if len(sys.argv) > 1:
        hash_tag = sys.argv[1]
    if len(sys.argv) > 2:
        GOAL = int(sys.argv[2])
    print("Download {} tweets with hashtag {}.".format(GOAL,hash_tag))
    timeline = []
    if True:
        timeline = TwitterHashtag.get_tweets(api=api, hash_tag=hash_tag, goal=GOAL)
    #TwitterHashtag.write_screen(timeline)
    TwitterHashtag.write_json(timeline,json)
    TwitterHashtag.write_csv(timeline,csv)

def clean_text(orig_text,verbose=False):
    import re, string
    if verbose: print("ORIGINAL")
    if verbose: print(orig_text)
    if verbose: print("REMOVE URLS")
    clean_text = re.sub(r"http\S+", "", orig_text)
    if verbose: print(clean_text)
    if verbose: print("REMOVE AT SIGNS")
    clean_text = re.sub(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9-_]+)", "", clean_text)
    if verbose: print(clean_text)
    if verbose: print("REMOVE PUNCTUATION")
    clean_text = clean_text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
    if verbose: print(clean_text)
    if verbose: print("REPLACE LINEBREAKS")
    clean_text = re.sub(r"(\r?\n|\r)", " ", clean_text)
    if verbose: print(clean_text)
    if verbose: print("STRIP NON-ASCII")
    clean_text = re.sub(r"[^\x00-\x7F]+","", clean_text)
    if verbose: print(clean_text)
    if verbose: print("STRIP EXTRA SPACES")
    clean_text = re.sub(' +', ' ', clean_text)
    if verbose: print(clean_text)
    if verbose: print()
    return clean_text;

def analyze_tokens(tweets,filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id_str','original_text','cleaned_text','filtered_tokens','stemmed_tokens','lemmatized_tokens']
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for one_tweet in tweets:
            tweet_id = one_tweet.get('id_str')
            full_text = one_tweet.get('full_text')
            strip_text=clean_text(full_text)
            filt_tokens_list=word_tokenize(strip_text)
            filt_tokens_str=TOKEN_SEPARATOR.join(filt_tokens_list)
            new_dict={'id_str':tweet_id,
                    'original_text':full_text,
                    'cleaned_text':strip_text,
                    'filtered_tokens':filt_tokens_str}
            writer.writerow(new_dict)

if __name__ == "__main__":
    CSV_FILENAME="tweets.csv"
    JSON_FILENAME="tweets.json"
    TOKENS_FILENAME="cleantokens.csv"
    if not os.path.exists(CSV_FILENAME):
        download_from_twitter(CSV_FILENAME,JSON_FILENAME)
    tweets=read_csv(CSV_FILENAME)
    print("Number of Tweets: {}".format(len(tweets)))
    analyze_tokens(tweets,TOKENS_FILENAME)
