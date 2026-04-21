import requests
import os

# RÉCUPÉRATION DES CLÉS (Via les Secrets GitHub)
CLAUDE_API_KEY = os.getenv("CLAUDE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    # 1. SCAN DES NEWS (TECH, FINANCE, IMMO)
    url = f"https://newsapi.org/v2/everything?q=(finance OR tech OR immobilier)&language=fr&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])[:15]
    except:
        articles = []
    
    context = "\n".join([f"- {a['title']}: {a['description']}" for a in articles])

    # 2. APPEL AU MENTOR (CLAUDE 3.5 SONNET)
    prompt = f"""Tu es un entrepreneur légendaire avec 50 ans d'expérience. Tu as un flair infaillible pour l'argent.
    Voici les derniers signaux du monde : {context}
    
    TA MISSION : Filtre le bruit inutile. Si tu vois une opportunité de 'bonne affaire' ou un signal de rupture, analyse-le avec ton instinct de vieux loup.
    Si rien n'est digne de ton attention, réponds strictement : 'RIEN'.
    
    FORMAT : 🚀 AFFAIRE / 🧐 ANALYSE / 💰 ACTION."""
    
    headers = {"x-api-key": CLAUDE_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    data = {"model": "claude-3-5-sonnet-20240620", "max_tokens": 800, "messages": [{"role": "user", "content": prompt}]}
    
    res = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data).json()
    analyse = res['content'][0]['text']

    # 3. ENVOI TELEGRAM
    if analyse.strip() != "RIEN":
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": f"🧠 **MUNDIS ALPHA**\n\n{analyse}", "parse_mode": "Markdown"})

if __name__ == "__main__":
    handler()
