import os
import requests
import time

# ============================================
# ДАННЫЕ ТОКЕНА
# ============================================
TOKEN_DATA = {
    "sites": {
        "ONE": "https://123tokens.github.io/one/",
        "TWO": "https://123tokens.github.io/two/",
        "THREE": "https://123tokens.github.io/three/"
    },
    "telegram": "https://t.me/onetwothree",
    "prices": {"ONE": "$0.01", "TWO": "€0.05", "THREE": "£0.10"}
}

# ============================================
# TELEGRAM
# ============================================
def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT")
    if token and chat:
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat, "text": text, "parse_mode": "Markdown"},
                timeout=10
            )
            return r.status_code == 200
        except:
            return False
    return False

def get_text(lang="ru"):
    if lang == "en":
        return f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — Solana ecosystem!

💰 Prices: $ONE {TOKEN_DATA['prices']['ONE']}, €TWO {TOKEN_DATA['prices']['TWO']}, £THREE {TOKEN_DATA['prices']['THREE']}

🌐 Sites:
$ONE: {TOKEN_DATA['sites']['ONE']}
€TWO: {TOKEN_DATA['sites']['TWO']}
£THREE: {TOKEN_DATA['sites']['THREE']}

⚡ Solana: 65,000 TPS, fee < $0.001
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi"""
    else:
        return f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — экосистема на Solana!

💰 Цены: $ONE {TOKEN_DATA['prices']['ONE']}, €TWO {TOKEN_DATA['prices']['TWO']}, £THREE {TOKEN_DATA['prices']['THREE']}

🌐 Сайты:
$ONE: {TOKEN_DATA['sites']['ONE']}
€TWO: {TOKEN_DATA['sites']['TWO']}
£THREE: {TOKEN_DATA['sites']['THREE']}

⚡ Solana: 65,000 TPS, комиссия < $0.001
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi"""

# ============================================
# BINANCE SQUARE (через прокси)
# ============================================
def post_binance():
    api_key = os.getenv("BINANCE_SQUARE_API_KEY")
    if not api_key:
        print("❌ Binance: нет ключа")
        return False
    
    try:
        # Прокси для обхода гео-блокировки
        proxies = {
            "http": "http://194.67.213.197:8080",  # Бесплатный прокси (может умереть)
            "https": "http://194.67.213.197:8080"
        }
        
        url = "https://api.binance.com/sapi/v1/square/post"
        headers = {"X-MBX-APIKEY": api_key, "Content-Type": "application/json"}
        payload = {
            "text": get_text("en")[:1900],
            "topic": "cryptocurrency",
            "lang": "en",
            "tags": ["ONE", "TWO", "THREE", "Solana"]
        }
        r = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=10)
        
        if r.status_code == 200:
            print("✅ Binance Square")
            return True
        else:
            print(f"❌ Binance: {r.status_code} - {r.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Binance: {e}")
        return False

# ============================================
# TELEGRAPH (с токеном)
# ============================================
def post_telegraph():
    token = os.getenv("TELEGRAPH_TOKEN")
    if not token:
        # Получаем токен, если его нет
        try:
            r = requests.post("https://api.telegra.ph/createAccount", json={
                "short_name": "OneTwoThree",
                "author_name": "One•Two•Three"
            }, timeout=10)
            if r.json().get('ok'):
                token = r.json()['result']['access_token']
                print(f"✅ Получен новый токен Telegraph")
                # Сохранить токен в переменную (но в GitHub Secrets не запишется)
        except:
            print("❌ Не удалось получить токен Telegraph")
            return False
    
    if not token:
        return False
    
    try:
        content = get_text("ru").replace('\n', '<br>')
        content += f"""
        <br><br>
        🌐 <b>Сайты:</b><br>
        🟢 $ONE: <a href="{TOKEN_DATA['sites']['ONE']}">{TOKEN_DATA['sites']['ONE']}</a><br>
        🟡 €TWO: <a href="{TOKEN_DATA['sites']['TWO']}">{TOKEN_DATA['sites']['TWO']}</a><br>
        🔵 £THREE: <a href="{TOKEN_DATA['sites']['THREE']}">{TOKEN_DATA['sites']['THREE']}</a>
        """
        
        r = requests.post("https://api.telegra.ph/createPage", json={
            "access_token": token,
            "title": "One•Two•Three на Solana",
            "content": content,
            "author_name": "One•Two•Three",
            "author_url": TOKEN_DATA['sites']['ONE']
        }, timeout=10)
        
        data = r.json()
        if data.get('ok'):
            print(f"✅ Telegraph: {data['result']['url']}")
            return data['result']['url']
        else:
            print(f"❌ Telegraph: {data}")
            return False
    except Exception as e:
        print(f"❌ Telegraph: {e}")
        return False

# ============================================
# PASTEBIN (с API ключом)
# ============================================
def post_pastebin():
    api_key = os.getenv("PASTEBIN_KEY")
    if not api_key:
        print("❌ Pastebin: нет API ключа")
        return False
    
    try:
        url = "https://pastebin.com/api/api_post.php"
        data = {
            "api_option": "paste",
            "api_dev_key": api_key,
            "api_paste_code": get_text("ru"),
            "api_paste_name": "One•Two•Three на Solana",
            "api_paste_format": "text",
            "api_paste_expire_date": "1D"
        }
        r = requests.post(url, data=data, timeout=10)
        
        if r.status_code == 200 and r.text.startswith("https://pastebin.com/"):
            print(f"✅ Pastebin: {r.text}")
            return r.text
        else:
            print(f"❌ Pastebin: {r.status_code} - {r.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Pastebin: {e}")
        return False

# ============================================
# ОСНОВНАЯ ФУНКЦИЯ
# ============================================
def main():
    print("🚀 One•Two•Three Расклейщик")
    print("=" * 40)
    
    results = []
    
    # 1. Binance Square
    print("\n📢 Binance Square...")
    results.append(f"Binance Square: {'✅' if post_binance() else '❌'}")
    
    # 2. Telegraph
    print("\n📢 Telegraph...")
    url = post_telegraph()
    results.append(f"Telegraph: {'✅ ' + url if url else '❌'}")
    
    # 3. Pastebin
    print("\n📢 Pastebin...")
    url = post_pastebin()
    results.append(f"Pastebin: {'✅ ' + url if url else '❌'}")
    
    # Отчет
    report = "📊 **Отчет One•Two•Three**\n\n" + "\n".join(results)
    send_telegram(report)
    print("\n" + report)

if __name__ == "__main__":
    main()
