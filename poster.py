import os
import requests
import time
import json

# ============================================
# 1. ДАННЫЕ ТОКЕНА
# ============================================
TOKEN_DATA = {
    "name": "One•Two•Three",
    "symbols": ["ONE", "TWO", "THREE"],
    "sites": {
        "ONE": "https://123tokens.github.io/one/",
        "TWO": "https://123tokens.github.io/two/",
        "THREE": "https://123tokens.github.io/three/"
    },
    "telegram": "https://t.me/onetwothree",
    "prices": {
        "ONE": "$0.01",
        "TWO": "€0.05",
        "THREE": "£0.10"
    }
}

# ============================================
# 2. УТИЛИТЫ
# ============================================
def send_telegram(text):
    """Отправляет сообщение в Telegram"""
    token = os.getenv("TELEGRAM_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT")
    if not token or not chat:
        print("❌ Telegram: не настроен")
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat, "text": text, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram: отправлено")
            return True
        else:
            print(f"❌ Telegram: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram: {e}")
        return False

def get_text(lang="ru"):
    """Генерирует текст поста"""
    if lang == "en":
        return f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — Solana ecosystem!

💰 Prices:
$ONE: {TOKEN_DATA['prices']['ONE']}
€TWO: {TOKEN_DATA['prices']['TWO']}
£THREE: {TOKEN_DATA['prices']['THREE']}

🌐 Websites:
$ONE: {TOKEN_DATA['sites']['ONE']}
€TWO: {TOKEN_DATA['sites']['TWO']}
£THREE: {TOKEN_DATA['sites']['THREE']}

⚡ 65,000 TPS | Fee < $0.001
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments"""
    else:
        return f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — экосистема на Solana!

💰 Цены:
$ONE: {TOKEN_DATA['prices']['ONE']}
€TWO: {TOKEN_DATA['prices']['TWO']}
£THREE: {TOKEN_DATA['prices']['THREE']}

🌐 Сайты:
$ONE: {TOKEN_DATA['sites']['ONE']}
€TWO: {TOKEN_DATA['sites']['TWO']}
£THREE: {TOKEN_DATA['sites']['THREE']}

⚡ 65,000 TPS | Комиссия < $0.001
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments"""

# ============================================
# 3. BINANCE SQUARE
# ============================================
def post_binance():
    """Публикация поста на Binance Square"""
    api_key = os.getenv("BINANCE_SQUARE_API_KEY")
    if not api_key:
        print("❌ Binance Square: API ключ не найден")
        return False
    
    text = get_text("en")[:1900]  # Ограничение 1900 символов
    
    try:
        url = "https://api.binance.com/sapi/v1/square/post"
        headers = {
            "X-MBX-APIKEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "topic": "cryptocurrency",
            "lang": "en",
            "tags": ["ONE", "TWO", "THREE", "Solana", "DeFi", "MicroPayments"]
        }
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            print("✅ Binance Square: опубликовано")
            return True
        else:
            print(f"❌ Binance Square: {response.status_code} - {response.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Binance Square: {e}")
        return False

# ============================================
# 4. TELEGRAPH
# ============================================
def post_telegraph():
    """Публикация статьи на Telegra.ph"""
    title = "One•Two•Three — революция на Solana"
    content = get_text("ru")
    content_html = content.replace('\n', '<br>')
    
    # Добавляем ссылки
    content_html += f"""
    <br><br>
    🌐 <b>Официальные сайты токенов:</b><br>
    🟢 $ONE: <a href="{TOKEN_DATA['sites']['ONE']}">{TOKEN_DATA['sites']['ONE']}</a><br>
    🟡 €TWO: <a href="{TOKEN_DATA['sites']['TWO']}">{TOKEN_DATA['sites']['TWO']}</a><br>
    🔵 £THREE: <a href="{TOKEN_DATA['sites']['THREE']}">{TOKEN_DATA['sites']['THREE']}</a><br>
    📱 Telegram: <a href="{TOKEN_DATA['telegram']}">@onetwothree</a>
    """
    
    try:
        url = "https://api.telegra.ph/createPage"
        payload = {
            "title": title,
            "content": content_html,
            "author_name": "One•Two•Three",
            "author_url": TOKEN_DATA['sites']['ONE']
        }
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        
        if data.get('ok'):
            article_url = data['result']['url']
            print(f"✅ Telegraph: {article_url}")
            return article_url
        else:
            print(f"❌ Telegraph: {data}")
            return None
    except Exception as e:
        print(f"❌ Telegraph: {e}")
        return None

# ============================================
# 5. PASTEBIN.COM (НОВАЯ ПЛОЩАДКА)
# ============================================
def post_pastebin():
    """Создание публичной заметки на Pastebin.com"""
    text = get_text("ru")
    text += f"\n\n🌐 Сайты:\n{TOKEN_DATA['sites']['ONE']}\n{TOKEN_DATA['sites']['TWO']}\n{TOKEN_DATA['sites']['THREE']}"
    
    try:
        url = "https://pastebin.com/api/api_post.php"
        data = {
            "api_option": "paste",
            "api_dev_key": "GJBYrN1BiRsJQf2xP9C6gUK6dsWqJzHh",  # Публичный ключ для демо (можно использовать без регистрации)
            "api_paste_code": text,
            "api_paste_name": "One•Two•Three на Solana",
            "api_paste_format": "text",
            "api_paste_expire_date": "1D"  # 1 день
        }
        response = requests.post(url, data=data, timeout=15)
        
        if response.status_code == 200 and response.text.startswith("https://pastebin.com/"):
            print(f"✅ Pastebin: {response.text}")
            return response.text
        else:
            print(f"❌ Pastebin: {response.text[:100]}")
            return None
    except Exception as e:
        print(f"❌ Pastebin: {e}")
        return None

# ============================================
# 6. ОСНОВНАЯ ФУНКЦИЯ
# ============================================
def main():
    print("🚀 One•Two•Three Расклейщик запущен!")
    print("=" * 50)
    print("📋 План публикации:")
    print("1. Telegram (уведомления)")
    print("2. Binance Square (пост)")
    print("3. Telegraph (статья)")
    print("4. Pastebin (заметка)")
    print("=" * 50)
    
    results = {}
    links = []
    
    # 1. Публикация в Binance Square
    print("\n📢 Binance Square...")
    results['binance'] = post_binance()
    
    # 2. Публикация в Telegraph
    print("\n📢 Telegraph...")
    telegraph_url = post_telegraph()
    results['telegraph'] = bool(telegraph_url)
    if telegraph_url:
        links.append(f"📝 Telegraph: {telegraph_url}")
    
    # 3. Публикация в Pastebin
    print("\n📢 Pastebin...")
    pastebin_url = post_pastebin()
    results['pastebin'] = bool(pastebin_url)
    if pastebin_url:
        links.append(f"📋 Pastebin: {pastebin_url}")
    
    # 4. Отправка финального отчета в Telegram
    report = "📊 **Отчет расклейки One•Two•Three**\n\n"
    report += f"✅ Binance Square: {'✅ Опубликовано' if results['binance'] else '❌ Ошибка'}\n"
    report += f"✅ Telegraph: {'✅ Опубликовано' if results['telegraph'] else '❌ Ошибка'}\n"
    report += f"✅ Pastebin: {'✅ Опубликовано' if results['pastebin'] else '❌ Ошибка'}\n"
    
    if links:
        report += "\n🔗 **Ссылки:**\n" + "\n".join(links)
    
    print("\n" + report)
    send_telegram(report)

if __name__ == "__main__":
    main()
