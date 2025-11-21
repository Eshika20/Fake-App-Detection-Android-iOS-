# Fetch app details
from google_play_scraper import app
def fetch_app(package_name):
    # Get app details from the Google Play Store.
    try:
        details = app(package_name,lang='en', country='us')
        return details
    except Exception as e:
        print("App not found or error occurred:", e)
        return None


# Extract the useful app features
def extract_features(app_data):
    return {
        "name": app_data.get("title"),
        "package": app_data.get("appId"),
        "developer": app_data.get("developer"),
        "icon": app_data.get("icon"),
        "description": app_data.get("description")
    }


# Compare names
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")
def text_similarity(a, b):
    emb1 = model.encode(a, convert_to_tensor=True)
    emb2 = model.encode(b, convert_to_tensor=True)
    score = float(util.cos_sim(emb1, emb2))
    return score


# Compare icons
import requests
from PIL import Image
import imagehash
def download_image(url, filename):
    img = requests.get(url).content
    with open(filename, "wb") as f:
        f.write(img)
def compare_icons(url1, url2):
    download_image(url1, "icon1.png")
    download_image(url2, "icon2.png")
    img1 = Image.open("icon1.png")
    img2 = Image.open("icon2.png")
    hash1 = imagehash.average_hash(img1)
    hash2 = imagehash.average_hash(img2)
    return 1 - (hash1 - hash2) / 64



# Generate a score to detect fake apps
def calculate_risk_score(sim_name, sim_icon, same_developer):
    score = 0
    if sim_name > 0.75:
        score += 20
    elif sim_icon > 0.7:
        score += 40
    elif not same_developer:
        score += 30
    return score















