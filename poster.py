import os
import time
import random
import json
import requests
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============================================
# ДАННЫЕ ТВОЕГО ТОКЕНА
# ============================================
TOKEN_DATA = {
    "name": "One•Two•Three",
    "symbols": ["ONE", "TWO", "THREE"],
    "contracts": {
        "ONE": "CGn6yYGTUkctq9PqDdK6ALgfxTS1vTBr9NWBPuoNYmad",
        "TWO": "H5kjSzmxW98iZ2Xvx7e45hxxyDjMYTk6z8aJfeFsj46d",
        "THREE": "uM1kuvsLYauDQZh8g6RrNw3oLAfSAvgEojvJT5hCLNV"
    },
    "links": {
        "website": "https://onetwothree.xyz",
        "telegram": "https://t.me/onetwothree"
    },
    "hashtags": "#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments"
}

# ============================================
# ГЕНЕРАТОР ПОСТОВ
# ============================================
class PostGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️ GROQ_API_KEY не найден")
            self.client = None
        else:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )
    
    def generate_post(self):
        """Генерирует пост из шаблонов"""
        templates = [
            f"""🚀 One•Two•Three — экосистема микро-платежей на Solana!

· $ONE = $0.01
· €TWO = €0.05  
· £THREE = £0.10

✅ Мгновенные транзакции
✅ Комиссия < $0.001
✅ Прямые пулы на Meteora

🔗 Сайт: {TOKEN_DATA['links']['website']}
📱 TG: @onetwothree

{TOKEN_DATA['hashtags']}""",

            f"""One•Two•Three ($ONE, €TWO, £THREE) — первая прогрессивная финтех-экосистема на Solana.

Три токена. Три валюты. Три ценовых уровня. Один кошелёк.

· $ONE — микро-вход
· €TWO — средний чек
· £THREE — крупные микро-платежи

🔹 Технологии: Solana (мгновенные транзакции, комиссия < $0.001)
🔹 Ликвидность: Meteora DAMM V2

"One, Two, Three — your change, your choice."

{TOKEN_DATA['hashtags']}""",

            f"""💰 One•Two•Three — инвестиционная логика:

📊 Эмиссия:
· $ONE: 9,000,000,000,000,000
· €TWO: 999,000,000,000,000  
· £THREE: 99,000,000,000,000

💰 Ценовая лестница: 1¢ → 5¢ → 10¢

🔐 Безопасность:
· Mint Authority отключён
· Ликвидность заблокирована на 365 дней

🌍 Почему Solana: 65 000 TPS, комиссия < $0.001

{TOKEN_DATA['hashtags']}"""
        ]
        
        return random.choice(templates)

# ============================================
# ОСНОВНОЙ ПОСТЕР
# ============================================
class CryptoPoster:
    def __init__(self):
        self.generator = PostGenerator()
        self.stats = {"posted": 0, "failed": 0, "platforms": {}}
        self.load_stats()
    
    def load_stats(self):
        try:
            with open("stats.json", "r") as f:
                self.stats = json.load(f)
        except:
            self.stats = {"posted": 0, "failed": 0, "platforms": {}}
    
    def save_stats(self):
        with open("stats.json", "w") as f:
            json.dump(self.stats, f, indent=2)
    
    def _init_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        return webdriver.Chrome(options=options)
    
    def post_to_telegram(self, text):
        """Отправляет пост в Telegram"""
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        
        if not bot_token or not chat_id:
            print("⚠️ Telegram не настроен")
            return False
        
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Пост в Telegram опубликован!")
                self.stats["posted"] += 1
                self.stats["platforms"]["telegram"] = self.stats["platforms"].get("telegram", 0) + 1
                return True
            else:
                print(f"⚠️ Ошибка Telegram: {response.text}")
                return False
        except Exception as e:
            print(f"⚠️ Ошибка Telegram: {e}")
            return False
    
    def post_to_avito(self, text):
        """Публикует на Avito (тестовая версия)"""
        print(f"📤 Avito: {text[:50]}...")
        # Здесь можно добавить реальную публикацию позже
        self.stats["posted"] += 1
        self.stats["platforms"]["avito"] = self.stats["platforms"].get("avito", 0) + 1
        return True
    
    def send_report(self):
        """Отправляет отчет"""
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        
        if bot_token and chat_id:
            try:
                text = f"""
📊 **One•Two•Three | Отчет**

✅ Всего постов: {self.stats['posted']}
❌ Ошибок: {self.stats['failed']}

📋 По площадкам:"""
                
                for platform, count in self.stats.get("platforms", {}).items():
                    text += f"\n  • {platform}: {count}"
                
                text += f"\n\n🕐 {time.strftime('%Y-%m-%d %H:%M:%S')}"
                
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                    timeout=30
                )
                print("📨 Отчет отправлен")
            except Exception as e:
                print(f"⚠️ Ошибка отчета: {e}")
    
    def run(self):
        """Запуск"""
        print("🚀 One•Two•Three Расклейщик запущен!")
        print("=" * 50)
        
        # Генерируем 5 постов
        for i in range(5):
            print(f"\n📝 Пост {i+1}/5")
            post_text = self.generator.generate_post()
            print(f"📄 {post_text[:100]}...")
            
            # Отправляем в Telegram
            self.post_to_telegram(post_text)
            
            # Имитация публикации на Avito
            self.post_to_avito(post_text)
            
            if i < 4:
                sleep_time = random.randint(60, 180)
                print(f"💤 Ждем {sleep_time} секунд...")
                time.sleep(sleep_time)
        
        self.save_stats()
        self.send_report()
        print("\n✅ Цикл завершен!")

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    poster = CryptoPoster()
    poster.run()
