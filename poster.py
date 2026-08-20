import os
import time
import random
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============================================
# ДАННЫЕ ТОКЕНА
# ============================================
TOKEN_DATA = {
    "name": "One•Two•Three",
    "symbols": ["ONE", "TWO", "THREE"],
    "contracts": {
        "ONE": "CGn6yYGTUkctq9PqDdK6ALgfxTS1vTBr9NWBPuoNYmad",
        "TWO": "H5kjSzmxW98iZ2Xvx7e45hxxyDjMYTk6z8aJfeFsj46d",
        "THREE": "uM1kuvsLYauDQZh8g6RrNw3oLAfSAvgEojvJT5hCLNV"
    },
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
# 1. BINANCE SQUARE
# ============================================
class BinanceSquarePoster:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_SQUARE_API_KEY")
        self.stats = {"posted": 0, "failed": 0}
    
    def post(self, text, lang="en"):
        if not self.api_key:
            print("⚠️ BINANCE_SQUARE_API_KEY не найден!")
            return False
        try:
            url = "https://api.binance.com/sapi/v1/square/post"
            headers = {"X-MBX-APIKEY": self.api_key, "Content-Type": "application/json"}
            payload = {"text": text, "topic": "cryptocurrency", "lang": lang, "tags": ["ONE", "TWO", "THREE", "Solana"]}
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Binance Square ({lang})")
                self.stats["posted"] += 1
                return True
            else:
                print(f"⚠️ Binance Square: {response.text}")
                self.stats["failed"] += 1
                return False
        except Exception as e:
            print(f"⚠️ Binance Square: {e}")
            self.stats["failed"] += 1
            return False

# ============================================
# 2. RUDOS.SU
# ============================================
class RudosPoster:
    def __init__(self):
        self.stats = {"posted": 0, "failed": 0}
    
    def _init_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,720')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post(self, text):
        driver = self._init_driver()
        try:
            print("📤 RuDos.su...")
            driver.get("https://rudos.su/add")
            time.sleep(2)
            wait = WebDriverWait(driver, 10)
            title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
            title_field.send_keys("One•Two•Three — экосистема на Solana")
            desc_field = driver.find_element(By.NAME, "description")
            desc_field.send_keys(text)
            publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Опубликовать')]")
            publish_btn.click()
            time.sleep(2)
            print("✅ RuDos.su")
            self.stats["posted"] += 1
            driver.quit()
            return True
        except Exception as e:
            print(f"⚠️ RuDos.su: {e}")
            self.stats["failed"] += 1
            driver.quit()
            return False

# ============================================
# 3. XMRBAZAAR
# ============================================
class XmrBazaarPoster:
    def __init__(self):
        self.stats = {"posted": 0, "failed": 0}
    
    def _init_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,720')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post(self, text):
        driver = self._init_driver()
        try:
            print("📤 XmrBazaar...")
            driver.get("https://xmrbazaar.com/board/create")
            time.sleep(2)
            wait = WebDriverWait(driver, 10)
            title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
            title_field.send_keys("One•Two•Three — Solana Ecosystem")
            desc_field = driver.find_element(By.NAME, "description")
            desc_field.send_keys(text)
            publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
            publish_btn.click()
            time.sleep(2)
            print("✅ XmrBazaar")
            self.stats["posted"] += 1
            driver.quit()
            return True
        except Exception as e:
            print(f"⚠️ XmrBazaar: {e}")
            self.stats["failed"] += 1
            driver.quit()
            return False

# ============================================
# 4. TELEGRAPH
# ============================================
class TelegraphPoster:
    def __init__(self):
        self.stats = {"articles": 0, "failed": 0}
    
    def post(self, title, content):
        try:
            content_html = content.replace('\n', '<br>')
            content_html += f"""
            <br><br>
            🌐 <b>Сайты:</b><br>
            🟢 $ONE: <a href="{TOKEN_DATA['sites']['ONE']}">{TOKEN_DATA['sites']['ONE']}</a><br>
            🟡 €TWO: <a href="{TOKEN_DATA['sites']['TWO']}">{TOKEN_DATA['sites']['TWO']}</a><br>
            🔵 £THREE: <a href="{TOKEN_DATA['sites']['THREE']}">{TOKEN_DATA['sites']['THREE']}</a><br>
            📱 TG: <a href="{TOKEN_DATA['telegram']}">{TOKEN_DATA['telegram']}</a>
            """
            response = requests.post("https://api.telegra.ph/createPage", json={
                "title": title,
                "content": content_html,
                "author_name": "One•Two•Three",
                "author_url": TOKEN_DATA['sites']['ONE']
            }, timeout=10)
            result = response.json()
            if result.get('ok'):
                url = result['result']['url']
                print(f"✅ Telegra.ph: {url}")
                self.stats["articles"] += 1
                return url
            return None
        except Exception as e:
            print(f"⚠️ Telegraph: {e}")
            return None

# ============================================
# 5. YEETIT
# ============================================
class YeetItPoster:
    def __init__(self):
        self.stats = {"posted": 0, "failed": 0}
    
    def post(self):
        try:
            html = f"""
            <html><head><title>One•Two•Three</title></head><body>
            <h1>🚀 One•Two•Three — Solana</h1>
            <b>$ONE</b> {TOKEN_DATA['prices']['ONE']} — <a href="{TOKEN_DATA['sites']['ONE']}">Сайт</a><br>
            <b>€TWO</b> {TOKEN_DATA['prices']['TWO']} — <a href="{TOKEN_DATA['sites']['TWO']}">Сайт</a><br>
            <b>£THREE</b> {TOKEN_DATA['prices']['THREE']} — <a href="{TOKEN_DATA['sites']['THREE']}">Сайт</a><br>
            📱 TG: <a href="{TOKEN_DATA['telegram']}">@onetwothree</a>
            </body></html>
            """
            response = requests.post("https://yeetit.site/v1/publish", json={"html": html}, timeout=10)
            if response.status_code == 200:
                print(f"✅ YeetIt: {response.json().get('url')}")
                self.stats["posted"] += 1
                return True
            self.stats["failed"] += 1
            return False
        except Exception as e:
            print(f"⚠️ YeetIt: {e}")
            self.stats["failed"] += 1
            return False

# ============================================
# 6. CURB.SALE
# ============================================
class CurbSalePoster:
    def __init__(self):
        self.stats = {"posted": 0, "failed": 0}
    
    def post(self):
        try:
            response = requests.post("https://api.curb.sale/listings", json={
                "title": "One•Two•Three — Solana Ecosystem",
                "price": "0.01",
                "description": f"Three tokens: $ONE {TOKEN_DATA['prices']['ONE']}, €TWO {TOKEN_DATA['prices']['TWO']}, £THREE {TOKEN_DATA['prices']['THREE']}",
                "currency": "USD"
            }, timeout=10)
            if response.status_code in [200, 201]:
                print("✅ Curb.Sale")
                self.stats["posted"] += 1
                return True
            self.stats["failed"] += 1
            return False
        except Exception as e:
            print(f"⚠️ Curb.Sale: {e}")
            self.stats["failed"] += 1
            return False

# ============================================
# ОСНОВНОЙ БОТ
# ============================================
def post_to_telegram(text):
    bot_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT")
    if bot_token and chat_id:
        try:
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", 
                         json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=10)
        except:
            pass

def main():
    print("🚀 One•Two•Three Расклейщик запущен!")
    print("🌐 Площадки: Binance Square + RuDos.su + XmrBazaar + Telegraph + YeetIt + Curb.Sale")
    print("=" * 50)
    
    # 1. Telegraph
    print("\n📝 Telegraph...")
    telegraph = TelegraphPoster()
    url = telegraph.post("One•Two•Three на Solana", 
        f"""One•Two•Three ($ONE, €TWO, £THREE) — экосистема на Solana.

Три токена: $ONE {TOKEN_DATA['prices']['ONE']}, €TWO {TOKEN_DATA['prices']['TWO']}, £THREE {TOKEN_DATA['prices']['THREE']}

Сайты:
{TOKEN_DATA['sites']['ONE']}
{TOKEN_DATA['sites']['TWO']}
{TOKEN_DATA['sites']['THREE']}

TG: @onetwothree""")
    if url:
        post_to_telegram(f"📝 Статья: {url}")
    
    # 2. Binance Square
    print("\n📢 Binance Square...")
    binance = BinanceSquarePoster()
    text = f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — экосистема на Solana!

$ONE {TOKEN_DATA['prices']['ONE']}: {TOKEN_DATA['sites']['ONE']}
€TWO {TOKEN_DATA['prices']['TWO']}: {TOKEN_DATA['sites']['TWO']}
£THREE {TOKEN_DATA['prices']['THREE']}: {TOKEN_DATA['sites']['THREE']}

⚡ Solana, TG: @onetwothree #ONE #TWO #THREE #Solana"""
    binance.post(text, "en")
    binance.post(text, "zh")
    
    # 3. RuDos.su
    print("\n📢 RuDos.su...")
    rudos = RudosPoster()
    rudos.post(f"""One•Two•Three ($ONE, €TWO, £THREE) — экосистема на Solana.

$ONE {TOKEN_DATA['prices']['ONE']}: {TOKEN_DATA['sites']['ONE']}
€TWO {TOKEN_DATA['prices']['TWO']}: {TOKEN_DATA['sites']['TWO']}
£THREE {TOKEN_DATA['prices']['THREE']}: {TOKEN_DATA['sites']['THREE']}

TG: @onetwothree""")
    
    # 4. XmrBazaar
    print("\n📢 XmrBazaar...")
    xmr = XmrBazaarPoster()
    xmr.post(f"""One•Two•Three ($ONE, €TWO, £THREE) — Solana ecosystem.

$ONE {TOKEN_DATA['prices']['ONE']}: {TOKEN_DATA['sites']['ONE']}
€TWO {TOKEN_DATA['prices']['TWO']}: {TOKEN_DATA['sites']['TWO']}
£THREE {TOKEN_DATA['prices']['THREE']}: {TOKEN_DATA['sites']['THREE']}

TG: @onetwothree""")
    
    # 5. YeetIt
    print("\n📢 YeetIt...")
    yeetit = YeetItPoster()
    yeetit.post()
    
    # 6. Curb.Sale
    print("\n📢 Curb.Sale...")
    curb = CurbSalePoster()
    curb.post()
    
    # Отчет
    total = binance.stats['posted'] + rudos.stats['posted'] + xmr.stats['posted'] + yeetit.stats['posted'] + curb.stats['posted']
    post_to_telegram(f"✅ **Готово! Постов: {total}**")
    print(f"\n✅ Готово! Постов: {total}")

if __name__ == "__main__":
    main()
