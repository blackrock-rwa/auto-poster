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
    }
}

# ============================================
# 1. ГЕНЕРАТОР ПОСТОВ (русский + английский + китайский)
# ============================================
class PostGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.use_ai = bool(api_key)
        if self.use_ai:
            from openai import OpenAI
            self.client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
        else:
            self.client = None

    def generate_posts(self):
        """Генерирует посты на русском, английском и китайском"""
        
        russian_posts = [
            f"""One•Two•Three ($ONE, €TWO, £THREE) — первая прогрессивная финтех-экосистема на Solana.

Три токена. Три валюты. Три ценовых уровня. Один кошелёк.

· $ONE — микро-вход (доступный каждому)
· €TWO — средний чек (ежедневные траты)
· £THREE — крупные микро-платежи

🔹 Технологии: Solana (мгновенные транзакции, комиссия < $0.001)
🔹 Ликвидность: Meteora DAMM V2
🔹 Безопасность: Аудит, блокировка ликвидности на 365 дней

Сайт: {TOKEN_DATA['links']['website']}
TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments""",

            f"""One•Two•Three — инвестиционная логика:

📊 Эмиссия:
· $ONE: 9,000,000,000,000,000
· €TWO: 999,000,000,000,000
· £THREE: 99,000,000,000,000

💰 Ценовая лестница: 1¢ → 5¢ → 10¢

🔐 Безопасность:
· Mint Authority отключён
· Ликвидность заблокирована на 365 дней

🌍 Почему Solana: 65 000 TPS, комиссия < $0.001

#ONE #TWO #THREE #Solana #DeFi #Investing"""
        ]
        
        english_posts = []
        chinese_posts = []
        
        if self.use_ai and self.client:
            for post in russian_posts:
                try:
                    eng_response = self.client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Translate to English. Keep emojis and hashtags."}, {"role": "user", "content": post}],
                        temperature=0.5, max_tokens=500
                    )
                    english_posts.append(eng_response.choices[0].message.content)
                    
                    ch_response = self.client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Translate to Chinese (Simplified). Keep emojis and hashtags."}, {"role": "user", "content": post}],
                        temperature=0.5, max_tokens=500
                    )
                    chinese_posts.append(ch_response.choices[0].message.content)
                    print(f"✅ Пост переведен на EN и ZH")
                except Exception as e:
                    print(f"⚠️ Ошибка перевода: {e}")
                    # fallback
                    english_posts.append(f"🚀 One•Two•Three — Micro-payments on Solana!\n\n· $ONE = $0.01\n· €TWO = €0.05\n· £THREE = £0.10\n\n#ONE #TWO #THREE #Solana")
                    chinese_posts.append(f"🚀 One•Two•Three — Solana 微支付生态！\n\n· $ONE = $0.01\n· €TWO = €0.05\n· £THREE = £0.10\n\n#ONE #TWO #THREE #Solana")
        else:
            # fallback если нет API
            english_posts = [f"🚀 One•Two•Three — Micro-payments on Solana! #ONE #TWO #THREE #Solana"]
            chinese_posts = [f"🚀 One•Two•Three — Solana 微支付生态！ #ONE #TWO #THREE #Solana"]
        
        return {"ru": russian_posts, "en": english_posts, "zh": chinese_posts}

# ============================================
# 2. РЕАЛЬНЫЙ ПОСТЕР НА АВИТО
# ============================================
class AvitoPoster:
    def __init__(self):
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
    
    def _init_driver(self):
        options = Options()
        options.add_argument('--headless')  # убрать для отладки
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post_to_avito(self, title, description, lang="ru"):
        driver = self._init_driver()
        try:
            print(f"📤 Avito ({lang.upper()}) — открываем страницу...")
            driver.get("https://www.avito.ru/additem")
            time.sleep(5)
            
            wait = WebDriverWait(driver, 15)
            
            # Заполняем заголовок (название)
            try:
                title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
                title_field.clear()
                title_field.send_keys(title[:50])
                time.sleep(1)
                print(f"   ✅ Заголовок: {title[:30]}...")
            except Exception as e:
                print(f"   ❌ Ошибка заголовка: {e}")
                driver.quit()
                return False
            
            # Заполняем описание
            try:
                desc_field = driver.find_element(By.NAME, "description")
                desc_field.clear()
                desc_field.send_keys(description)
                time.sleep(1)
                print(f"   ✅ Описание: {len(description)} символов")
            except Exception as e:
                print(f"   ❌ Ошибка описания: {e}")
                driver.quit()
                return False
            
            # Нажимаем кнопку "Опубликовать"
            try:
                publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Опубликовать')]")
                publish_btn.click()
                time.sleep(5)
                print(f"   ✅ Кнопка 'Опубликовать' нажата!")
                self.stats["posted"] += 1
                self.stats["platforms"][f"avito_{lang}"] = self.stats["platforms"].get(f"avito_{lang}", 0) + 1
                driver.quit()
                return True
            except Exception as e:
                print(f"   ❌ Кнопка не найдена: {e}")
                driver.quit()
                return False
                
        except Exception as e:
            print(f"⚠️ Критическая ошибка Avito ({lang}): {e}")
            driver.quit()
            self.stats["failed"] += 1
            return False
    
    def post_to_telegram(self, text, lang="ru"):
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        if not bot_token or not chat_id:
            return False
        
        try:
            label = {"ru": "🇷🇺", "en": "🇬🇧", "zh": "🇨🇳"}.get(lang, "")
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": f"{label}\n\n{text}", "parse_mode": "Markdown"},
                timeout=30
            )
            if response.status_code == 200:
                print(f"✅ Telegram ({lang}) отправлен")
                self.stats["posted"] += 1
                self.stats["platforms"][f"telegram_{lang}"] = self.stats["platforms"].get(f"telegram_{lang}", 0) + 1
                return True
            return False
        except Exception as e:
            print(f"⚠️ Ошибка Telegram ({lang}): {e}")
            return False
    
    def send_report(self):
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        if bot_token and chat_id:
            try:
                text = f"📊 **Отчет расклейки**\n\n✅ Всего постов: {self.stats['posted']}\n❌ Ошибок: {self.stats['failed']}\n\n📋 По площадкам:"
                for platform, count in self.stats.get("platforms", {}).items():
                    text += f"\n  • {platform}: {count}"
                text += f"\n\n🕐 {time.strftime('%Y-%m-%d %H:%M:%S')}"
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=30)
                print("📨 Отчет отправлен")
            except Exception as e:
                print(f"⚠️ Ошибка отчета: {e}")
    
    def run(self):
        print("🚀 Avito-постер запущен!")
        print("🌍 Языки: Русский 🇷🇺, English 🇬🇧, 中文 🇨🇳")
        print("=" * 60)
        
        generator = PostGenerator()
        posts = generator.generate_posts()
        
        for lang, texts in posts.items():
            lang_name = {"ru": "Русский", "en": "English", "zh": "中文"}[lang]
            print(f"\n📝 Язык: {lang_name} — {len(texts)} постов")
            
            for i, text in enumerate(texts):
                print(f"\n  Пост {i+1}/{len(texts)}")
                title = text[:50]
                print(f"  📌 {title}...")
                
                # Отправляем в Telegram (как отчет)
                self.post_to_telegram(text, lang)
                
                # Публикуем на Авито
                self.post_to_avito(title, text, lang)
                
                if i < len(texts) - 1:
                    wait_time = random.randint(60, 120)  # 1-2 минуты
                    print(f"  💤 Ждем {wait_time} секунд...")
                    time.sleep(wait_time)
        
        self.save_stats()
        self.send_report()
        print("\n✅ Все циклы завершены!")

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    poster = AvitoPoster()
    poster.run()
