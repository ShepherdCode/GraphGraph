import sys
import os
import csv
import TwitterHashtag
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

CSV_FILENAME="tweets.csv"
JSON_FILENAME="tweets.json"
TOKENS_FILENAME="cleantokens.csv"
FREQ_FILENAME="frequency.csv"
TOKEN_SEPARATOR=' '
STOP_LANGUAGE='english'
MIN_WORD_SIZE=3
stops = set(stopwords.words(STOP_LANGUAGE)) # lntk works like 'and'
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def read_csv(filename):
    database=[]
    with open(filename, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            database.append(row)
    return database

def download_from_twitter():
    (csv,json)=(CSV_FILENAME,JSON_FILENAME)
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

def get_tokens(textin):
    tokens_list=word_tokenize(textin)  # nltk library call
    large_tokens=[w for w in tokens_list if len(w)>=MIN_WORD_SIZE]
    # Learned from https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    nonstop_tokens_list=[w for w in large_tokens if not w in stops]
    return nonstop_tokens_list

def get_stems(tokens):
    stem_tokens=[stemmer.stem(w) for w in tokens]
    return stem_tokens

def get_lemmas(tokens):
    # Learned from https://www.geeksforgeeks.org/python-lemmatization-with-nltk/
    lemma_tokens=[lemmatizer.lemmatize(w) for w in tokens]
    return lemma_tokens

def analyze_word_frequency (word_string):
    word_list = sorted(word_string.split())
    prev_word=""
    frequencies={}
    for one_word in word_list:
        if one_word == prev_word:
            frequencies[one_word]=frequencies[one_word]+1
        else:
            frequencies[one_word]=1
        prev_word = one_word
    sortfreq = sorted(frequencies.items(), key=lambda kv: kv[1])
    with open(FREQ_FILENAME, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['lemma','frequency']
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for one_pair in reversed(sortfreq):
            new_dict={'lemma':one_pair[0],'frequency':one_pair[1]}
            writer.writerow(new_dict)

def analyze_tokens(tweets):
    lemmas = ""
    print("Analyze tokens in {} tweets...".format(len(tweets)))
    with open(TOKENS_FILENAME, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id_str','original_text','cleaned_text','filtered_tokens','stemmed_tokens','lemmatized_tokens']
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for one_tweet in tweets:
            tweet_id = one_tweet.get('id_str')
            full_text = one_tweet.get('full_text')
            strip_text=clean_text(full_text)
            filt_tokens=get_tokens(strip_text)
            stem_tokens=get_stems(filt_tokens)
            stem_token_str=TOKEN_SEPARATOR.join(stem_tokens)
            lemma_tokens=get_lemmas(filt_tokens)
            lemma_token_str=TOKEN_SEPARATOR.join(lemma_tokens)
            new_dict={'id_str':tweet_id,
                    'original_text':full_text,
                    'cleaned_text':strip_text,
                    'filtered_tokens':stem_token_str,
                    'stemmed_tokens':stem_token_str,
                    'lemmatized_tokens':lemma_token_str}
            writer.writerow(new_dict)
            lemmas=TOKEN_SEPARATOR.join([lemmas,lemma_token_str])
    print("Analyze lemmas in {} tokens...".format(len(lemmas.split())))
    analyze_word_frequency(lemmas)

if __name__ == "__main__":
    if os.path.exists(CSV_FILENAME):
        print("Reuse existing file of tweets: {}".format(CSV_FILENAME))
    else:
        print("Download from Twitter to {}".format(CSV_FILENAME))
        download_from_twitter()
    tweets=read_csv(CSV_FILENAME)
    analyze_tokens(tweets)
    print("Our analysis is in these files: {}, {}, {}".format(CSV_FILENAME,TOKENS_FILENAME,FREQ_FILENAME))
