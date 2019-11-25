import sys
import csv
import TwitterHashtag

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
    TwitterHashtag.write_json(timeline)
    TwitterHashtag.write_csv(timeline)
