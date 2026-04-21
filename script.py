import requests
import os

def handler():
    # 1. RÉCUPÉRATION DES SECRETS
    api_key = os.getenv("CLAUDE_KEY", "").strip()
    tg_token = os.getenv("TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("CHAT_ID", "").strip()
    news_key = os.getenv("NEWS_API_KEY", "").strip()

    # 2. NEWS
    news_url = f"https://newsapi.org/v2/top-headlines?category=technology&language=fr&apiKey={news_key}"
    try:
        articles = requests.get(news_url).json().get('articles', [])[:5]
        context = " / ".join([a['title'] for a in articles])
    except:
        context = "Signaux indisponibles"

    # 3. GEMINI - CONFIGURATION ULTIME
    # On utilise gemini-1.5-flash qui est le plus rapide et robuste
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": f"Tu es une IA d'arbitrage. Analyse : {context}"}]}]
    }
    
    res = requests.post(url, json=payload)
    
    # 4. GESTION DES MESSAGES
    if res.status_code == 200:
        try:
            msg = "✅ **SUCCÈS**\n\n" + res.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            msg = f"❌ Erreur structure : {res.text[:100]}"
    else:
        # SI CA ECHOUE ENCORE, ON VA VOIR EXACTEMENT POURQUOI
        msg = f"❌ CODE ERREUR : {res.status_code}\nMESSAGE : {res.text}"

    # 5. ENVOI TELEGRAM
    requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", 
                  data={"chat_id": chat_id, "text": msg})

if __name__ == "__main__":
    handler()
