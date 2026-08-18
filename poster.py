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
# 1. ДАННЫЕ ТВОЕГО ТОКЕНА
# ============================================
TOKEN_DATA = {
    "name": "One•Two•Three",
    "symbols": ["ONE", "TWO", "THREE"],
    "contracts": {
        "ONE": "CGn6yYGTUkctq9PqDdK6ALgfxTS1vTBr9NWBPuoNYmad",
        "TWO": "H5kjSzmxW98iZ2Xvx7e45hxxyDjMYTk6z8aJfeFsj46d",
        "THREE": "uM1kuvsLYauDQZh8g6RrNw3oLAfSAvgEojvJT5hCLNV"
    },
    "prices": {
        "ONE": "$0.01",
        "TWO": "€0.05",
        "THREE": "£0.10"
    },
    "links": {
        "website": "https://onetwothree.xyz",
        "telegram": "https://t.me/onetwothree",
        "twitter": "https://x.com/onetwothree",
        "pools": {
            "ONE/USDT": "https://www.geckoterminal.com/solana/pools/D6tgbM8TwtneypFPbTLFNYJS8Uu3WAFz4L9QRYj5HPiN",
            "TWO/USDT": "https://www.geckoterminal.com/solana/pools/Dyzw4gDGYkwdYTKvayWEXNvVCudbpzARWhiQQd4gy6w5",
            "THREE/USDC": "https://www.geckoterminal.com/solana/pools/4AeLkonsCs6aKwnKrKepM5CnNypvKYSGX4SVkDD74iUv"
        }
    },
    "hashtags": "#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments #Fintech #Web3"
}

# ============================================
# 2. БАНК ГОТОВЫХ ПОСТОВ (из твоих материалов)
# ============================================
POST_TEMPLATES = {
    "main": [
        """One•Two•Three ($ONE, €TWO, £THREE) — первая прогрессивная финтех-экосистема на Solana.

Три токена. Три валюты. Три ценовых уровня. Один кошелёк.

· $ONE — микро-вход (доступный каждому)
· €TWO — средний чек (ежедневные траты)
· £THREE — крупные микро-платежи

🔹 Технологии: Solana (мгновенные транзакции, комиссия < $0.001)
🔹 Ликвидность: Meteora DAMM V2
🔹 Безопасность: Аудит, блокировка ликвидности на 365 дней

🌐 Экосистема: Единый кошелёк, мгновенная конвертация, арбитражные механизмы.

"One, Two, Three — your change, your choice."\n\n{hashtags}"""
    ],
    
    "short": [
        """🚀 One•Two•Three — экосистема микро-платежей на Solana!

· $ONE = $0.01
· €TWO = €0.05
· £THREE = £0.10

✅ Мгновенные транзакции
✅ Комиссия < $0.001
✅ Прямые пулы на Meteora

🔗 Сайт: {website}
📱 TG: @onetwothree\n\n{hashtags}"""
    ],
    
    "investor": [
        """One•Two•Three — инвестиционная логика:

📊 Эмиссия:
· $ONE: 9,000,000,000,000,000
· €TWO: 999,000,000,000,000
· £THREE: 99,000,000,000,000

💰 Ценовая лестница: 1¢ → 5¢ → 10¢

🔐 Безопасность:
· Mint Authority отключён (эмиссия фиксирована)
· Ликвидность заблокирована на 365 дней
· Аудит смарт-контрактов

📈 Ликвидность: Meteora DAMM V2

🌍 Почему Solana: 65 000 TPS, комиссия < $0.001, DeFi №2\n\n{hashtags}"""
    ],
    
    "dev": [
        """One•Two•Three — технические детали:

· Сеть: Solana
· Стандарт: SPL
· Decimals: 9
· Платформа: PinkSale (IDO) → Meteora (DEX)
· Оракулы: Chainlink для кросс-курсов

Адреса контрактов:
· $ONE: {contract_one}
· €TWO: {contract_two}
· £THREE: {contract_three}

Пул $ONE/USDT: {pool_one}\n\n{hashtags}"""
    ],
    
    "teaser": [
        """🚀 Анонс! One•Two•Three — первая прогрессивная экосистема микро-платежей на Solana.
Три токена, три валюты, три ценовых уровня.

💰 $ONE = $0.01 | €TWO = €0.05 | £THREE = £0.10

⚡ Solana: мгновенные транзакции, комиссия < $0.001

🔗 Сайт: {website}
📱 TG: @onetwothree\n\n{hashtags}""",
        
        """💧 Пулы на Meteora уже работают:

· $ONE/USDT
· €TWO/USDT
· £THREE/USDC
· Прямые пары ONE/TWO, ONE/THREE, TWO/THREE

Торгуй сейчас! 📈

🔗 {pool_one}
🔗 {pool_two}
🔗 {pool_three}\n\n{hashtags}"""
    ]
}

# ============================================
# 3. ГЕНЕРАТОР ПОСТОВ (ИИ + ШАБЛОНЫ)
# ============================================
class PostGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY не найден!")
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
    
    def generate_post(self, post_type="random"):
        """Генерирует пост из шаблонов или через ИИ"""
        
        # Если нужен конкретный тип
        if post_type in POST_TEMPLATES:
            template = random.choice(POST_TEMPLATES[post_type])
        else:
            # Смешиваем все типы
            all_templates = []
            for templates in POST_TEMPLATES.values():
                all_templates.extend(templates)
            template = random.choice(all_templates)
        
        # Заполняем переменные
        post = template.format(
            website=TOKEN_DATA["links"]["website"],
            telegram=TOKEN_DATA["links"]["telegram"],
            twitter=TOKEN_DATA["links"]["twitter"],
            contract_one=TOKEN_DATA["contracts"]["ONE"],
            contract_two=TOKEN_DATA["contracts"]["TWO"],
            contract_three=TOKEN_DATA["contracts"]["THREE"],
            pool_one=TOKEN_DATA["links"]["pools"]["ONE/USDT"],
            pool_two=TOKEN_DATA["links"]["pools"]["TWO/USDT"],
            pool_three=TOKEN_DATA["links"]["pools"]["THREE/USDC"],
            hashtags=TOKEN_DATA["hashtags"]
        )
        
        # Иногда генерируем через ИИ для разнообразия
        if random.random() < 0.2:  # 20% постов через ИИ
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "system",
                        "content": "Ты — крипто-маркетолог. Генерируй рекламные посты для токена One•Two•Three на Solana."
                    }, {
                        "role": "user",
                        "content": f"""
                        Сгенерируй уникальный рекламный пост для крипто-токена One•Two•Three.

                        Информация:
                        - Токены: $ONE ($0.01), €TWO (€0.05), £THREE (£0.10)
                        - Сеть: Solana (мгновенные транзакции, комиссия < $0.001)
                        - Пулы: Meteora DAMM V2
                        - Сайт: onetwothree.xyz
                        - TG: @onetwothree

                        Требования:
                        - Длина 100-200 символов
                        - Агрессивный, бычий тон
                        - Упомянуть все 3 токена
                        - Призыв к действию
                        - Добавить хештеги
                        """
                    }],
                    temperature=0.9,
                    max_tokens=300
                )
                ai_post = response.choices[0].message.content.strip()
                return ai_post
            except:
                pass
        
        return post

# ============================================
# 4. ПОСТЕР
# ============================================
class CryptoPoster:
    def __init__(self):
        self.generator = PostGenerator()
        self.stats = {"posted": 0, "failed": 0, "platforms": {}}
        self.posted_history = []  # Чтобы не повторяться
        self.load_stats()
    
    def load_stats(self):
        try:
            with open("stats.json", "r") as f:
                self.stats = json.load(f)
            with open("history.json", "r") as f:
                self.posted_history = json.load(f)
        except:
            pass
    
    def save_stats(self):
        with open("stats.json", "w") as f:
            json.dump(self.stats, f, indent=2)
        with open("history.json", "w") as f:
            json.dump(self.posted_history, f, indent=2)
    
    def _init_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
        return webdriver.Chrome(options=options)
    
    def post_to_avito(self, text):
        driver = self._init_driver()
        try:
            print("📤 Постим на Avito...")
            driver.get("https://www.avito.ru/additem")
            time.sleep(5)
            wait = WebDriverWait(driver, 10)
            
            title = text[:50] if len(text) > 50 else text
            title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
            title_field.send_keys(title)
            time.sleep(1)
            
            desc_field = driver.find_element(By.NAME, "description")
            desc_field.send_keys(text[:500])
            time.sleep(1)
            
            try:
                publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Опубликовать')]")
                publish_btn.click()
                time.sleep(5)
                print("✅ Пост опубликован!")
                self.stats["posted"] += 1
                self.stats["platforms"]["avito"] = self.stats["platforms"].get("avito", 0) + 1
                self.posted_history.append({"platform": "avito", "text": text[:50], "time": time.time()})
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
    
    def post_to_telegram(self, text):
        """Постит в Telegram-канал (если есть)"""
        bot_token = os.getenv("TELEGRAM_TOKEN")
        channel_id = os.getenv("TELEGRAM_CHANNEL")  # Отдельный канал для расклейки
        
        if bot_token and channel_id:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": channel_id, "text": text, "parse_mode": "Markdown"},
                    timeout=10
                )
                print("✅ Пост в Telegram опубликован!")
                self.stats["posted"] += 1
                self.stats["platforms"]["telegram"] = self.stats["platforms"].get("telegram", 0) + 1
                return True
            except Exception as e:
                print(f"⚠️ Ошибка Telegram: {e}")
                return False
        return False
    
    def post_to_twitter(self, text):
        """Постит в Twitter (заглушка, нужен API)"""
        print(f"🐦 Twitter: {text[:50]}...")
        # Тут нужен Twitter API v2
        return True
    
    def send_report(self):
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        if bot_token and chat_id:
            try:
                text = f"""
📊 **One•Two•Three | Отчет расклейки**

🪙 **Токен:** One•Two•Three ($ONE, €TWO, £THREE)
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
    
    def run(self, posts_count=10):
        print("🚀 One•Two•Three Расклейщик запущен!")
        print(f"🪙 Токен: One•Two•Three ($ONE, €TWO, £THREE)")
        print(f"📊 Постов за цикл: {posts_count}")
        print("=" * 50)
        
        for i in range(posts_count):
            # Выбираем тип поста (чередуем)
            post_types = ["main", "short", "investor", "dev", "teaser"]
            post_type = random.choice(post_types)
            
            print(f"\n📝 Пост {i+1}/{posts_count} (тип: {post_type})")
            post_text = self.generator.generate_post(post_type)
            print(f"📄 {post_text[:100]}...")
            
            # Постим на все площадки
            self.post_to_avito(post_text)
            self.post_to_telegram(post_text)
            self.post_to_twitter(post_text)
            
            if i < posts_count - 1:
                sleep_time = random.randint(300, 900)
                print(f"💤 Ждем {sleep_time//60} минут...")
                time.sleep(sleep_time)
        
        self.save_stats()
        self.send_report()
        print("\n✅ Цикл завершен!")

# ============================================
# 5. ТОЧКА ВХОДА
# ============================================
if __name__ == "__main__":
    poster = CryptoPoster()
    poster.run(posts_count=10)
