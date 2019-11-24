import os
import twitter

CONSUMER_KEY=os.environ["twitter_consumer_key"]
CONSUMER_SECRET=os.environ["twitter_consumer_secret"]
ACCESS_TOKEN_KEY=os.environ["twitter_access_token"]
ACCESS_TOKEN_SECRET=os.environ["twitter_access_secret"]

if __name__ == '__main__':
    api = twitter.Api(consumer_key=[CONSUMER_KEY],
                  consumer_secret=[CONSUMER_SECRET],
                  access_token_key=[ACCESS_TOKEN_KEY],
                  access_token_secret=[ACCESS_TOKEN_SECRET])
    print("Success. api=",end='')
    print(api)
