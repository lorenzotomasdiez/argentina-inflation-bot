from config import X_AHORRO_API_KEY, X_AHORRO_API_SECRET, X_AHORRO_API_ACCESS_TOKEN, X_AHORRO_API_ACCESS_TOKEN_SECRET, X_BCRA_API_KEY, X_BCRA_API_SECRET, X_BCRA_API_ACCESS_TOKEN, X_BCRA_API_ACCESS_TOKEN_SECRET
from .client import get_twitter_conn_v2, get_twitter_conn_v1

def ahorro_client():
  client_v1 = get_twitter_conn_v1(
    api_key=X_AHORRO_API_KEY, 
    api_secret=X_AHORRO_API_SECRET, 
    access_token=X_AHORRO_API_ACCESS_TOKEN, 
    access_token_secret=X_AHORRO_API_ACCESS_TOKEN_SECRET
  )
  client_v2 = get_twitter_conn_v2(
    api_key=X_AHORRO_API_KEY, 
    api_secret=X_AHORRO_API_SECRET, 
    access_token=X_AHORRO_API_ACCESS_TOKEN, 
    access_token_secret=X_AHORRO_API_ACCESS_TOKEN_SECRET
  )
  
  return [client_v1, client_v2]

def bcra_client():
  client_v1 = get_twitter_conn_v1(
    api_key=X_BCRA_API_KEY, 
    api_secret=X_BCRA_API_SECRET, 
    access_token=X_BCRA_API_ACCESS_TOKEN, 
    access_token_secret=X_BCRA_API_ACCESS_TOKEN_SECRET
  )
  client_v2 = get_twitter_conn_v2(
    api_key=X_BCRA_API_KEY, 
    api_secret=X_BCRA_API_SECRET, 
    access_token=X_BCRA_API_ACCESS_TOKEN, 
    access_token_secret=X_BCRA_API_ACCESS_TOKEN_SECRET
  )
  
  return [client_v1, client_v2]

def tweet(clients, message, media_path = None):
  clientv1, clientv2 = clients
  if media_path is not None:
    media = media_upload_ahorro(clientv1, media_path)
    result = clientv2.create_tweet(
      text=message,
      media_ids=[media]
    )
  else: 
    result = clientv2.create_tweet(
      text=message
    )
  
  print(result)
  return True


def media_upload_ahorro(client, media_path):
  try:
    media = client.media_upload(filename=media_path)
    return media.media_id
  except Exception as e:
    print(e)
    return False