import pandas as pd
import re
import spacy
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

# Charger les stop words et le modèle de langue français avec spaCy
stop_words = set(stopwords.words('french'))
stemmer = SnowballStemmer("french")
nlp = spacy.load("fr_core_news_sm")

# Charger les données
data_df = pd.read_csv("uvbf_combined.csv")  # Remplacer par votre fichier

# # Fonction de nettoyage
# def clean_text(text):
#     # Supprimer les mentions, hashtags, URL, ponctuation, et emojis
#     text = re.sub(r'@\w+|#\w+|https?://\S+', '', text)  # Supprime @mentions, #hashtags, et URLs
#     text = re.sub(r'[^\w\s]', '', text)                 # Supprime la ponctuation
#     text = re.sub(r'\d+', '', text)                     # Supprime les nombres
#     text = text.lower()                                 # Convertit en minuscules

#     # Tokenisation et suppression des stop words
#     tokens = word_tokenize(text)
#     tokens = [word for word in tokens if word not in stop_words]

#     # Lemmatisation ou stemming
#     tokens = [stemmer.stem(word) for word in tokens]    # Utilise le stemming
#     # Pour la lemmatisation avec spaCy, remplacez par :
#     # tokens = [token.lemma_ for token in nlp(" ".join(tokens))]

#     return ' '.join(tokens)

# Fonction de nettoyage
def clean_text(text):
    # Supprimer les mentions, hashtags, URL
    text = re.sub(r'@\w+|#\w+|https?://\S+', '', text)  # Supprime @mentions, #hashtags, et URLs
    text = re.sub(r'[^\w\s]', '', text)                 # Supprime la ponctuation
    text = re.sub(r'\d+', '', text)                     # Supprime les nombres
    text = text.lower()                                 # Convertit en minuscules

    # Supprimer les emojis
    text = re.sub(r'[^\x00-\x7F]+', '', text)           # Supprime les emojis et autres caractères non-ASCII

    # Tokenisation et suppression des stop words
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatisation ou stemming
    tokens = [stemmer.stem(word) for word in tokens]    # Utilise le stemming
    # Pour la lemmatisation avec spaCy, remplacez par :
    # tokens = [token.lemma_ for token in nlp(" ".join(tokens))]

    return ' '.join(tokens)


# Appliquer le nettoyage au texte
data_df['Texte_nettoye'] = data_df['Texte'].apply(clean_text)

# Sauvegarder le texte nettoyé
data_df.to_csv("uvbf_cleaned.csv", index=False, encoding='utf-8')
print("Le texte a été nettoyé et sauvegardé dans 'uvbf_cleaned.csv'.")
