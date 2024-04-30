import tweepy

def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
  """Get twitter conn 1.1"""

  auth = tweepy.OAuth1UserHandler(api_key, api_secret)
  auth.set_access_token(
    access_token,
    access_token_secret,
  )
  return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
  """Get twitter conn 2.0"""

  client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
  )

  return client