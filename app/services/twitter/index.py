import tweepy
from config import X_AHORRO_API_KEY, X_AHORRO_API_SECRET, X_AHORRO_API_ACCESS_TOKEN, X_AHORRO_API_ACCESS_TOKEN_SECRET
from .client import get_twitter_conn_v2, get_twitter_conn_v1
def tweet_bcra(message):
  print(f"Tweeting: {message}")
  

def tweet_text_ahorro(message, media_path = None):
  try:
    client = get_twitter_conn_v2(
      api_key=X_AHORRO_API_KEY, 
      api_secret=X_AHORRO_API_SECRET, 
      access_token=X_AHORRO_API_ACCESS_TOKEN, 
      access_token_secret=X_AHORRO_API_ACCESS_TOKEN_SECRET
    )

    if media_path is not None:
      media = media_upload_ahorro(media_path)
      result = client.create_tweet(
        text=message,
        media_ids=[media]
      )
    else: 
      result = client.create_tweet(
        text=message
      )
    
    print(result)
    return True
  
  except Exception as e:
    print(f"Error: {e}")
    return False


def media_upload_ahorro(media_path):
  try:
    client_v1 = get_twitter_conn_v1(
      api_key=X_AHORRO_API_KEY, 
      api_secret=X_AHORRO_API_SECRET, 
      access_token=X_AHORRO_API_ACCESS_TOKEN, 
      access_token_secret=X_AHORRO_API_ACCESS_TOKEN_SECRET
    )
    media = client_v1.media_upload(filename=media_path)
    return media.media_id
  except Exception as e:
    print(e)
    return False