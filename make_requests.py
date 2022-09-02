import requests 
import json
import urllib.request
import praw
import random
from discord.ext.commands import MissingPermissions

reddit = praw.Reddit(client_id= 'GknGYLZa2TGHG48IJP9ksQ',
                     client_secret = 'iLibqEqsghdl3fGxgfH_TNOkK54mpw', 
                     user_agent = 'bot-o-meme by Zoneout215')

def get_memes_urls(limit=10):
    request_subreddits = ['virginvschad', 'Chadtopia', 'chadmemes'] 
    meme_list = []
    for request in request_subreddits:
        subreddit = reddit.subreddit(request)
        for submission in subreddit.new(limit=(limit//len(request_subreddits)) + 1):
            meme_list.append(
                ['https://reddit.com' + submission.permalink, submission.title, submission.url])
    random.shuffle(meme_list)
    return meme_list
