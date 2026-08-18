import os
import time
import random
import json
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =====================================================
# 1. БЕСПЛАТНЫЙ ИИ (GigaChat / Yandex GPT)
# =====================================================
class FreeAI:
    def __init__(self):
        # Регистрируешься → получаешь ключ → вставляешь в GitHub Secrets
        self.api_key = os.getenv("GIGACHAT_KEY") or os.getenv("YANDEX_KEY")
        self.provider = "gigachat" if os.getenv("GIGACHAT_KEY") else "yandex"
        
    def generate_ads(self, product, count=5):
        """Генерирует уникальные рекламные тексты (бесплатно)"""
        prompt = f"Придумай {count} уникальных рекламных текстов для товара: {product}. Каждый текст от 50 до 100 символов. В конце каждого текста - призыв к действию. Без повторений. Верни в виде JSON-списка."
        
        if self.provider == "gigachat":
            url = "https://api.gigachat.ru/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}"}
        else:
            url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
            headers = {"Authorization": f"Api-Key {self.api_key}"}
        
        try:
            response = requests.post(url, headers=headers, json={
                "model": "GigaChat-Max" if self.provider == "gigachat" else "yandexgpt-lite",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.9
            }, timeout=30)
            
            # Парсим ответ
            if self.provider == "gigachat":
                content = response.json()['choices'][0]['message']['content']
            else:
                content = response.json()['result']['alternatives'][0]['message']['text']
            
            # Извлекаем JSON из ответа
            import ast
            texts = ast.literal_eval(content)
            return texts[:count]
        except:
            # Если API не работает - используем шаблоны (запасной вариант)
            return [
                f"🔥 {product}! Скидка 20% только сегодня! Звони!",
                f"📱 {product} в отличном состоянии. Гарантия. Пиши в WhatsApp!",
                f"💰 {product} по самой низкой цене. Торг уместен. Жми в чат!",
                f"⭐ {product} с бесплатной доставкой. Успей купить!",
                f"🎁 {product} + подарок при заказе. Подробности в сообщении!"
            ]

# =====================================================
# 2. БЕСПЛАТНЫЕ НОМЕРА (без SMS-сервисов)
# =====================================================
class FreePhone:
    def __init__(self):
        self.used_phones = set()
        # Загружаем запасные номера (пополняешь раз в месяц)
        self.phone_pool = self._load_phone_pool()
        
    def _load_phone_pool(self):
        """Загружает номера из файла или парсит бесплатные сайты"""
        try:
            with open("phones.txt", "r") as f:
                return f.read().splitlines()
        except:
            # Если файла нет - парсим бесплатный сайт с номерами
            try:
                response = requests.get("https://receive-sms-online.info/russia-phone-numbers/", timeout=10)
                numbers = re.findall(r'(\+7\d{10})', response.text)
                return numbers[:20]  # Берем 20 номеров
            except:
                return ["+79161234567", "+79162345678", "+79163456789"]  # Тестовые
    
    def get_number(self):
        """Возвращает свободный номер"""
        available = [p for p in self.phone_pool if p not in self.used_phones]
        if not available:
            return None
        number = random.choice(available)
        self.used_phones.add(number)
        return number

# =====================================================
# 3. ОСНОВНОЙ ПОСТЕР (с Tor и авторегистрацией)
# =====================================================
class AutoPoster:
    def __init__(self):
        self.ai = FreeAI()
        self.phone = FreePhone()
        self.stats = {"posted": 0, "failed": 0, "accounts": 0}
        
    def _init_driver(self):
        """Запускает браузер через Tor (бесплатный прокси)"""
        options = Options()
        options.add_argument('--headless')  # Убрать для отладки
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        return webdriver.Chrome(options=options)
    
    def register_account(self, platform):
        """Регистрирует новый аккаунт с бесплатным номером"""
        phone = self.phone.get_number()
        if not phone:
            print("❌ Закончились номера! Добавь новые в phones.txt")
            return False
        
        driver = self._init_driver()
        try:
            driver.get(f"{platform}/register")
            time.sleep(3)
            
            # Заполняем форму (селекторы под Avito)
            email = f"user_{random.randint(10000,99999)}@mail.ru"
            driver.find_element(By.NAME, "email").send_keys(email)
            driver.find_element(By.NAME, "phone").send_keys(phone)
            driver.find_element(By.NAME, "password").send_keys("AutoPass123!")
            
            # Кнопка регистрации
            driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]").click()
            time.sleep(5)
            
            # Сохраняем куки
            cookies = driver.get_cookies()
            with open(f"account_{platform.replace('https://','')}.json", "w") as f:
                json.dump(cookies, f)
            
            self.stats["accounts"] += 1
            print(f"✅ Аккаунт создан: {phone}")
            driver.quit()
            return True
            
        except Exception as e:
            print(f"⚠️ Ошибка регистрации: {e}")
            driver.quit()
            return False
    
    def post_ad(self, platform, ad_text):
        """Публикует объявление"""
        driver = self._init_driver()
        try:
            # Загружаем сохраненные куки
            try:
                with open(f"account_{platform.replace('https://','')}.json", "r") as f:
                    cookies = json.load(f)
                    for cookie in cookies:
                        driver.add_cookie(cookie)
            except:
                # Если нет аккаунта - создаем
                self.register_account(platform)
                return False
            
            driver.get(f"{platform}/additem")
            time.sleep(3)
            
            # Заполняем поля
            driver.find_element(By.NAME, "title").send_keys(ad_text[:50])
            driver.find_element(By.NAME, "description").send_keys(ad_text)
            
            # Кнопка публикации
            driver.find_element(By.XPATH, "//button[contains(text(), 'Опубликовать')]").click()
            time.sleep(5)
            
            # Проверяем успех
            if "успешно" in driver.page_source.lower() or "размещено" in driver.page_source.lower():
                self.stats["posted"] += 1
                print(f"✅ Пост #{self.stats['posted']}: {ad_text[:30]}...")
                driver.quit()
                return True
            else:
                # Аккаунт забанен - удаляем и создаем новый
                driver.quit()
                self.register_account(platform)
                return False
                
        except Exception as e:
            print(f"⚠️ Ошибка постинга: {e}")
            driver.quit()
            return False
    
    def save_stats(self):
        """Сохраняет статистику"""
        with open("stats.json", "w") as f:
            json.dump(self.stats, f)
        
        # Отправка в Telegram (бесплатно)
        try:
            bot_token = os.getenv("TELEGRAM_TOKEN")
            chat_id = os.getenv("TELEGRAM_CHAT")
            if bot_token and chat_id:
                text = f"📊 Статистика:\n✅ Постов: {self.stats['posted']}\n❌ Ошибок: {self.stats['failed']}\n👤 Аккаунтов: {self.stats['accounts']}"
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": text}
                )
        except:
            pass

# =====================================================
# 4. ЗАПУСК (бесконечный цикл)
# =====================================================
if __name__ == "__main__":
    poster = AutoPoster()
    
    # Список площадок
    platforms = [
        "https://avito.ru",
        "https://youla.ru"
    ]
    
    # Твой товар (можно загружать из файла)
    PRODUCT = "iPhone 13 128GB, идеальное состояние"
    
    print("🚀 Запуск авто-расклейщика...")
    
    while True:
        for platform in platforms:
            # Генерируем свежие тексты (бесплатно)
            ads = poster.ai.generate_ads(PRODUCT, count=3)
            
            for ad in ads:
                success = poster.post_ad(platform, ad)
                
                if not success:
                    poster.stats["failed"] += 1
                
                # Пауза между постами (10-30 минут)
                sleep_time = random.randint(600, 1800)
                print(f"💤 Ждем {sleep_time//60} минут...")
                time.sleep(sleep_time)
            
            # После 3 постов на площадке - регистрируем новый аккаунт
            poster.register_account(platform)
        
        # Сохраняем статистику
        poster.save_stats()
        
        # Ночная пауза (6 часов)
        print("🌙 Спячка на 6 часов...")
        time.sleep(21600)
