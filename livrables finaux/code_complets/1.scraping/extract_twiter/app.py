import asyncio
from twikit import Client, TooManyRequests
from datetime import datetime
import csv
import json
from configparser import ConfigParser
from random import randint
import os

MINIMUM_TWEETS = 1000
QUERY = '(Université UVBF OR UVBF OR #UVBF OR "Université Virtuelle du Burkina Faso" OR "UV-BF" OR "UV BF" OR "UV_BF") lang:fr'

async def get_tweets(tweets, client):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Latest')  # Changer à Latest
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets

async def main():
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    client = Client(language='en-US')

    cookies_file = 'cookies.json'
    if not os.path.exists(cookies_file):
        print(f"{datetime.now()} - Aucun cookie trouvé. Connexion manuelle nécessaire.")
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies(cookies_file)
        print(f"{datetime.now()} - Connexion réussie. Cookies sauvegardés.")
    else:
        client.load_cookies(cookies_file)
        print(f"{datetime.now()} - Cookies chargés depuis {cookies_file}.")

    tweet_count = 0
    tweets = None
    tweets_data = []

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets, client)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = {
                'text': tweet.text,
                'author': tweet.user.name if tweet.user else 'Unknown',
                'date': tweet.created_at
            }
            tweets_data.append(tweet_data)
            print(f'{datetime.now()} - Got {tweet_count} tweets')

            with open('tweets_uvbf.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([tweet_data['text'], tweet_data['author'], tweet_data['date']])

    with open('tweets_uvbf.json', 'w', encoding='utf-8') as json_file:
        json.dump(tweets_data, json_file, ensure_ascii=False, indent=4)

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')

asyncio.run(main())

