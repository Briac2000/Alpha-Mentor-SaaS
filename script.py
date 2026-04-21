import requests
import os

# CONFIG
API_KEY = os.getenv("CLAUDE_KEY") # Ta clé Gemini (AIza...) est ici
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    # 1. SCAN NEWS
    query = "(SaaS OR 'artificial intelligence' OR fintech OR arbitrage)"
    url = f"https://newsapi.org/v2/everything?q={query}&language=fr&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        articles = requests.get(url).json().get('articles', [])[:15]
        context = "\n".join([f"- {a['title']}" for a in articles])
    except:
        context = "Signaux indisponibles."

    # 2. PROMPT IDENTITY
    prompt = f"""IDENTITÉ : Tu es une Intelligence Synthétique de haut niveau pour l'arbitrage d'opportunités globales. 
    Analyse ces signaux et révèle la richesse cachée : {context}
    
    STRUCTURE STRICTE :
    - 📡 **LE SIGNAL** : Tendance brute.
    - 🧬 **L'ANTHÈSE** : Pourquoi les autres échouent.
    - ⚡ **L'OPPORTUNITÉ D'ARBITRAGE** : Solution précise.
    - 🏁 **VITESSE D'EXÉCUTION** : Pas concret < 24h.
    - 📈 **NOTE DE CONVICTION** : 1-10."""

    # 3. APPEL GEMINI (URL MISE À JOUR)
    # Changement ici : v1 au lieu de v1beta et format de l'URL
    gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    res = requests.post(gemini_url, json=payload)
    
    if res.status_code == 200:
        try:
            analyse = res.json()['candidates'][0]['content']['parts'][0]['text']
            final_msg = f"🤖 **UNITÉ SYNTHÉTIQUE ACTIVÉE**\n\n{analyse}"
        except:
            final_msg = "❌ Erreur de lecture de la réponse Google."
    else:
        final_msg = f"❌ Erreur API Google ({res.status_code}) : Vérifie si ta clé API est bien collée dans CLAUDE_KEY."

    # 4. ENVOI TELEGRAM
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    handler()
