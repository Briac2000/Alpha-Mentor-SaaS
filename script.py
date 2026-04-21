import requests
import os

# CONFIG (Récupération des Secrets)
API_KEY = os.getenv("CLAUDE_KEY") # Ta clé Gemini (AIza...)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    print("Démarrage du scan...")
    
    # 1. NEWS
    news_url = f"https://newsapi.org/v2/top-headlines?category=business&language=fr&apiKey={NEWS_API_KEY}"
    news_data = requests.get(news_url).json()
    articles = news_data.get('articles', [])[:5]
    context = " ".join([a['title'] for a in articles])
    print(f"News récupérées : {len(articles)}")

    # 2. PROMPT
    prompt = f"Tu es une IA d'arbitrage. Analyse ces news et donne une opportunité business courte : {context}"

    # 3. GEMINI
    print("Appel à Gemini...")
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    res = requests.post(gemini_url, json=payload)
    print(f"Réponse Gemini code : {res.status_code}")
    
    if res.status_code == 200:
        analyse = res.json()['candidates'][0]['content']['parts'][0]['text']
        # On nettoie un peu le texte pour Telegram
        message = f"🚀 ANALYSE ALPHA :\n\n{analyse[:3500]}" 
    else:
        message = f"❌ Erreur API : {res.status_code}"

    # 4. TELEGRAM (Sans Markdown pour éviter les bugs)
    print("Envoi vers Telegram...")
    final_res = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
        data={"chat_id": CHAT_ID, "text": message}
    )
    print(f"Réponse Telegram : {final_res.status_code}")

if __name__ == "__main__":
    handler()
