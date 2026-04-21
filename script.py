import requests
import os

# CONFIGURATION
API_KEY = os.getenv("CLAUDE_KEY").strip()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    # 1. RÉCUPÉRATION DES NEWS
    news_url = f"https://newsapi.org/v2/everything?q=business+tech&language=fr&apiKey={NEWS_API_KEY}"
    articles = requests.get(news_url).json().get('articles', [])[:10]
    context = "\n".join([a['title'] for a in articles])

    # 2. IDENTITÉ ET PROMPT
    prompt = f"Tu es une IA d'arbitrage. Analyse ces news et donne une opportunité : {context}. Réponds avec : SIGNAL, ANTHÈSE, OPPORTUNITÉ, VITESSE, CONVICTION."

    # 3. APPEL GOOGLE (L'URL LA PLUS STABLE)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    res = requests.post(url, json=payload)
    
    if res.status_code == 200:
        analyse = res.json()['candidates'][0]['content']['parts'][0]['text']
        msg = f"🤖 **UNITÉ SYNTHÉTIQUE**\n\n{analyse}"
    else:
        msg = f"❌ Erreur : {res.json().get('error', {}).get('message', 'Problème de clé')}"

    # 4. TELEGRAM
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    handler()
