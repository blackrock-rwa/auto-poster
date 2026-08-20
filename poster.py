import os
import time
import random
import json
import requests
import hashlib
from openai import OpenAI
import google.generativeai as genai
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
# 1. BINANCE SQUARE (УЖЕ РАБОТАЕТ)
# ============================================
class BinanceSquarePoster:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_SQUARE_API_KEY")
        self.stats = {"posted": 0, "failed": 0, "platforms": {}}
        self.load_stats()
    
    def load_stats(self):
        try:
            with open("stats.json", "r") as f:
                self.stats = json.load(f)
        except:
            pass
    
    def save_stats(self):
        with open("stats.json", "w") as f:
            json.dump(self.stats, f, indent=2)
    
    def generate_post(self, lang="en"):
        en_posts = [
            f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — экосистема на Solana!

Три токена. Три уровня. Один кошелёк.

· $ONE — микро-вход — {TOKEN_DATA['prices']['ONE']}
  🔗 {TOKEN_DATA['sites']['ONE']}
· €TWO — средний чек — {TOKEN_DATA['prices']['TWO']}
  🔗 {TOKEN_DATA['sites']['TWO']}
· £THREE — крупные платежи — {TOKEN_DATA['prices']['THREE']}
  🔗 {TOKEN_DATA['sites']['THREE']}

⚡ Solana: мгновенные транзакции, комиссия < $0.001

📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments""",
            f"""💎 One•Two•Three — умная платежная система на Solana!

· $ONE ({TOKEN_DATA['prices']['ONE']}) — микро-платежи
  {TOKEN_DATA['sites']['ONE']}
· €TWO ({TOKEN_DATA['prices']['TWO']}) — ежедневные траты
  {TOKEN_DATA['sites']['TWO']}
· £THREE ({TOKEN_DATA['prices']['THREE']}) — крупные платежи
  {TOKEN_DATA['sites']['THREE']}

⚡ 65,000 TPS | Комиссия < $0.001
🔒 Аудит | LP заблокирована 365 дней

📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Payments #Crypto #Web3"""
        ]
        zh_posts = [
            f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — Solana 上的金融科技生态系统！

三种代币。三个层级。一个钱包。

· $ONE — 微支付 — {TOKEN_DATA['prices']['ONE']}
  🔗 {TOKEN_DATA['sites']['ONE']}
· €TWO — 日常消费 — {TOKEN_DATA['prices']['TWO']}
  🔗 {TOKEN_DATA['sites']['TWO']}
· £THREE — 大额支付 — {TOKEN_DATA['prices']['THREE']}
  🔗 {TOKEN_DATA['sites']['THREE']}

⚡ Solana: 即时交易, 手续费 < $0.001

📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #加密货币 #DeFi #微支付""",
            f"""💎 One•Two•Three — Solana 上最智能的支付系统！

· $ONE ({TOKEN_DATA['prices']['ONE']}) — 微支付
  {TOKEN_DATA['sites']['ONE']}
· €TWO ({TOKEN_DATA['prices']['TWO']}) — 日常消费
  {TOKEN_DATA['sites']['TWO']}
· £THREE ({TOKEN_DATA['prices']['THREE']}) — 大额支付
  {TOKEN_DATA['sites']['THREE']}

⚡ 65,000 TPS | 手续费 < $0.001
🔒 已审计 | LP锁定365天

📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #支付 #加密货币 #Web3"""
        ]
        if lang == "en":
            return random.choice(en_posts)
        else:
            return random.choice(zh_posts)
    
    def post_to_binance_square(self, text, lang="en"):
        if not self.api_key:
            print("⚠️ BINANCE_SQUARE_API_KEY не найден!")
            return False
        try:
            url = "https://api.binance.com/sapi/v1/square/post"
            headers = {"X-MBX-APIKEY": self.api_key, "Content-Type": "application/json"}
            payload = {"text": text, "topic": "cryptocurrency", "lang": lang, "tags": ["ONE", "TWO", "THREE", "Solana", "DeFi"]}
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                print(f"✅ Binance Square ({lang}) — опубликовано!")
                self.stats["posted"] += 1
                self.stats["platforms"][f"binance_{lang}"] = self.stats["platforms"].get(f"binance_{lang}", 0) + 1
                return True
            else:
                print(f"⚠️ Ошибка Binance Square: {response.text}")
                self.stats["failed"] += 1
                return False
        except Exception as e:
            print(f"⚠️ Ошибка Binance Square: {e}")
            self.stats["failed"] += 1
            return False
    
    def run(self, posts_per_lang=3):
        print("📢 Постим в Binance Square...")
        for i in range(posts_per_lang):
            self.post_to_binance_square(self.generate_post("en"), "en")
            time.sleep(300)
            self.post_to_binance_square(self.generate_post("zh"), "zh")
            if i < posts_per_lang - 1:
                wait_time = random.randint(3600, 7200)
                print(f"  💤 Ждем {wait_time//3600} часов...")
                time.sleep(wait_time)
        self.save_stats()

# ============================================
# 2. TELEGRAPH (СТАТЬИ)
# ============================================
class TelegraphPoster:
    def __init__(self):
        self.stats = {"articles": 0, "failed": 0}
    
    def post_to_telegraph(self, title, content):
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
            }, timeout=30)
            result = response.json()
            if result.get('ok'):
                url = result['result']['url']
                print(f"✅ Telegra.ph: {url}")
                self.stats["articles"] += 1
                return url
            return None
        except Exception as e:
            print(f"⚠️ Ошибка Telegraph: {e}")
            return None

# ============================================
# 3. TELEGRAM ADS BOT (СВОЯ ДОСКА В ТЕЛЕГРАМ)
# ============================================
class TelegramAdsBotPoster:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_ADS_BOT_TOKEN")
        self.channel_id = os.getenv("TELEGRAM_ADS_CHANNEL")
        self.stats = {"posted": 0, "failed": 0}
    
    def post_to_channel(self, text, photo_url=None):
        if not self.bot_token or not self.channel_id:
            print("⚠️ Telegram Ads Bot не настроен!")
            return False
        try:
            if photo_url:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.bot_token}/sendPhoto",
                    data={"chat_id": self.channel_id, "caption": text, "parse_mode": "Markdown"},
                    files={"photo": requests.get(photo_url).content}
                )
            else:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                    json={"chat_id": self.channel_id, "text": text, "parse_mode": "Markdown"},
                    timeout=30
                )
            if response.status_code == 200:
                print(f"✅ Telegram Ads Bot — отправлено!")
                self.stats["posted"] += 1
                return True
            else:
                print(f"⚠️ Ошибка Ads Bot: {response.text}")
                self.stats["failed"] += 1
                return False
        except Exception as e:
            print(f"⚠️ Ошибка Ads Bot: {e}")
            self.stats["failed"] += 1
            return False
    
    def run(self):
        print("📢 Постим в Telegram Ads Bot (свой канал)...")
        text = f"""🚀 **One•Two•Three — экосистема на Solana!**

Три токена. Три уровня. Один кошелёк.

**$ONE** — микро-вход — {TOKEN_DATA['prices']['ONE']}
🔗 {TOKEN_DATA['sites']['ONE']}

**€TWO** — средний чек — {TOKEN_DATA['prices']['TWO']}
🔗 {TOKEN_DATA['sites']['TWO']}

**£THREE** — крупные платежи — {TOKEN_DATA['prices']['THREE']}
🔗 {TOKEN_DATA['sites']['THREE']}

⚡ Solana: мгновенные транзакции, комиссия < $0.001
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments"""
        self.post_to_channel(text)

# ============================================
# 4. AIBTC.NEWS CLASSIFIEDS
# ============================================
class AibtcNewsPoster:
    def __init__(self):
        self.stats = {"posted": 0, "failed": 0}
    
    def post_to_aibtc(self, text):
        try:
            # CLI-команда через subprocess
            import subprocess
            result = subprocess.run([
                "bun", "run", "aibtc-news-classifieds/aibtc-news-classifieds.ts", "post-classified",
                "--title", "One•Two•Three — Solana Ecosystem",
                "--body", text,
                "--category", "services",
                "--btc-address", os.getenv("BTC_ADDRESS", "")
            ], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✅ aibtc.news — опубликовано!")
                self.stats["posted"] += 1
                return True
            else:
                print(f"⚠️ Ошибка aibtc.news: {result.stderr}")
                self.stats["failed"] += 1
                return False
        except Exception as e:
            print(f"⚠️ Ошибка aibtc.news: {e}")
            self.stats["failed"] += 1
            return False
    
    def run(self):
        print("📢 Постим в aibtc.news Classifieds...")
        text = f"""One•Two•Three ($ONE, €TWO, £THREE) — the first progressive fintech ecosystem on Solana.

Prices: $ONE={TOKEN_DATA['prices']['ONE']}, €TWO={TOKEN_DATA['prices']['TWO']}, £THREE={TOKEN_DATA['prices']['THREE']}

Websites:
$ONE: {TOKEN_DATA['sites']['ONE']}
€TWO: {TOKEN_DATA['sites']['TWO']}
£THREE: {TOKEN_DATA['sites']['THREE']}

TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments"""
        self.post_to_aibtc(text)

# ============================================
# 5. RUDOS.SU (БЕЗ РЕГИСТРАЦИИ)
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
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post_to_rudos(self, text):
        driver = self._init_driver()
        try:
            print("📤 RuDos.su...")
            driver.get("https://rudos.su/add")
            time.sleep(5)
            
            wait = WebDriverWait(driver, 15)
            
            # Заголовок
            title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
            title_field.send_keys("One•Two•Three — экосистема на Solana")
            time.sleep(1)
            
            # Описание
            desc_field = driver.find_element(By.NAME, "description")
            desc_field.send_keys(text)
            time.sleep(1)
            
            # Публикация
            publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Опубликовать')]")
            publish_btn.click()
            time.sleep(5)
            
            print(f"✅ RuDos.su — опубликовано!")
            self.stats["posted"] += 1
            driver.quit()
            return True
        except Exception as e:
            print(f"⚠️ Ошибка RuDos.su: {e}")
            self.stats["failed"] += 1
            driver.quit()
            return False
    
    def run(self):
        print("📢 Постим в RuDos.su...")
        text = f"""One•Two•Three ($ONE, €TWO, £THREE) — первая прогрессивная финтех-экосистема на Solana.

Три токена. Три валюты. Три ценовых уровня. Один кошелёк.

· $ONE — микро-вход — {TOKEN_DATA['prices']['ONE']}
  {TOKEN_DATA['sites']['ONE']}
· €TWO — средний чек — {TOKEN_DATA['prices']['TWO']}
  {TOKEN_DATA['sites']['TWO']}
· £THREE — крупные микро-платежи — {TOKEN_DATA['prices']['THREE']}
  {TOKEN_DATA['sites']['THREE']}

🔹 Технологии: Solana (мгновенные транзакции, комиссия < $0.001)
🔹 Ликвидность: Meteora DAMM V2
🔹 Безопасность: Аудит, блокировка ликвидности на 365 дней

📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments"""
        self.post_to_rudos(text)

# ============================================
# 6. XMRBAZAAR (ЧЕРЕЗ SELENIUM)
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
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post_to_xmrbazaar(self, text):
        driver = self._init_driver()
        try:
            print("📤 XmrBazaar...")
            driver.get("https://xmrbazaar.com/board/create")
            time.sleep(5)
            
            wait = WebDriverWait(driver, 15)
            
            # Заголовок
            title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
            title_field.send_keys("One•Two•Three — Solana Ecosystem")
            time.sleep(1)
            
            # Описание
            desc_field = driver.find_element(By.NAME, "description")
            desc_field.send_keys(text)
            time.sleep(1)
            
            # Категория
            category = driver.find_element(By.NAME, "category")
            category.send_keys("Cryptocurrency")
            time.sleep(1)
            
            # Публикация
            publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
            publish_btn.click()
            time.sleep(5)
            
            print(f"✅ XmrBazaar — опубликовано!")
            self.stats["posted"] += 1
            driver.quit()
            return True
        except Exception as e:
            print(f"⚠️ Ошибка XmrBazaar: {e}")
            self.stats["failed"] += 1
            driver.quit()
            return False
    
    def run(self):
        print("📢 Постим в XmrBazaar...")
        text = f"""One•Two•Three ($ONE, €TWO, £THREE) — the first progressive fintech ecosystem on Solana!

Three tokens. Three currencies. Three price levels. One wallet.

· $ONE — micro-entry — {TOKEN_DATA['prices']['ONE']}
  {TOKEN_DATA['sites']['ONE']}
· €TWO — medium check — {TOKEN_DATA['prices']['TWO']}
  {TOKEN_DATA['sites']['TWO']}
· £THREE — large micro-payments — {TOKEN_DATA['prices']['THREE']}
  {TOKEN_DATA['sites']['THREE']}

🔹 Technology: Solana (instant txs, fee < $0.001)
🔹 Liquidity: Meteora DAMM V2
🔹 Security: Audited, LP locked 365 days

📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments"""
        self.post_to_xmrbazaar(text)

# ============================================
# 7. ОСНОВНОЙ БОТ (ВСЕ ПЛОЩАДКИ)
# ============================================
class MainBot:
    def __init__(self):
        self.binance = BinanceSquarePoster()
        self.telegraph = TelegraphPoster()
        self.telegram_ads = TelegramAdsBotPoster()
        self.aibtc = AibtcNewsPoster()
        self.rudos = RudosPoster()
        self.xmrbazaar = XmrBazaarPoster()
        self.setup_gemini()
    
    def setup_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.model = None
    
    def generate_article(self):
        if not self.model:
            return "One•Two•Three", "Экосистема на Solana. Сайты: one.artem.pro, two.artem.pro, three.artem.pro"
        try:
            prompt = f"""
            Напиши статью про One•Two•Three на Solana.
            Токены: $ONE ({TOKEN_DATA['prices']['ONE']}), €TWO ({TOKEN_DATA['prices']['TWO']}), £THREE ({TOKEN_DATA['prices']['THREE']})
            Сайты: {TOKEN_DATA['sites']['ONE']}, {TOKEN_DATA['sites']['TWO']}, {TOKEN_DATA['sites']['THREE']}
            TG: {TOKEN_DATA['telegram']}
            Верни JSON: {{"title": "...", "content": "..."}}
            """
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            if result.startswith('{'):
                data = json.loads(result)
                return data.get('title'), data.get('content')
            lines = result.split('\n')
            return lines[0].strip('# ').strip(), '\n'.join(lines[1:])
        except:
            return "One•Two•Three", "Экосистема на Solana. Сайты: one.artem.pro, two.artem.pro, three.artem.pro"
    
    def post_to_telegram(self, text):
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        if not bot_token or not chat_id:
            return False
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=30
            )
            return response.status_code == 200
        except:
            return False
    
    def run(self):
        print("🚀 One•Two•Three Расклейщик запущен!")
        print("🌐 Площадки: Binance Square + Telegraph + Telegram Ads Bot + aibtc.news + RuDos.su + XmrBazaar")
        print("=" * 60)
        
        # 1. Telegraph (статья)
        print("\n📝 Генерируем статью для Telegraph...")
        title, content = self.generate_article()
        if title and content:
            url = self.telegraph.post_to_telegraph(title, content)
            if url:
                self.post_to_telegram(f"📝 **Статья про One•Two•Three**\n\n{title}\n\n🔗 {url}")
        
        # 2. Binance Square
        print("\n📢 Постим в Binance Square...")
        self.binance.run(posts_per_lang=3)
        
        # 3. Telegram Ads Bot (свой канал)
        print("\n📢 Постим в Telegram Ads Bot...")
        self.telegram_ads.run()
        
        # 4. aibtc.news Classifieds
        print("\n📢 Постим в aibtc.news...")
        self.aibtc.run()
        
        # 5. RuDos.su
        print("\n📢 Постим в RuDos.su...")
        self.rudos.run()
        
        # 6. XmrBazaar
        print("\n📢 Постим в XmrBazaar...")
        self.xmrbazaar.run()
        
        # 7. Финальный отчет
        self.post_to_telegram("✅ **Все циклы завершены!**")
        print("\n✅ Все циклы завершены!")

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    bot = MainBot()
    bot.run()
