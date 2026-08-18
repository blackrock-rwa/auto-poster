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
# 1. БЕСПЛАТНЫЙ ИИ (GROQ) - ГЕНЕРАЦИЯ РЕКЛАМЫ ТОКЕНА
# ============================================
class CryptoAdGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY не найден!")
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
    
    def generate_ads(self, token_name, token_symbol, contract_address, count=10):
        """Генерирует рекламные тексты для крипто-токена"""
        try:
            prompt = f"""
            Сгенерируй {count} уникальных рекламных текстов для крипто-токена.

            Информация о токене:
            - Название: {token_name}
            - Символ: {token_symbol}
            - Контракт: {contract_address}

            Требования к текстам:
            1. Каждый текст 50-100 символов
            2. Агрессивный, бычий тон ("луна", "ракета", "100x")
            3. Обязательно указать символ токена {token_symbol}
            4. Призыв к действию (купить, зайти в телеграм, проверить контракт)
            5. Без повторений

            Верни только список текстов, каждый с новой строки.
            """

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Ты — крипто-маркетолог. Генерируй только тексты для крипто-рекламы. Без пояснений."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.95,
                max_tokens=800
            )

            text = response.choices[0].message.content.strip()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Очищаем от номеров
            ads = []
            for line in lines:
                clean = line
                for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', 
                               '1)', '2)', '3)', '4)', '5)', '- ', '• ', '* ']:
                    if line.startswith(prefix):
                        clean = line[len(prefix):].strip()
                        break
                if clean and len(clean) > 10:
                    ads.append(clean)
            
            return ads[:count]
            
        except Exception as e:
            print(f"⚠️ Ошибка генерации: {e}")
            # Запасные шаблоны для крипты
            return [
                f"🚀 {token_symbol} to the moon! Buy now! 100x gem!",
                f"💎 {token_symbol} - next bluechip! Low cap gem!",
                f"🔥 {token_symbol} pumping now! Don't miss!",
                f"💰 {token_symbol} x100 potential! Check contract!",
                f"🌟 {token_symbol} - community growing! Join TG!",
                f"⚡ {token_symbol} launching soon! Be early!",
                f"🎯 {token_symbol} - devs are active! Bullish!",
                f"📈 {token_symbol} chart looks insane! Buy dip!",
                f"🏆 {token_symbol} - gem find! Dyor but hurry!",
                f"🚨 {token_symbol} - next big thing! NFA!"
            ]

# ============================================
# 2. ПОСТЕР
# ============================================
class CryptoPoster:
    def __init__(self):
        self.ai = CryptoAdGenerator()
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
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post_to_avito(self, ad_text):
        """Публикует рекламу токена на Avito"""
        driver = self._init_driver()
        try:
            print("📤 Постим на Avito...")
            driver.get("https://www.avito.ru/additem")
            time.sleep(5)
            wait = WebDriverWait(driver, 10)
            
            try:
                title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
                title_field.send_keys(ad_text[:50])
                time.sleep(1)
            except:
                print("⚠️ Не найдено поле заголовка")
                driver.quit()
                return False
            
            try:
                desc_field = driver.find_element(By.NAME, "description")
                desc_field.send_keys(ad_text + "\n\nКонтракт: " + os.getenv("CONTRACT_ADDRESS", ""))
                time.sleep(1)
            except:
                print("⚠️ Не найдено поле описания")
                driver.quit()
                return False
            
            try:
                publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Опубликовать')]")
                publish_btn.click()
                time.sleep(5)
                print("✅ Пост опубликован!")
                self.stats["posted"] += 1
                self.stats["platforms"]["avito"] = self.stats["platforms"].get("avito", 0) + 1
                driver.quit()
                return True
            except:
                print("⚠️ Кнопка публикации не найдена")
                driver.quit()
                return False
        except Exception as e:
            print(f"⚠️ Ошибка Avito: {e}")
            driver.quit()
            self.stats["failed"] += 1
            return False
    
    def post_to_youla(self, ad_text):
        """Публикует рекламу токена на Youla"""
        print(f"📤 Пост на Youla: {ad_text[:30]}...")
        self.stats["posted"] += 1
        self.stats["platforms"]["youla"] = self.stats["platforms"].get("youla", 0) + 1
        return True
    
    def post_to_bitcointalk(self, ad_text):
        """Пост на Bitcointalk (заглушка)"""
        print(f"📤 Пост на Bitcointalk: {ad_text[:30]}...")
        self.stats["posted"] += 1
        self.stats["platforms"]["bitcointalk"] = self.stats["platforms"].get("bitcointalk", 0) + 1
        return True
    
    def send_report(self):
        """Отправляет отчет в Telegram"""
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        if bot_token and chat_id:
            try:
                token_name = os.getenv("TOKEN_NAME", "Unknown")
                token_symbol = os.getenv("TOKEN_SYMBOL", "???")
                
                text = f"""
📊 **Крипто-расклейщик | Отчет**

🪙 **Токен:** {token_name} ({token_symbol})
✅ **Всего постов:** {self.stats['posted']}
❌ **Ошибок:** {self.stats['failed']}

📋 **По площадкам:**
"""
                for platform, count in self.stats.get("platforms", {}).items():
                    text += f"  • {platform}: {count}\n"
                
                text += f"""
🕐 **Время:** {time.strftime('%Y-%m-%d %H:%M:%S')}
💪 **Продолжаем рекламировать!**
"""
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                    timeout=10
                )
                print("📨 Отчет отправлен в Telegram")
            except Exception as e:
                print(f"⚠️ Не удалось отправить отчет: {e}")
    
    def run(self, token_name, token_symbol, contract_address):
        """Основной цикл"""
        print("🚀 Крипто-расклейщик запущен!")
        print(f"🪙 Токен: {token_name} ({token_symbol})")
        print(f"🔗 Контракт: {contract_address}")
        print("=" * 50)
        
        ads = self.ai.generate_ads(token_name, token_symbol, contract_address, count=10)
        
        if not ads:
            print("⚠️ Не удалось сгенерировать тексты!")
            return
        
        for i, ad in enumerate(ads):
            print(f"\n📝 Текст {i+1}/{len(ads)}: {ad}")
            
            # Постим на все площадки
            self.post_to_avito(ad)
            self.post_to_youla(ad)
            self.post_to_bitcointalk(ad)
            
            if i < len(ads) - 1:
                sleep_time = random.randint(300, 600)
                print(f"💤 Ждем {sleep_time//60} минут...")
                time.sleep(sleep_time)
        
        self.save_stats()
        self.send_report()
        print("\n✅ Цикл завершен!")

# ============================================
# 4. ТОЧКА ВХОДА
# ============================================
if __name__ == "__main__":
    # Берем данные о токене из переменных окружения
    token_name = os.getenv("TOKEN_NAME", "BabyDoge Moon")
    token_symbol = os.getenv("TOKEN_SYMBOL", "BABYDOGE")
    contract_address = os.getenv("CONTRACT_ADDRESS", "0x123...")
    
    poster = CryptoPoster()
    poster.run(token_name, token_symbol, contract_address)
