import requests
import os

def handler():
    # Récupération des secrets
    api_key = os.getenv("CLAUDE_KEY", "").strip()
    tg_token = os.getenv("TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("CHAT_ID", "").strip()
    news_key = os.getenv("NEWS_API_KEY", "").strip()

    # 1. NEWS
    news_url = f"https://newsapi.org/v2/top-headlines?category=technology&language=fr&apiKey={news_key}"
    try:
        articles = requests.get(news_url).json().get('articles', [])[:5]
        context = "\n".join([a['title'] for a in articles])
    except:
        context = "Pas de news disponibles."

    # 2. PROMPT
    prompt = f"Tu es une IA d'arbitrage. Analyse ces news et donne une opportunité : {context}. Réponds en français."

    # 3. GEMINI (L'URL la plus stable au monde)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    res = requests.post(url, json=payload)
    
    if res.status_code == 200:
        try:
            texte = res.json()['candidates'][0]['content']['parts'][0]['text']
            msg = f"✅ **ANALYSE RÉUSSIE**\n\n{texte}"
        except:
            msg = f"❌ Erreur structure JSON : {res.text[:200]}"
    else:
        # Ici on affiche TOUTE l'erreur pour comprendre
        msg = f"❌ ERREUR API ({res.status_code})\nMessage : {res.text[:200]}"

    # 4. TELEGRAM
    requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", 
                  data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    handler()
