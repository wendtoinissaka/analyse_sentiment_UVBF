import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs

# Configurer le chemin du WebDriver pour Chrome
os.environ["webdriver.chrome.driver"] = "/usr/lib/chromium-browser/chromedriver"

# Options pour exécuter Chrome en mode headless
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

# Dictionnaire pour stocker les données
UVsdict = {
    "date": [],
    'desc': [],
    'likes': [],
    'comments': [],
    "nb_comments": [],
    'shares': [],
}

# Initialiser le WebDriver
driver = webdriver.Chrome(options=options)

# Charger la page Facebook
driver.get('https://web.facebook.com/uvburkina')
driver.implicitly_wait(10)

# Faire défiler la page pour charger les publications
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  # Attendre que le contenu se charge
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Récupérer le HTML de la page
html = driver.page_source
soup = bs(html, "html.parser")

# Trouver toutes les publications
publications = soup.find_all("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd")

for publication in publications:
    # Récupérer le texte de la publication
    texte_publication = publication.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
    for texte in texte_publication:
        desc = texte.get_text(strip=True)
        UVsdict['desc'].append(desc)

    # Récupérer la date de publication
    date_publication = publication.find("span", class_="x1rg5ohu x6ikm8r x10wlt62 x16dsc37 xt0b8zv")
    if date_publication:
        date = date_publication.get_text(strip=True)
        UVsdict['date'].append(date)

    # Récupérer le nombre de likes
    like_publication = publication.find("div", class_="x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62")
    if like_publication:
        like = like_publication.get_text(strip=True)
        UVsdict['likes'].append(like)

    # Récupérer le nombre de commentaires
    nb_comments_publication = publication.find("span", class_="xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs x1sur9pj xkrqix3")
    if nb_comments_publication:
        comments = nb_comments_publication.get_text(strip=True)
        UVsdict['nb_comments'].append(comments)

    # Récupérer le nombre de partages
    share_publication = publication.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xi81zsa")
    if share_publication:
        share = share_publication.get_text(strip=True)
        UVsdict['shares'].append(share)

    # Récupérer les commentaires
    comments_publications = publication.find_all("div", class_="xmjcpbm x1tlxs6b x1g8br2z x1gn5b1j x230xth x9f619 xzsf02u x1rg5ohu xdj266r x11i5rnm xat24cr x1mh8g0r x193iq5w x1mzt3pk x1n2onr6 xeaf4i8 x13faqbe")
    for comment in comments_publications:
        comment_text = comment.get_text(strip=True)
        UVsdict['comments'].append(comment_text)

# Afficher les données récupérées
print(UVsdict)

# Fermer le navigateur
driver.quit()
