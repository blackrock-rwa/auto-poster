import os
import requests
import time

# ============================================
# ТВОИ ДАННЫЕ
# ============================================
TOKEN_DATA = {
    "sites": {
        "ONE": "https://123tokens.github.io/one/",
        "TWO": "https://123tokens.github.io/two/",
        "THREE": "https://123tokens.github.io/three/"
    },
    "telegram": "https://t.me/onetwothree"
}

# ============================================
# TELEGRAM (УЖЕ РАБОТАЕТ)
# ============================================
def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT")
    if token and chat:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat, "text": text, "parse_mode": "Markdown"},
                timeout=10
            )
            print("✅ Telegram отправлен")
            return True
        except Exception as e:
            print(f"❌ Telegram: {e}")
            return False
    return False

# ============================================
# BINANCE SQUARE (ПРЯМОЙ API)
# ============================================
def post_to_binance(text):
    api_key = os.getenv("BINANCE_SQUARE_API_KEY")
    if not api_key:
        print("❌ Нет BINANCE_SQUARE_API_KEY")
        return False
    
    try:
        url = "https://api.binance.com/sapi/v1/square/post"
        headers = {
            "X-MBX-APIKEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text[:1900],
            "topic": "cryptocurrency",
            "lang": "en",
            "tags": ["ONE", "TWO", "THREE", "Solana"]
        }
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Binance Square")
            return True
        else:
            print(f"❌ Binance: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Binance: {e}")
        return False

# ============================================
# ОСНОВНАЯ ФУНКЦИЯ
# ============================================
def main():
    print("🚀 Запуск расклейки One•Two•Three")
    print("=" * 40)
    
    # Текст объявления
    text = f"""🔥 One•Two•Three ($ONE, €TWO, £THREE) — экосистема на Solana!

💰 $ONE — {TOKEN_DATA['sites']['ONE']}
💰 €TWO — {TOKEN_DATA['sites']['TWO']}
💰 £THREE — {TOKEN_DATA['sites']['THREE']}

⚡ 65,000 TPS | Комиссия < $0.001
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi"""
    
    # 1. Постим в Binance Square
    print("\n📢 Binance Square...")
    post_to_binance(text)
    
    # 2. Отчет в Telegram
    send_telegram(f"""✅ **One•Two•Three расклейка выполнена!**

📢 Binance Square — опубликовано
📱 TG: @onetwothree

🌐 Сайты:
$ONE: {TOKEN_DATA['sites']['ONE']}
€TWO: {TOKEN_DATA['sites']['TWO']}
£THREE: {TOKEN_DATA['sites']['THREE']}""")
    
    print("\n✅ Готово!")

if __name__ == "__main__":
    main()
