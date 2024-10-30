from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Initialisation de Selenium et connexion à Facebook
s = Service("/usr/local/bin/chromedriver")
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-webrtc")

driver = webdriver.Chrome(service=s, options=chrome_options)

# Se connecter à Facebook
driver.get("https://www.facebook.com/login")
time.sleep(10)

# Connexion à Facebook
email = "flambieali@gmail.com"
password = "FLAM0756"
driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "pass").send_keys(password)
driver.find_element(By.NAME, "login").click()
time.sleep(5)

# Recherche des publications contenant "UVBF"
driver.get("https://web.facebook.com/search/posts?q=universit%C3%A9%20virtuelle%20du%20burkina%20faso&filters=eyJycF9sb2NhdGlvbjowIjoie1wibmFtZVwiOlwibG9jYXRpb25cIixcImFyZ3NcIjpcIjEwODc3NzUzOTE1NDM4NlwifSJ9&locale=fr_FR")
time.sleep(5)

scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

data = []
while True:
    # Scroll jusqu'en bas de la page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    # Récupère les publications après le scroll
    posts = driver.find_elements(By.XPATH, '//div[@data-ad-preview="message"]')
    
    for post in posts:
        try:
            # Vérifie et clique sur "En voir plus" si le bouton est présent
            voir_plus = post.find_element(By.XPATH, './/div[@role="button" and @tabindex="0"]')
            voir_plus.click()
            time.sleep(1)  # Pause pour charger le texte complet
        except:
            pass

        # Tente de capturer le texte et l'auteur
        try:
            texte = post.text
            auteur = post.find_element(By.XPATH, './/a[@role="link" and @tabindex="0"]').text
        except:
            texte = "Texte non disponible"
            auteur = "Auteur inconnu"

        # Cliquer pour accéder à la page des commentaires
        commentaires = []
        try:
            comment_button = post.find_element(By.XPATH, './/div[@id=":rg8:" and @role="button" and @tabindex="0"]')
            comment_button.click()
            time.sleep(20)  # Attendre que la page des commentaires charge
            
            # Récupérer les commentaires
            commentaires_divs = driver.find_elements(By.XPATH, '//div[@class="html-div x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp"]//div[@class="xv55zj0 x1vvkbs x1rg5ohu xxymvpz"]')
            for commentaire_div in commentaires_divs:
                commentaire_texte = commentaire_div.text
                if commentaire_texte:
                    commentaires.append(commentaire_texte)
            
            # Revenir en arrière après extraction des commentaires
            driver.back()
            time.sleep(2)
        except:
            commentaires.append("Commentaires non disponibles")

        # Ajout des données dans la liste si non déjà existante
        if {"auteur": auteur, "texte": texte, "commentaires": commentaires} not in data:
            data.append({
                "auteur": auteur,
                "texte": texte,
                "commentaires": commentaires
            })

    # Vérifie si on a atteint le bas de la page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Sauvegarde en CSV
df = pd.DataFrame(data)
df.to_csv("posts_facebook_uvbf.csv", index=False, encoding='utf-8')
driver.quit()
print("Données sauvegardées dans posts_facebook_uvbf.csv")
