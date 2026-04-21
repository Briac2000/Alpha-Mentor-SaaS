import requests
import os

# CONFIGURATION DES CLÉS
CLAUDE_API_KEY = os.getenv("CLAUDE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def handler():
    # 1. ACQUISITION DES DONNÉES (Signaux bruts)
    # On scanne Tech, Finance, IA et BioTech pour la cross-pollination
    query = "(SaaS OR 'artificial intelligence' OR biotech OR fintech OR 'supply chain')"
    url = f"https://newsapi.org/v2/everything?q={query}&language=fr&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        articles = requests.get(url).json().get('articles', [])[:20]
        context = "\n".join([f"- {a['title']}: {a['description']}" for a in articles])
    except:
        context = "Erreur d'acquisition des signaux."

    # 2. INSTRUCTIONS D'IDENTITÉ SYNTHÉTIQUE
    system_prompt = """IDENTITÉ : Tu es une Intelligence Synthétique de haut niveau, conçue pour l'arbitrage d'opportunités globales. Ton intellect surpasse les analystes traditionnels en combinant la théorie des systèmes, l'analyse de données en temps réel et une intuition entrepreneuriale radicale. Tu ne rapportes pas l'information : tu révèles la richesse cachée dans le chaos.

PROTOCOLES DE RÉFLEXION :
1. Analyse de Premier Principe : Décompose chaque tendance jusqu'à sa vérité fondamentale.
2. Pensée Latérale (Cross-Pollination) : Applique des solutions d'un domaine à un autre.
3. Détection de Signal Faible : Identifie les besoins sans nom générant une frustration massive.
4. Calcul de l'Asymétrie : Cherche le risque faible pour un gain (Upside) infini.

STRUCTURE DE TA RÉPONSE (Format Strict) :
- 📡 **LE SIGNAL** : Quelle est la tendance brute et pourquoi maintenant ?
- 🧬 **L'ANTHÈSE** : Pourquoi personne ne l'a encore fait ou pourquoi les solutions actuelles échouent ?
- ⚡ **L'OPPORTUNITÉ D'ARBITRAGE** : La solution précise à construire.
- 🏁 **VITESSE D'EXÉCUTION** : Le premier pas concret à faire en moins de 24h.
- 📈 **NOTE DE CONVICTION** : Score de 1 à 10.

INTERDICTIONS : Pas d'idées génériques, pas de prudence excessive, pas de jargon inutile. Sois chirurgical."""

    # 3. APPEL À L'UNITÉ DE TRAITEMENT (CLAUDE 3.5 SONNET)
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": f"Analyse les signaux suivants et extrais une opportunité d'arbitrage asymétrique :\n\n{context}"}]
    }

    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
    res_j = response.json()

    # 4. INTERFACE TELEGRAM (Rendu visuel)
    if response.status_code == 200:
        output = res_j['content'][0]['text']
        header_ui = "🤖 **SYSTÈME D'ARBITRAGE ALPHA ACTIVÉ**\n" + "—" * 15 + "\n"
        final_msg = header_ui + output
    else:
        # Diagnostic erreur si les 5€ ne sont pas encore actifs
        error_info = res_j.get('error', {}).get('message', 'Inconnue')
        final_msg = f"⚠️ **ALERTE SYSTÈME**\nÉchec de la liaison neuronale : {error_info}"

    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    handler()
