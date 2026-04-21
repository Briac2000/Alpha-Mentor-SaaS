import requests
import os

# CONFIG
API_KEY = os.getenv("CLAUDE_KEY") # On utilise le secret existant
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    # 1. SCAN NEWS
    query = "(SaaS OR 'artificial intelligence' OR fintech OR arbitrage)"
    url = f"https://newsapi.org/v2/everything?q={query}&language=fr&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get('articles', [])[:15]
    context = "\n".join([f"- {a['title']}" for a in articles])

    # 2. PROMPT IDENTITY
    prompt = f"""IDENTITÉ : Tu es une Intelligence Synthétique de haut niveau pour l'arbitrage d'opportunités.
    Analyse ces signaux : {context}
    
    STRUCTURE STRICTE :
    - 📡 **LE SIGNAL**
    - 🧬 **L'ANTHÈSE**
    - ⚡ **L'OPPORTUNITÉ D'ARBITRAGE**
    - 🏁 **VITESSE D'EXÉCUTION**
    - 📈 **NOTE DE CONVICTION** (1-10)"""

    # 3. APPEL GEMINI (Google)
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    res = requests.post(gemini_url, json=payload)
    
    if res.status_code == 200:
        analyse = res.json()['candidates'][0]['content']['parts'][0]['text']
        final_msg = f"🤖 **UNITÉ SYNTHÉTIQUE ACTIVÉE**\n\n{analyse}"
    else:
        final_msg = f"❌ Erreur Système : {res.text[:100]}"

    # 4. ENVOI TELEGRAM
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    handler()
