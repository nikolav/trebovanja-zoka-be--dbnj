
import tweepy
import contextlib


@contextlib.contextmanager
def twitter_client(bearer_token: str):
  error  = None
  client = None
  res    = ()

  try:
    client = tweepy.Client(bearer_token = bearer_token)
    res = (error, client,)
    yield res

  finally:
    del client



