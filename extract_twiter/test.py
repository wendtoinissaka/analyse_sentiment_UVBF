from configparser import ConfigParser
import tweepy
import csv

# Lecture des clés API depuis config.ini
config = ConfigParser()
config.read('config.ini')

# Récupération des clés
bearer_token = config['Twitter']['bearer_token']

# Authentification avec l'API Tweepy pour l'API v2
client = tweepy.Client(bearer_token=bearer_token)

# Tester l'authentification
try:
    response = client.get_me()
    print("Authentication successful!")
    print(response.data)
except Exception as e:
    print(f'Error during authentication: {e}')

# Fonction pour rechercher des tweets
def search_tweets(keywords, max_results=100):
    try:
        tweets = client.search_recent_tweets(query=keywords, max_results=max_results, tweet_fields=['created_at', 'author_id'])
        return tweets.data
    except Exception as e:
        print(f'Error while searching tweets: {e}')
        return []

# Sauvegarder les tweets dans un fichier CSV
def save_tweets_to_csv(tweets, filename='tweets.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Auteur ID', 'Texte'])  # Écrire l'en-tête

        for tweet in tweets:
            tweet_date = tweet.created_at
            tweet_author_id = tweet.author_id
            tweet_text = tweet.text
            writer.writerow([tweet_date, tweet_author_id, tweet_text])

# Mots-clés à rechercher
keywords = '"Université UVBF" OR "UVBF" OR #UVBF'

# Recherche et sauvegarde des tweets
tweets = search_tweets(keywords)
if tweets:
    save_tweets_to_csv(tweets)
    print(f'{len(tweets)} tweets saved to tweets.csv')
else:
    print('No tweets found or an error occurred.')


# from configparser import ConfigParser
# import tweepy

# # Lecture des clés API depuis config.ini
# config = ConfigParser()
# config.read('config.ini')

# # Récupération des clés
# consumer_key = config['Twitter']['consumer_key']
# consumer_secret = config['Twitter']['consumer_secret']
# access_token = config['Twitter']['access_token']
# access_token_secret = config['Twitter']['access_token_secret']
# bearer_token = config['Twitter']['bearer_token']

# # Authentification avec l'API Tweepy
# auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
# api = tweepy.API(auth)

# # Tester l'authentification
# try:
#     response = api.verify_credentials()  # Vérifiez les informations d'identification
#     print("Authentication successful!")
#     print(response)
# except Exception as e:
#     print(f'Error during authentication: {e}')
