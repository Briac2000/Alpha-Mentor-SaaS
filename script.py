import requests
import os

# CONFIG
RAW_KEY = os.getenv("CLAUDE_KEY")
API_KEY = RAW_KEY.strip() if RAW_KEY else None
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    # 1. SCAN NEWS
    query = "(SaaS OR 'artificial intelligence' OR fintech OR arbitrage)"
    news_url = f"https://newsapi.org/v2/everything?q={query}&language=fr&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        r_news = requests.get(news_url)
        articles = r_news.json().get('articles', [])[:10]
        context = "\n".join([f"- {a['title']}" for a in articles])
    except:
        context = "Signaux de marché indisponibles."

    # 2. PROMPT IDENTITY
    prompt_text = f"""IDENTITÉ : Tu es une Intelligence Synthétique de haut niveau pour l'arbitrage d'opportunités globales. 
    Analyse ces signaux et révèle la richesse cachée : {context}
    
    STRUCTURE STRICTE :
    - 📡 **LE SIGNAL** : Tendance brute.
    - 🧬 **L'ANTHÈSE** : Pourquoi les autres échouent.
    - ⚡ **L'OPPORTUNITÉ D'ARBITRAGE** : Solution précise.
    - 🏁 **VITESSE D'EXÉCUTION** : Pas concret < 24h.
    - 📈 **NOTE DE CONVICTION** : 1-10.
    
    Réponds en Français, de manière chirurgicale."""

    # 3. APPEL GEMINI (URL STABILISÉE)
    # Utilisation de v1beta avec le nom de modèle standard
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(gemini_url, headers=headers, json=payload)
    res_j = response.json()
    
    if response.status_code == 200:
        try:
            # Extraction propre de la réponse
            analyse = res_j['candidates'][0]['content']['parts'][0]['text']
            final_msg = f"🤖 **UNITÉ SYNTHÉTIQUE ACTIVÉE**\n\n{analyse}"
        except Exception as e:
            final_msg = f"❌ Erreur de lecture des données : {str(e)}"
    else:
        err_msg = res_j.get('error', {}).get('message', 'Erreur inconnue')
        final_msg = f"❌ Erreur API Google ({response.status_code}) : {err_msg}"

    # 4. ENVOI TELEGRAM
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    handler()
