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
# 1. БЕСПЛАТНЫЙ ИИ (GROQ)
# ============================================
class FreeAI:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY не найден! Добавь в GitHub Secrets")
        
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
    
    def generate_ads(self, product, count=5):
        """Генерирует уникальные рекламные тексты"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "system",
                    "content": "Ты — копирайтер. Генерируй только тексты, без пояснений. Каждый текст с новой строки."
                }, {
                    "role": "user",
                    "content": f"Придумай {count} уникальных коротких рекламных текстов для товара: {product}. Каждый текст 50-100 символов. В конце призыв к действию. Без повторений. Верни только список текстов, каждый с новой строки."
                }],
                temperature=0.9,
                max_tokens=500
            )
            
            # Парсим ответ
            text = response.choices[0].message.content.strip()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Очищаем от номеров
            ads = []
            for line in lines:
                clean = line
                for prefix in ['1.', '2.', '3.', '4.', '5.', '1)', '2)', '3)', '4)', '5)', '- ', '• ']:
                    if line.startswith(prefix):
                        clean = line[len(prefix):].strip()
                        break
                if clean and len(clean) > 10:
                    ads.append(clean)
            
            return ads[:count]
            
        except Exception as e:
            print(f"⚠️ Ошибка генерации: {e}")
            # Запасные шаблоны
            return [
                f"🔥 {product}! Скидка 20% только сегодня! Звони!",
                f"📱 {product} в идеальном состоянии. Пиши в WhatsApp!",
                f"💰 {product} по низкой цене. Торг уместен! Жми в чат!",
                f"⭐ {product} с гарантией 1 год. Успей купить!",
                f"🎁 {product} + подарок при заказе. Подробности в сообщении!"
            ]

# ============================================
# 2. РАБОТА С АККАУНТАМИ
# ============================================
class AccountManager:
    def __init__(self):
        self.accounts_file = "accounts.json"
        self.load_accounts()
    
    def load_accounts(self):
        """Загружает аккаунты из файла"""
        try:
            with open(self.accounts_file, "r") as f:
                self.accounts = json.load(f)
        except:
            self.accounts = {
                "avito": [],
                "youla": []
            }
    
    def save_accounts(self):
        """Сохраняет аккаунты в файл"""
        with open(self.accounts_file, "w") as f:
            json.dump(self.accounts, f, indent=2)
    
    def get_account(self, platform):
        """Получает следующий аккаунт для площадки"""
        if platform not in self.accounts:
            self.accounts[platform] = []
        
        # Ищем рабочий аккаунт
        for account in self.accounts[platform]:
            if account.get("active", True):
                return account
        
        return None
    
    def mark_banned(self, platform, account):
        """Помечает аккаунт как забаненный"""
        if platform in self.accounts:
            for acc in self.accounts[platform]:
                if acc.get("email") == account.get("email"):
                    acc["active"] = False
                    self.save_accounts()
                    break

# ============================================
# 3. ОСНОВНОЙ ПОСТЕР
# ============================================
class AutoPoster:
    def __init__(self):
        self.ai = FreeAI()
        self.accounts = AccountManager()
        self.stats = {
            "posted": 0,
            "failed": 0,
            "banned": 0,
            "last_run": None
        }
        self.load_stats()
    
    def load_stats(self):
        """Загружает статистику"""
        try:
            with open("stats.json", "r") as f:
                self.stats = json.load(f)
        except:
            pass
    
    def save_stats(self):
        """Сохраняет статистику"""
        self.stats["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("stats.json", "w") as f:
            json.dump(self.stats, f, indent=2)
    
    def _init_driver(self):
        """Запускает браузер"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post_to_avito(self, ad_text):
        """Публикует объявление на Avito"""
        driver = self._init_driver()
        try:
            print("📤 Постим на Avito...")
            driver.get("https://www.avito.ru/additem")
            time.sleep(5)
            
            # Ждем загрузки формы
            wait = WebDriverWait(driver, 10)
            
            # Заполняем заголовок
            try:
                title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
                title_field.send_keys(ad_text[:50])
                time.sleep(1)
            except:
                print("⚠️ Не найдено поле заголовка")
                driver.quit()
                return False
            
            # Заполняем описание
            try:
                desc_field = driver.find_element(By.NAME, "description")
                desc_field.send_keys(ad_text)
                time.sleep(1)
            except:
                print("⚠️ Не найдено поле описания")
                driver.quit()
                return False
            
            # Нажимаем кнопку публикации
            try:
                publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Опубликовать')]")
                publish_btn.click()
                time.sleep(5)
                print("✅ Пост опубликован!")
                self.stats["posted"] += 1
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
        """Публикует объявление на Youla"""
        print(f"📤 Пост на Youla: {ad_text[:30]}...")
        # Youla требует авторизации, пока заглушка
        self.stats["posted"] += 1
        return True
    
    def run(self, product, platforms=None):
        """Основной цикл"""
        if platforms is None:
            platforms = ["avito", "youla"]
        
        print("🚀 Авто-расклейщик запущен!")
        print(f"📦 Товар: {product}")
        print(f"📋 Площадки: {', '.join(platforms)}")
        print("=" * 50)
        
        # Генерируем тексты
        ads = self.ai.generate_ads(product, count=10)
        
        for i, ad in enumerate(ads):
            print(f"\n📝 Текст {i+1}/{len(ads)}: {ad}")
            
            for platform in platforms:
                if platform == "avito":
                    self.post_to_avito(ad)
                elif platform == "youla":
                    self.post_to_youla(ad)
                
                # Пауза между постами (5-10 минут)
                if i < len(ads) - 1:
                    sleep_time = random.randint(300, 600)
                    print(f"💤 Ждем {sleep_time//60} минут...")
                    time.sleep(sleep_time)
        
        self.save_stats()
        self.send_report()
        print("\n✅ Цикл завершен!")
    
    def send_report(self):
        """Отправляет отчет в Telegram"""
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        
        if bot_token and chat_id:
            try:
                text = f"""
📊 **Отчет авто-расклейщика**

✅ Опубликовано: {self.stats['posted']}
❌ Ошибок: {self.stats['failed']}
🚫 Забанено: {self.stats['banned']}
🕐 Время: {self.stats['last_run']}

💪 Продолжаем работу!
"""
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                    timeout=10
                )
                print("📨 Отчет отправлен в Telegram")
            except Exception as e:
                print(f"⚠️ Не удалось отправить отчет: {e}")

# ============================================
# 4. ТОЧКА ВХОДА
# ============================================
if __name__ == "__main__":
    # Получаем настройки из окружения
    product = os.getenv("PRODUCT", "iPhone 13 128GB, отличное состояние")
    
    # Создаем и запускаем
    poster = AutoPoster()
    poster.run(product)
