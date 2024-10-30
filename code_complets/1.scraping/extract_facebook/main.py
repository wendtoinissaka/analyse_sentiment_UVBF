from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

# Configurer Selenium avec ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Accéder à Facebook et demander à l'utilisateur de se connecter manuellement
driver.get('https://www.facebook.com')
input("Connecte-toi à Facebook manuellement, puis appuie sur Entrée ici pour continuer...")

# Attendre que la page charge
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
print("Page chargée. Recherche effectuée.")

# Étape 1 : Effectuer une recherche pour "UVBF"
search_box = driver.find_element(By.XPATH, "//input[@type='search']")
search_box.send_keys('UVBF')  # Recherche du terme UVBF
search_box.send_keys(Keys.RETURN)  # Simuler la touche "Entrée"
print("Recherche effectuée pour 'UVBF'.")

# Attendre que les résultats de recherche apparaissent
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Publications']")))
print("Filtre 'Publications' sélectionné.")

# Étape 2 : Accéder à la section "Filtres" et choisir "Publications"
publications_filter = driver.find_element(By.XPATH, "//span[text()='Publications']")
publications_filter.click()

# Attendre que les publications se chargent
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Publications de']")))
print("Filtre 'Publications de' sélectionné.")

# Étape 3 : Filtrer par "Publications de"
publications_de_filter = driver.find_element(By.XPATH, "//input[@placeholder='Publications de']")
publications_de_filter.click()

# Attendre que l'input soit actif
time.sleep(2)  # Juste pour donner un peu de temps

# Utiliser WebDriverWait pour attendre que l'option "Publications publiques" soit cliquable
publications_publiques_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Publications publiques']"))
)

# Faire défiler jusqu'à l'élément avant de cliquer
driver.execute_script("arguments[0].scrollIntoView();", publications_publiques_option)
publications_publiques_option.click()
print("Option 'Publications publiques' sélectionnée.")

# Attendre que les publications publiques se chargent
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='article']")))
    print("Publications chargées.")
except Exception as e:
    print("Erreur lors de l'attente des publications : ", e)

# Créer un fichier CSV pour sauvegarder les résultats
with open('publications_uvbf.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Auteur', 'Texte', 'Date'])
    print("Fichier CSV créé.")

    # Extraire le contenu de la page avec BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Trouver les publications sur la page
    publications = soup.find_all('div', {'role': 'article'})  # Met à jour la classe
    print(f"Nombre de publications trouvées : {len(publications)}")

    # Extraire les informations des publications
    for index, post in enumerate(publications):
        try:
            # Afficher le contenu brut du post pour le débogage
            print(f"[Post {index + 1}] Contenu brut : {post}")

            # Extraire le texte de la publication
            texte_post = post.find('div', {'data-ad-preview': 'message'})  # Ajustez ce sélecteur si nécessaire
            texte_post = texte_post.text.strip() if texte_post else 'Texte indisponible'
            print(f"[Post {index + 1}] Texte : {texte_post}")

            # Extraire la date de publication
            date_post = post.find('abbr')
            date_post = date_post.text.strip() if date_post else 'Inconnue'
            print(f"[Post {index + 1}] Date : {date_post}")

            # Extraire le nom de l'auteur
            auteur_post = post.find('h3')
            if auteur_post:
                auteur_span = auteur_post.find('span')
                auteur_post = auteur_span.text.strip() if auteur_span else 'Inconnu'
            else:
                auteur_post = 'Inconnu'
            print(f"[Post {index + 1}] Auteur : {auteur_post}")

            writer.writerow([auteur_post, texte_post, date_post])
            print(f"Auteur: {auteur_post}, Date: {date_post}, Texte: {texte_post[:50]}...")

        except Exception as e:
            print(f"Erreur lors de l'extraction des données pour le post {index + 1}: {e}")

# Vérifier si des publications ont été trouvées avant de défiler
if len(publications) == 0:
    print("Aucune publication trouvée. Aucune nécessité de défiler pour charger plus de données.")
else:
    # Étape 5 : Faire défiler la page plusieurs fois pour charger plus de publications
    def scroll_down(driver, scroll_times):
        for i in range(scroll_times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Défilement {i + 1} effectué.")
            time.sleep(5)  # Temps d'attente pour charger plus de publications

    # Effectuer plusieurs scrolls pour charger plus de contenu
    scroll_times = 10  # Ajuste selon le nombre de publications que tu veux récupérer
    scroll_down(driver, scroll_times)

# Fermer le navigateur une fois terminé
driver.quit()
print("Scraping terminé. Les données sont sauvegardées dans 'publications_uvbf.csv'.")

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import time
# import csv

# # Configurer Selenium avec ChromeDriverManager
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # Accéder à Facebook et demander à l'utilisateur de se connecter manuellement
# driver.get('https://www.facebook.com')
# input("Connecte-toi à Facebook manuellement, puis appuie sur Entrée ici pour continuer...")

# # Attendre que la page charge
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
# print("Page chargée. Recherche effectuée.")

# # Étape 1 : Effectuer une recherche pour "UVBF"
# search_box = driver.find_element(By.XPATH, "//input[@type='search']")
# search_box.send_keys('UVBF')  # Recherche du terme UVBF
# search_box.send_keys(Keys.RETURN)  # Simuler la touche "Entrée"
# print("Recherche effectuée pour 'UVBF'.")

# # Attendre que les résultats de recherche apparaissent
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Publications']")))
# print("Filtre 'Publications' sélectionné.")

# # Étape 2 : Accéder à la section "Filtres" et choisir "Publications"
# publications_filter = driver.find_element(By.XPATH, "//span[text()='Publications']")
# publications_filter.click()

# # Attendre que les publications se chargent
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Publications de']")))
# print("Filtre 'Publications de' sélectionné.")

# # Étape 3 : Filtrer par "Publications de"
# publications_de_filter = driver.find_element(By.XPATH, "//input[@placeholder='Publications de']")
# publications_de_filter.click()

# # Attendre que l'input soit actif
# time.sleep(2)  # Juste pour donner un peu de temps

# # Utiliser WebDriverWait pour attendre que l'option "Publications publiques" soit cliquable
# publications_publiques_option = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//span[text()='Publications publiques']"))
# )

# # Faire défiler jusqu'à l'élément avant de cliquer
# driver.execute_script("arguments[0].scrollIntoView();", publications_publiques_option)
# publications_publiques_option.click()
# print("Option 'Publications publiques' sélectionnée.")

# # Attendre que les publications publiques se chargent
# try:
#     WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='article']")))
#     print("Publications chargées.")
# except Exception as e:
#     print("Erreur lors de l'attente des publications : ", e)

# # Étape 4 : Extraire le contenu de la page avec BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'lxml')

# # Trouver les publications sur la page
# publications = soup.find_all('div', {'role': 'article'})  # Met à jour la classe

# # Vérifier combien de publications ont été trouvées
# print(f"Nombre de publications trouvées : {len(publications)}")

# # Créer un fichier CSV pour sauvegarder les résultats
# with open('publications_uvbf.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Auteur', 'Texte', 'Date'])
#     print("Fichier CSV créé.")

#     # Extraire les informations des publications
#     for index, post in enumerate(publications):
#         try:
#             # Afficher le contenu brut du post pour le débogage
#             print(f"[Post {index + 1}] Contenu brut : {post}")

#             # Extraire le texte de la publication
#             texte_post = post.find('div', {'data-ad-preview': 'message'}).text.strip() if post.find('div', {'data-ad-preview': 'message'}) else 'Texte indisponible'
#             print(f"[Post {index + 1}] Texte : {texte_post}")

#             # Extraire la date de publication
#             date_post = post.find('abbr')
#             date_post = date_post.text.strip() if date_post else 'Inconnue'
#             print(f"[Post {index + 1}] Date : {date_post}")

#             # Extraire le nom de l'auteur
#             auteur_post = post.find('h3')
#             if auteur_post:
#                 auteur_span = auteur_post.find('span')
#                 auteur_post = auteur_span.text.strip() if auteur_span else 'Inconnu'
#             else:
#                 auteur_post = 'Inconnu'
#             print(f"[Post {index + 1}] Auteur : {auteur_post}")

#             writer.writerow([auteur_post, texte_post, date_post])
#             print(f"Auteur: {auteur_post}, Date: {date_post}, Texte: {texte_post[:50]}...")
#         except Exception as e:
#             print(f"Erreur lors de l'extraction des données pour le post {index + 1}: {e}")

# # Vérifier si des publications ont été trouvées avant de défiler
# if len(publications) == 0:
#     print("Aucune publication trouvée. Aucune nécessité de défiler pour charger plus de données.")
# else:
#     # Étape 5 : Faire défiler la page plusieurs fois pour charger plus de publications
#     def scroll_down(driver, scroll_times):
#         for i in range(scroll_times):
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             print(f"Défilement {i + 1} effectué.")
#             time.sleep(5)  # Temps d'attente pour charger plus de publications

#     # Effectuer plusieurs scrolls pour charger plus de contenu
#     scroll_times = 10  # Ajuste selon le nombre de publications que tu veux récupérer
#     scroll_down(driver, scroll_times)

# # Fermer le navigateur une fois terminé
# driver.quit()
# print("Scraping terminé. Les données sont sauvegardées dans 'publications_uvbf.csv'.")


#26 OCTOBRE 2024
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import time
# import csv

# # Configurer Selenium avec ChromeDriverManager
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # Accéder à Facebook et demander à l'utilisateur de se connecter manuellement
# driver.get('https://www.facebook.com')
# input("Connecte-toi à Facebook manuellement, puis appuie sur Entrée ici pour continuer...")

# # Attendre que la page charge
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))

# # Étape 1 : Effectuer une recherche pour "UVBF"
# search_box = driver.find_element(By.XPATH, "//input[@type='search']")
# search_box.send_keys('UVBF')  # Recherche du terme UVBF
# search_box.send_keys(Keys.RETURN)  # Simuler la touche "Entrée"

# # Attendre que les résultats de recherche apparaissent
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Publications']")))

# # Étape 2 : Accéder à la section "Filtres" et choisir "Publications"
# publications_filter = driver.find_element(By.XPATH, "//span[text()='Publications']")
# publications_filter.click()

# # Attendre que les publications se chargent
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Publications de']")))

# # Étape 3 : Filtrer par "Publications de"
# publications_de_filter = driver.find_element(By.XPATH, "//input[@placeholder='Publications de']")
# publications_de_filter.click()

# # Attendre que l'input soit actif
# WebDriverWait(driver, 2)

# # Utiliser WebDriverWait pour attendre que l'option "Publications publiques" soit cliquable
# publications_publiques_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Publications publiques']")))

# # Faire défiler jusqu'à l'élément avant de cliquer
# driver.execute_script("arguments[0].scrollIntoView();", publications_publiques_option)
# publications_publiques_option.click()

# # Attendre que les publications publiques se chargent
# WebDriverWait(driver, 10)

# # Étape 4 : Faire défiler la page plusieurs fois pour charger plus de publications
# def scroll_down(driver, scroll_times):
#     for i in range(scroll_times):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         print(f"Défilement {i + 1} effectué.")
#         time.sleep(5)

# # Effectuer plusieurs scrolls pour charger plus de contenu
# scroll_times = 10  # Ajuste selon le nombre de publications que tu veux récupérer
# scroll_down(driver, scroll_times)

# # Étape 5 : Extraire le contenu de la page avec BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'lxml')

# # Trouver les publications sur la page
# publications = soup.find_all('div', {'class': 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'})

# # Vérifier combien de publications ont été trouvées
# print(f"Nombre de publications trouvées : {len(publications)}")

# # Créer un fichier CSV pour sauvegarder les résultats
# with open('publications_uvbf.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Auteur', 'Texte', 'Date'])

#     # Extraire les informations des publications
#     for index, post in enumerate(publications):
#         try:
#             # Extraire le texte de la publication
#             texte_post = post.find('div', {'class': 'ecm0bbzt e5nlhep0 a8c37x1j'})
#             texte_post = texte_post.text.strip() if texte_post else 'Texte indisponible'
#             print(f"[Post {index + 1}] Texte : {texte_post}")

#             # Extraire la date de publication
#             date_post = post.find('abbr')
#             date_post = date_post.text.strip() if date_post else 'Inconnue'
#             print(f"[Post {index + 1}] Date : {date_post}")

#             # Extraire le nom de l'auteur
#             auteur_post = post.find('h3')  # On utilise h3 ici
#             if auteur_post:
#                 auteur_span = auteur_post.find('span')
#                 auteur_post = auteur_span.text.strip() if auteur_span else 'Inconnu'
#             else:
#                 auteur_post = 'Inconnu'
#             print(f"[Post {index + 1}] Auteur : {auteur_post}")

#             writer.writerow([auteur_post, texte_post, date_post])
#             print(f"Auteur: {auteur_post}, Date: {date_post}, Texte: {texte_post[:50]}...")
#         except Exception as e:
#             print(f"Erreur lors de l'extraction des données pour le post {index + 1}: {e}")
#             continue

# # Fermer le navigateur une fois terminé
# driver.quit()

# print("Scraping terminé. Les données sont sauvegardées dans 'publications_uvbf.csv'.")





# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import time
# import csv

# # Configurer Selenium avec ChromeDriverManager
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # Accéder à Facebook et demander à l'utilisateur de se connecter manuellement
# driver.get('https://www.facebook.com')
# input("Connecte-toi à Facebook manuellement, puis appuie sur Entrée ici pour continuer...")

# # Attendre que la page charge
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))

# # Étape 1 : Effectuer une recherche pour "UVBF"
# search_box = driver.find_element(By.XPATH, "//input[@type='search']")
# search_box.send_keys('UVBF')  # Recherche du terme UVBF
# search_box.send_keys(Keys.RETURN)  # Simuler la touche "Entrée"

# # Attendre que les résultats de recherche apparaissent
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Publications']")))

# # Étape 2 : Accéder à la section "Filtres" et choisir "Publications"
# publications_filter = driver.find_element(By.XPATH, "//span[text()='Publications']")
# publications_filter.click()

# # Attendre que les publications se chargent
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Publications de']")))

# # Étape 3 : Filtrer par "Publications de"
# publications_de_filter = driver.find_element(By.XPATH, "//input[@placeholder='Publications de']")
# publications_de_filter.click()

# # Attendre que l'input soit actif
# WebDriverWait(driver, 2)

# # Utiliser WebDriverWait pour attendre que l'option "Publications publiques" soit cliquable
# publications_publiques_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Publications publiques']")))

# # Faire défiler jusqu'à l'élément avant de cliquer
# driver.execute_script("arguments[0].scrollIntoView();", publications_publiques_option)
# publications_publiques_option.click()

# # Attendre que les publications publiques se chargent
# WebDriverWait(driver, 10)

# # Étape 4 : Faire défiler la page plusieurs fois pour charger plus de publications
# def scroll_down(driver, scroll_times):
#     for i in range(scroll_times):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         print(f"Défilement {i + 1} effectué.")
#         time.sleep(5)

# # Effectuer plusieurs scrolls pour charger plus de contenu
# scroll_times = 10  # Ajuste selon le nombre de publications que tu veux récupérer
# scroll_down(driver, scroll_times)

# # Étape 5 : Extraire le contenu de la page avec BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'lxml')

# # Trouver les publications sur la page
# publications = soup.find_all('div', {'class': 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'})

# # Vérifier combien de publications ont été trouvées
# print(f"Nombre de publications trouvées : {len(publications)}")

# # Créer un fichier CSV pour sauvegarder les résultats
# with open('publications_uvbf.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Auteur', 'Texte', 'Date'])

#     # Extraire les informations des publications
#     for index, post in enumerate(publications):
#         try:
#             # Extraire le texte de la publication
#             texte_post = post.find('div', {'class': 'ecm0bbzt e5nlhep0 a8c37x1j'})
#             texte_post = texte_post.text.strip() if texte_post else 'Texte indisponible'
#             print(f"[Post {index + 1}] Texte : {texte_post}")

#             # Extraire la date de publication
#             date_post = post.find('abbr')
#             date_post = date_post.text.strip() if date_post else 'Inconnue'
#             print(f"[Post {index + 1}] Date : {date_post}")

#             # Extraire le nom de l'auteur
#             auteur_post = post.find('h3')  # On utilise h3 ici
#             if auteur_post:
#                 auteur_span = auteur_post.find('span')
#                 auteur_post = auteur_span.text.strip() if auteur_span else 'Inconnu'
#             else:
#                 auteur_post = 'Inconnu'
#             print(f"[Post {index + 1}] Auteur : {auteur_post}")

#             writer.writerow([auteur_post, texte_post, date_post])
#             print(f"Auteur: {auteur_post}, Date: {date_post}, Texte: {texte_post[:50]}...")
#         except Exception as e:
#             print(f"Erreur lors de l'extraction des données pour le post {index + 1}: {e}")
#             continue

# # Fermer le navigateur une fois terminé
# driver.quit()

# print("Scraping terminé. Les données sont sauvegardées dans 'publications_uvbf.csv'.")
