import requests
import os

# CONFIG
API_KEY = os.getenv("CLAUDE_KEY") # Ta clé Google AI Studio (AIza...)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    # 1. NEWS SIMPLES
    news_url = f"https://newsapi.org/v2/top-headlines?country=fr&category=business&apiKey={NEWS_API_KEY}"
    articles = requests.get(news_url).json().get('articles', [])[:5]
    context = " / ".join([a['title'] for a in articles])

    # 2. PROMPT
    prompt = f"Tu es une IA d'arbitrage. Analyse ces news : {context}. Donne une opportunité business."

    # 3. APPEL GEMINI (URL LA PLUS STABLE)
    # Note : Utilisation de v1/models/gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    res = requests.post(url, headers=headers, json=payload)
    
    if res.status_code == 200:
        analyse = res.json()['candidates'][0]['content']['parts'][0]['text']
        message = f"✅ ANALYSE RÉUSSIE :\n\n{analyse}"
    else:
        # Si ça met encore 404, c'est la clé API qui est en cause
        message = f"❌ Erreur {res.status_code} : Vérifie que ton secret CLAUDE_KEY contient bien la clé AIza..."

    # 4. ENVOI TELEGRAM
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": message})

if __name__ == "__main__":
    handler()
