import asyncio
from twikit import Client, TooManyRequests
from datetime import datetime
import csv
import json
from configparser import ConfigParser
from random import randint
import os
import time

# Constantes de configuration
MINIMUM_TWEETS = 1000
QUERY = '(Université UVBF OR UVBF OR #UVBF OR "Université Virtuelle du Burkina Faso" OR "UV-BF" OR "UV BF" OR "UV_BF") lang:fr'
MAX_RETRIES = 3
RATE_LIMIT_PAUSE = 60
OUTPUT_FILE = 'publications1_uvbf.csv'  # Définition du nom de fichier comme constante

# [Le reste des fonctions get_comments, get_tweets, process_tweet_batch reste identique]
async def get_comments(client, tweet_id, retry_count=0):
    """
    Fonction optimisée pour récupérer les commentaires
    """
    comments = []
    try:
        replies = await client.search_tweet(f"conversation_id:{tweet_id}", product='Latest')
        
        if replies:
            for reply in replies:
                comment_data = {
                    'text': reply.text,
                    'author': reply.user.name if reply.user else 'Unknown',
                    'date': reply.created_at
                }
                comments.append(comment_data)
        
        await asyncio.sleep(1 if not comments else 0.5)
        
    except TooManyRequests as e:
        if retry_count < MAX_RETRIES:
            print(f'{datetime.now()} - Rate limit hit, waiting {RATE_LIMIT_PAUSE} seconds...')
            await asyncio.sleep(RATE_LIMIT_PAUSE)
            return await get_comments(client, tweet_id, retry_count + 1)
        else:
            print(f'{datetime.now()} - Max retries reached for tweet {tweet_id}')
            return []
    except Exception as e:
        print(f'{datetime.now()} - Error fetching comments for tweet {tweet_id}: {str(e)}')
        return []
        
    return comments

async def get_tweets(tweets, client, retry_count=0):
    """
    Fonction optimisée pour récupérer les tweets
    """
    try:
        if tweets is None:
            print(f'{datetime.now()} - Getting tweets...')
            tweets = await client.search_tweet(QUERY, product='Latest')
        else:
            wait_time = randint(2, 5)
            print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
            await asyncio.sleep(wait_time)
            tweets = await tweets.next()
    except TooManyRequests as e:
        if retry_count < MAX_RETRIES:
            print(f'{datetime.now()} - Rate limit hit, waiting {RATE_LIMIT_PAUSE} seconds...')
            await asyncio.sleep(RATE_LIMIT_PAUSE)
            return await get_tweets(tweets, client, retry_count + 1)
        else:
            print(f'{datetime.now()} - Max retries reached for getting tweets')
            return None
    except Exception as e:
        print(f'{datetime.now()} - Error getting tweets: {str(e)}')
        return None
    
    return tweets

async def process_tweet_batch(tweets_batch, client, writer):
    """
    Traite un lot de tweets et leurs commentaires en parallèle
    """
    tasks = []
    for tweet in tweets_batch:
        tasks.append(process_single_tweet(tweet, client, writer))
    await asyncio.gather(*tasks)

async def process_single_tweet(tweet, client, writer):
    """
    Traite un seul tweet et ses commentaires et les sauvegarde au même format
    """
    # Sauvegarde du tweet
    writer.writerow([
        tweet.user.name if tweet.user else 'Unknown',
        tweet.text,
        tweet.created_at
    ])

    # Récupération et sauvegarde des commentaires
    comments = await get_comments(client, tweet.id)
    for comment in comments:
        writer.writerow([
            comment['author'],
            comment['text'],
            comment['date']
        ])

    print(f'{datetime.now()} - Processed tweet {tweet.id} with {len(comments)} comments')

async def main():
    """
    Fonction principale optimisée
    """
    # Configuration initiale
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    client = Client(language='en-US')
    cookies_file = 'cookies.json'

    # Gestion de l'authentification
    if not os.path.exists(cookies_file):
        print(f"{datetime.now()} - Aucun cookie trouvé. Connexion manuelle nécessaire.")
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies(cookies_file)
        print(f"{datetime.now()} - Connexion réussie. Cookies sauvegardés.")
    else:
        client.load_cookies(cookies_file)
        print(f"{datetime.now()} - Cookies chargés depuis {cookies_file}.")

    # Initialisation du CSV avec le nouveau format
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Auteur', 'Texte', 'Date'])  # Nouveaux en-têtes simplifiés
        
        tweet_count = 0
        tweets = None
        start_time = time.time()

        while tweet_count < MINIMUM_TWEETS:
            tweets = await get_tweets(tweets, client)
            
            if not tweets:
                print(f'{datetime.now()} - No more tweets found')
                break

            # Traitement des tweets par lots
            current_batch = []
            for tweet in tweets:
                tweet_count += 1
                current_batch.append(tweet)
                
                if len(current_batch) >= 5:
                    await process_tweet_batch(current_batch, client, writer)
                    current_batch = []
            
            # Traiter le dernier lot
            if current_batch:
                await process_tweet_batch(current_batch, client, writer)

            # Statistiques de progression
            elapsed_time = time.time() - start_time
            tweets_per_second = tweet_count / elapsed_time
            print(f'{datetime.now()} - Progress: {tweet_count} items collected. '
                  f'Rate: {tweets_per_second:.2f} items/second')

    # Message de fin avec le chemin complet du fichier
    file_path = OUTPUT_FILE
    print(f'{datetime.now()} - Collection completed! Total: {tweet_count} items')
    print(f'{datetime.now()} - Les données ont été sauvegardées dans : {file_path}')

if __name__ == "__main__":
    asyncio.run(main())


# # Importation des bibliothèques nécessaires
# import asyncio
# from twikit import Client, TooManyRequests
# from datetime import datetime
# import csv
# import json
# from configparser import ConfigParser
# from random import randint
# import os
# import time

# # Constantes de configuration
# MINIMUM_TWEETS = 1000
# QUERY = '(Université UVBF OR UVBF OR #UVBF OR "Université Virtuelle du Burkina Faso" OR "UV-BF" OR "UV BF" OR "UV_BF") lang:fr'
# MAX_RETRIES = 3  # Nombre maximum de tentatives en cas d'erreur
# RATE_LIMIT_PAUSE = 60  # Pause en secondes après avoir atteint la limite

# async def get_comments(client, tweet_id, retry_count=0):
#     """
#     Fonction optimisée pour récupérer les commentaires
#     """
#     comments = []
#     try:
#         # Récupération des réponses au tweet avec gestion des erreurs
#         replies = await client.search_tweet(f"conversation_id:{tweet_id}", product='Latest')
        
#         if replies:
#             for reply in replies:
#                 comment_data = {
#                     'text': reply.text,
#                     'author': reply.user.name if reply.user else 'Unknown',
#                     'date': reply.created_at
#                 }
#                 comments.append(comment_data)
        
#         # Délai dynamique basé sur le nombre de commentaires trouvés
#         await asyncio.sleep(1 if not comments else 0.5)
        
#     except TooManyRequests as e:
#         if retry_count < MAX_RETRIES:
#             print(f'{datetime.now()} - Rate limit hit, waiting {RATE_LIMIT_PAUSE} seconds...')
#             await asyncio.sleep(RATE_LIMIT_PAUSE)
#             return await get_comments(client, tweet_id, retry_count + 1)
#         else:
#             print(f'{datetime.now()} - Max retries reached for tweet {tweet_id}')
#             return []
#     except Exception as e:
#         print(f'{datetime.now()} - Error fetching comments for tweet {tweet_id}: {str(e)}')
#         return []
        
#     return comments

# async def get_tweets(tweets, client, retry_count=0):
#     """
#     Fonction optimisée pour récupérer les tweets
#     """
#     try:
#         if tweets is None:
#             print(f'{datetime.now()} - Getting tweets...')
#             tweets = await client.search_tweet(QUERY, product='Latest')
#         else:
#             wait_time = randint(2, 5)  # Réduit le temps d'attente
#             print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
#             await asyncio.sleep(wait_time)
#             tweets = await tweets.next()
#     except TooManyRequests as e:
#         if retry_count < MAX_RETRIES:
#             print(f'{datetime.now()} - Rate limit hit, waiting {RATE_LIMIT_PAUSE} seconds...')
#             await asyncio.sleep(RATE_LIMIT_PAUSE)
#             return await get_tweets(tweets, client, retry_count + 1)
#         else:
#             print(f'{datetime.now()} - Max retries reached for getting tweets')
#             return None
#     except Exception as e:
#         print(f'{datetime.now()} - Error getting tweets: {str(e)}')
#         return None
    
#     return tweets

# async def process_tweet_batch(tweets_batch, client, writer):
#     """
#     Traite un lot de tweets en parallèle
#     """
#     tasks = []
#     for tweet in tweets_batch:
#         tasks.append(process_single_tweet(tweet, client, writer))
#     await asyncio.gather(*tasks)

# async def process_single_tweet(tweet, client, writer):
#     """
#     Traite un seul tweet et ses commentaires
#     """
#     tweet_data = {
#         'type': 'tweet',
#         'id': tweet.id,
#         'text': tweet.text,
#         'author': tweet.user.name if tweet.user else 'Unknown',
#         'date': tweet.created_at,
#         'parent_tweet_id': ''
#     }
    
#     # Sauvegarde du tweet
#     writer.writerow([
#         tweet_data['type'],
#         tweet_data['text'],
#         tweet_data['author'],
#         tweet_data['date'],
#         tweet_data['parent_tweet_id']
#     ])

#     # Récupération des commentaires
#     comments = await get_comments(client, tweet.id)
    
#     # Sauvegarde des commentaires
#     for comment in comments:
#         writer.writerow([
#             'comment',
#             comment['text'],
#             comment['author'],
#             comment['date'],
#             tweet.id
#         ])

#     print(f'{datetime.now()} - Processed tweet {tweet.id} with {len(comments)} comments')

# async def main():
#     """
#     Fonction principale optimisée
#     """
#     # Configuration initiale
#     config = ConfigParser()
#     config.read('config.ini')
#     username = config['X']['username']
#     email = config['X']['email']
#     password = config['X']['password']

#     client = Client(language='en-US')
#     cookies_file = 'cookies.json'

#     # Gestion de l'authentification
#     if not os.path.exists(cookies_file):
#         print(f"{datetime.now()} - Aucun cookie trouvé. Connexion manuelle nécessaire.")
#         await client.login(auth_info_1=username, auth_info_2=email, password=password)
#         client.save_cookies(cookies_file)
#         print(f"{datetime.now()} - Connexion réussie. Cookies sauvegardés.")
#     else:
#         client.load_cookies(cookies_file)
#         print(f"{datetime.now()} - Cookies chargés depuis {cookies_file}.")

#     # Initialisation du CSV
#     with open('tweets_uvbf.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Type', 'Text', 'Author', 'Date', 'Parent_Tweet_ID'])
        
#         tweet_count = 0
#         tweets = None
#         start_time = time.time()

#         while tweet_count < MINIMUM_TWEETS:
#             tweets = await get_tweets(tweets, client)
            
#             if not tweets:
#                 print(f'{datetime.now()} - No more tweets found')
#                 break

#             # Traitement des tweets par lots
#             current_batch = []
#             for tweet in tweets:
#                 tweet_count += 1
#                 current_batch.append(tweet)
                
#                 if len(current_batch) >= 5:  # Traiter par lots de 5 tweets
#                     await process_tweet_batch(current_batch, client, writer)
#                     current_batch = []
            
#             # Traiter le dernier lot s'il en reste
#             if current_batch:
#                 await process_tweet_batch(current_batch, client, writer)

#             # Afficher les statistiques de progression
#             elapsed_time = time.time() - start_time
#             tweets_per_second = tweet_count / elapsed_time
#             print(f'{datetime.now()} - Progress: {tweet_count} tweets collected. '
#                   f'Rate: {tweets_per_second:.2f} tweets/second')

#     print(f'{datetime.now()} - Collection completed! Total: {tweet_count} tweets')

# if __name__ == "__main__":
#     asyncio.run(main())




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