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



###FONCTIONNE BIEN
# import asyncio
# from twikit import Client, TooManyRequests
# from datetime import datetime
# import csv
# import json
# from configparser import ConfigParser
# from random import randint
# import os

# MINIMUM_TWEETS = 20
# QUERY = '(Université UVBF OR UVBF OR #UVBF) lang:fr'  # Requête de recherche

# # La fonction get_tweets devient asynchrone et prend client en paramètre
# async def get_tweets(tweets, client):
#     if tweets is None:
#         #* get tweets
#         print(f'{datetime.now()} - Getting tweets...')
#         tweets = await client.search_tweet(QUERY, product='Top')  # Requête avec les mots-clés UVBF
#     else:
#         wait_time = randint(5, 10)
#         print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
#         await asyncio.sleep(wait_time)
#         tweets = await tweets.next()
#     return tweets

# # Fonction principale asynchrone
# async def main():
#     #* login credentials
#     config = ConfigParser()
#     config.read('config.ini')
#     username = config['X']['username']
#     email = config['X']['email']
#     password = config['X']['password']

#     #* authenticate to X.com (anciennement Twitter)
#     client = Client(language='en-US')

#     # Vérifier si les cookies existent
#     cookies_file = 'cookies.json'
#     if not os.path.exists(cookies_file):
#         print(f"{datetime.now()} - Aucun cookie trouvé. Connexion manuelle nécessaire.")
#         await client.login(auth_info_1=username, auth_info_2=email, password=password)
#         client.save_cookies(cookies_file)
#         print(f"{datetime.now()} - Connexion réussie. Cookies sauvegardés.")
#     else:
#         client.load_cookies(cookies_file)
#         print(f"{datetime.now()} - Cookies chargés depuis {cookies_file}.")

#     tweet_count = 0
#     tweets = None
#     tweets_data = []

#     while tweet_count < MINIMUM_TWEETS:
#         try:
#             tweets = await get_tweets(tweets, client)  # Passe client à get_tweets()
#         except TooManyRequests as e:
#             rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
#             print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
#             wait_time = rate_limit_reset - datetime.now()
#             await asyncio.sleep(wait_time.total_seconds())
#             continue

#         if not tweets:
#             print(f'{datetime.now()} - No more tweets found')
#             break

#         for tweet in tweets:
#             tweet_count += 1
#             tweet_data = {
#                 'text': tweet.text,
#                 'author': tweet.user.name,
#                 'date': tweet.created_at  # Pas besoin de strftime ici
#             }
#             tweets_data.append(tweet_data)
#             print(f'{datetime.now()} - Got {tweet_count} tweets')

#             # Sauvegarde des tweets dans un fichier CSV
#             with open('tweets_uvbf.csv', 'a', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([tweet_data['text'], tweet_data['author'], tweet_data['date']])

#     # Sauvegarder aussi en JSON
#     with open('tweets_uvbf.json', 'w', encoding='utf-8') as json_file:
#         json.dump(tweets_data, json_file, ensure_ascii=False, indent=4)

#     print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')

# # Exécute la boucle asynchrone
# asyncio.run(main())



# import asyncio  # Ajoute asyncio pour gérer les coroutines
# from twikit import Client, TooManyRequests
# import time
# from datetime import datetime
# import csv
# from configparser import ConfigParser
# from random import randint
# import os

# MINIMUM_TWEETS = 10
# QUERY = '(from:elonmusk) lang:en until:2020-01-01 since:2018-01-01'

# # La fonction get_tweets devient asynchrone et prend client en paramètre
# async def get_tweets(tweets, client):
#     if tweets is None:
#         #* get tweets
#         print(f'{datetime.now()} - Getting tweets...')
#         tweets = await client.search_tweet(QUERY, product='Top')  # Ajoute await ici
#     else:
#         wait_time = randint(5, 10)
#         print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
#         await asyncio.sleep(wait_time)  # Utilise asyncio.sleep pour les fonctions asynchrones
#         tweets = await tweets.next()  # Ajoute await ici car next() peut être asynchrone
#     return tweets

# # Fonction principale asynchrone
# async def main():
#     #* login credentials
#     config = ConfigParser()
#     config.read('config.ini')
#     username = config['X']['username']
#     email = config['X']['email']
#     password = config['X']['password']

#     #* create a csv file
#     with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

#     #* authenticate to X.com (anciennement Twitter)
#     client = Client(language='en-US')

#     # Vérifier si les cookies existent
#     cookies_file = 'cookies.json'

#     if not os.path.exists(cookies_file):
#         # Si les cookies n'existent pas, se connecter et les sauvegarder
#         print(f"{datetime.now()} - Aucun cookie trouvé. Connexion manuelle nécessaire.")
#         await client.login(auth_info_1=username, auth_info_2=email, password=password)  # Ajout de await ici
#         # Sauvegarder les cookies après la connexion
#         client.save_cookies(cookies_file)
#         print(f"{datetime.now()} - Connexion réussie. Cookies sauvegardés.")
#     else:
#         # Charger les cookies existants
#         client.load_cookies(cookies_file)
#         print(f"{datetime.now()} - Cookies chargés depuis {cookies_file}.")

#     tweet_count = 0
#     tweets = None
    
#     while tweet_count < MINIMUM_TWEETS:
#         try:
#             tweets = await get_tweets(tweets, client)  # Passe client comme paramètre à get_tweets()
#         except TooManyRequests as e:
#             rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
#             print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
#             wait_time = rate_limit_reset - datetime.now()
#             await asyncio.sleep(wait_time.total_seconds())  # Utilise asyncio.sleep
#             continue
        
#         if not tweets:
#             print(f'{datetime.now()} - No more tweets found')
#             break
        
#         for tweet in tweets:
#             tweet_count += 1
#             tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
            
#             # Sauvegarde les tweets dans le fichier CSV
#             with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(tweet_data)
            
#             print(f'{datetime.now()} - Got {tweet_count} tweets')
    
#     print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')

# # Exécute la boucle asynchrone
# asyncio.run(main())















# from twikit import Client, TooManyRequests
# import time
# from datetime import datetime
# import csv
# from configparser import ConfigParser
# from random import randint


# MINIMUM_TWEETS = 10
# QUERY = '(from:elonmusk) lang:en until:2020-01-01 since:2018-01-01'


# def get_tweets(tweets):
#     if tweets is None:
#         #* get tweets
#         print(f'{datetime.now()} - Getting tweets...')
#         tweets = client.search_tweet(QUERY, product='Top')
#     else:
#         wait_time = randint(5, 10)
#         print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
#         time.sleep(wait_time)
#         tweets = tweets.next()

#     return tweets


# #* login credentials
# config = ConfigParser()
# config.read('config.ini')
# username = config['X']['username']
# email = config['X']['email']
# password = config['X']['password']

# #* create a csv file
# with open('tweets.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])



# #* authenticate to X.com
# #! 1) use the login credentials. 2) use cookies.
# client = Client(language='en-US')
# # client.login(auth_info_1=username, auth_info_2=email, password=password)
# # client.save_cookies('cookies.json')

# client.load_cookies('cookies.json')

# tweet_count = 0
# tweets = None

# while tweet_count < MINIMUM_TWEETS:

#     try:
#         tweets = get_tweets(tweets)
#     except TooManyRequests as e:
#         rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
#         print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
#         wait_time = rate_limit_reset - datetime.now()
#         time.sleep(wait_time.total_seconds())
#         continue

#     if not tweets:
#         print(f'{datetime.now()} - No more tweets found')
#         break

#     for tweet in tweets:
#         tweet_count += 1
#         tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
        
#         with open('tweets.csv', 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(tweet_data)

#     print(f'{datetime.now()} - Got {tweet_count} tweets')


# print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')