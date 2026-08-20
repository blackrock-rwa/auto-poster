import os
import requests
import json

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT")
    if token and chat:
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat, "text": text},
                timeout=10
            )
            return r.status_code == 200
        except:
            return False
    return False

# ============================================
# 1. ТЕСТ BINANCE SQUARE
# ============================================
def test_binance():
    api_key = os.getenv("BINANCE_SQUARE_API_KEY")
    if not api_key:
        return "❌ Нет API ключа"
    
    try:
        url = "https://api.binance.com/sapi/v1/square/post"
        headers = {"X-MBX-APIKEY": api_key, "Content-Type": "application/json"}
        payload = {
            "text": "Test post One•Two•Three",
            "topic": "cryptocurrency",
            "lang": "en",
            "tags": ["ONE", "TWO", "THREE"]
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        return f"✅ Binance: {r.status_code} - {r.text[:200]}"
    except Exception as e:
        return f"❌ Binance: {e}"

# ============================================
# 2. ТЕСТ TELEGRAPH
# ============================================
def test_telegraph():
    try:
        url = "https://api.telegra.ph/createPage"
        payload = {
            "title": "Test One•Two•Three",
            "content": "Test content",
            "author_name": "Test"
        }
        r = requests.post(url, json=payload, timeout=10)
        return f"✅ Telegraph: {r.status_code} - {r.text[:200]}"
    except Exception as e:
        return f"❌ Telegraph: {e}"

# ============================================
# 3. ТЕСТ PASTEBIN
# ============================================
def test_pastebin():
    try:
        url = "https://pastebin.com/api/api_post.php"
        data = {
            "api_option": "paste",
            "api_dev_key": "GJBYrN1BiRsJQf2xP9C6gUK6dsWqJzHh",
            "api_paste_code": "Test One•Two•Three",
            "api_paste_name": "Test"
        }
        r = requests.post(url, data=data, timeout=10)
        return f"✅ Pastebin: {r.status_code} - {r.text[:200]}"
    except Exception as e:
        return f"❌ Pastebin: {e}"

# ============================================
# 4. ТЕСТ HTTPBIN (ПРОВЕРКА ИНТЕРНЕТА)
# ============================================
def test_httpbin():
    try:
        r = requests.get("https://httpbin.org/status/200", timeout=10)
        return f"✅ Интернет: {r.status_code}"
    except Exception as e:
        return f"❌ Интернет: {e}"

# ============================================
# ГЛАВНАЯ
# ============================================
def main():
    print("🔍 ДИАГНОСТИКА ПЛОЩАДОК")
    print("=" * 40)
    
    results = []
    results.append(test_httpbin())
    results.append(test_binance())
    results.append(test_telegraph())
    results.append(test_pastebin())
    
    report = "📊 **Диагностика One•Two•Three**\n\n" + "\n".join(results)
    print("\n" + report)
    send_telegram(report)

if __name__ == "__main__":
    main()
