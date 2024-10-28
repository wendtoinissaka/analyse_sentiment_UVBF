import pandas as pd
import numpy as np

# Lire les fichiers CSV avec le délimiteur virgule
facebook_df = pd.read_csv("uvbf_facebook.csv", delimiter=',')
tweets_df = pd.read_csv("publications_uvbf_tweet.csv", delimiter=',')
# tweets_df = pd.read_csv("tweets_uvbf.csv", delimiter=',')

# Vérifier et harmoniser les colonnes
print("Colonnes du fichier Facebook avant harmonisation:", facebook_df.columns)
if len(facebook_df.columns) == 2:
    facebook_df.columns = ['Auteur', 'Texte']
    facebook_df['Date'] = '01/01/2018'  # Ajouter la date par défaut pour les publications Facebook
else:
    print("Attention : Le fichier 'uvbf_facebook.csv' n'a pas deux colonnes comme attendu.")

print("Colonnes du fichier Tweets avant harmonisation:", tweets_df.columns)
if len(tweets_df.columns) == 3:
    tweets_df.columns = ['Texte', 'Auteur', 'Date']
else:
    print("Attention : Le fichier 'tweets_uvbf.csv' n'a pas trois colonnes comme attendu.")

# Convertir les dates des tweets en format français (jj/mm/aaaa)
tweets_df['Date'] = pd.to_datetime(tweets_df['Date'], errors='coerce').dt.strftime('%d/%m/%Y')

# Fusionner les DataFrames
merged_df = pd.concat([facebook_df, tweets_df], ignore_index=True)

# Exporter le DataFrame fusionné vers un nouveau fichier CSV
merged_df.to_csv("uvbf_combined1.csv", index=False, encoding='utf-8')

print("Les fichiers ont été fusionnés avec succès et sauvegardés dans 'uvbf_combined.csv'.")


# import pandas as pd
# import numpy as np

# # Lire les fichiers CSV avec le délimiteur virgule
# facebook_df = pd.read_csv("uvbf_facebook.csv", delimiter=',')
# tweets_df = pd.read_csv("tweets_uvbf.csv", delimiter=',')

# # Vérifier et harmoniser les colonnes
# print("Colonnes du fichier Facebook avant harmonisation:", facebook_df.columns)
# if len(facebook_df.columns) == 2:
#     facebook_df.columns = ['Auteur', 'Texte']
#     facebook_df['Date'] = np.nan  # Ajouter une colonne "Date" vide pour les publications Facebook
# else:
#     print("Attention : Le fichier 'uvbf_facebook.csv' n'a pas deux colonnes comme attendu.")

# print("Colonnes du fichier Tweets avant harmonisation:", tweets_df.columns)
# if len(tweets_df.columns) == 3:
#     tweets_df.columns = ['Texte', 'Auteur', 'Date']
# else:
#     print("Attention : Le fichier 'tweets_uvbf.csv' n'a pas trois colonnes comme attendu.")

# # Convertir les dates des tweets en format français (jj/mm/aaaa)
# tweets_df['Date'] = pd.to_datetime(tweets_df['Date'], errors='coerce').dt.strftime('%d/%m/%Y')

# # Fusionner les DataFrames
# merged_df = pd.concat([facebook_df, tweets_df], ignore_index=True)

# # Exporter le DataFrame fusionné vers un nouveau fichier CSV
# merged_df.to_csv("uvbf_combined.csv", index=False, encoding='utf-8')

# print("Les fichiers ont été fusionnés avec succès et sauvegardés dans 'uvbf_combined.csv'.")



# import pandas as pd

# # Lire les fichiers CSV avec le délimiteur virgule
# facebook_df = pd.read_csv("uvbf_facebook.csv", delimiter=',')
# tweets_df = pd.read_csv("tweets_uvbf.csv", delimiter=',')

# # Vérifier la structure des colonnes et harmoniser les noms
# print("Colonnes du fichier Facebook avant harmonisation:", facebook_df.columns)
# if len(facebook_df.columns) == 2:
#     facebook_df.columns = ['Auteur', 'Texte']
# else:
#     print("Attention : Le fichier 'uvbf_facebook.csv' n'a pas deux colonnes comme attendu.")

# print("Colonnes du fichier Tweets avant harmonisation:", tweets_df.columns)
# if len(tweets_df.columns) == 3:
#     tweets_df.columns = ['Texte', 'Auteur', 'Date']
# else:
#     print("Attention : Le fichier 'tweets_uvbf.csv' n'a pas trois colonnes comme attendu.")

# # Fusionner les DataFrames
# merged_df = pd.concat([facebook_df, tweets_df[['Auteur', 'Texte']]], ignore_index=True)

# # Exporter le DataFrame fusionné vers un nouveau fichier CSV
# merged_df.to_csv("uvbf_combined.csv", index=False, encoding='utf-8')

# print("Les fichiers ont été fusionnés avec succès et sauvegardés dans 'uvbf_combined.csv'.")
