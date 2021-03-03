from application import *
from apikeys import *
import tweepy

corona = "CoronaVirus"
animal = "Animal Crossing"
donald = "Donald Trump"

interested_keyword = "Covid"

# However many tweets processed before plot/average
average_time_step = 1
listener = Listener(interested_keyword, average_time_step)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

stream = Streamer(auth, listener, interested_keyword)

def stream_multiple(interested_keywords):
    pass

if __name__=='__main__':
    stream.start_stream()
