import os
import time
import random
import json
import requests
from openai import OpenAI
import google.generativeai as genai

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
    "prices": {
        "ONE": "$0.01",
        "TWO": "€0.05", 
        "THREE": "£0.10"
    }
}

# ============================================
# ГЕНЕРАТОР СТАТЕЙ (Gemini)
# ============================================
class ArticleGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.model = None
    
    def generate_article(self):
        """Генерирует SEO-статью про One•Two•Three"""
        if not self.model:
            return None, None
        
        try:
            prompt = f"""
            Напиши статью про крипто-токен {TOKEN_DATA['name']} на Solana.

            Информация о токене:
            - Три токена: $ONE ({TOKEN_DATA['prices']['ONE']}), €TWO ({TOKEN_DATA['prices']['TWO']}), £THREE ({TOKEN_DATA['prices']['THREE']})
            - Сеть: Solana (мгновенные транзакции, комиссия < $0.001)
            - Адреса контрактов:
              $ONE: {TOKEN_DATA['contracts']['ONE']}
              €TWO: {TOKEN_DATA['contracts']['TWO']}
              £THREE: {TOKEN_DATA['contracts']['THREE']}
            - Сайт: {TOKEN_DATA['links']['website']}
            - Telegram: {TOKEN_DATA['links']['telegram']}

            Требования:
            - Заголовок: кликбейтный, с ключевыми словами
            - Длина: 200-300 слов
            - Структура: вступление, описание токенов, технологии, вывод
            - Используй эмодзи и маркированные списки
            - Язык: русский
            - В конце: ссылка на сайт и призыв к действию

            Верни в формате JSON:
            {{"title": "Заголовок", "content": "Полный текст статьи"}}
            """

            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Парсим JSON
            try:
                if result.startswith('{'):
                    data = json.loads(result)
                    return data.get('title'), data.get('content')
                else:
                    lines = result.split('\n')
                    title = lines[0].strip('# ').strip()
                    content = '\n'.join(lines[1:])
                    return title, content
            except:
                lines = result.split('\n')
                title = lines[0].strip('# ').strip()
                content = '\n'.join(lines[1:])
                return title, content

        except Exception as e:
            print(f"⚠️ Ошибка Gemini: {e}")
            return None, None

# ============================================
# ПОСТЕР НА TELEGRAPH
# ============================================
class TelegraphPoster:
    def __init__(self):
        self.stats = {"articles": 0, "failed": 0}
    
    def post_to_telegraph(self, title, content):
        """Публикует статью на Telegra.ph"""
        try:
            url = "https://api.telegra.ph/createPage"
            
            # Форматируем контент для Telegraph (HTML)
            content_html = content.replace('\n', '<br>')
            
            # Добавляем ссылку на сайт в конце
            content_html += f'<br><br>🌐 <a href="{TOKEN_DATA["links"]["website"]}">{TOKEN_DATA["links"]["website"]}</a><br>📱 <a href="{TOKEN_DATA["links"]["telegram"]}">{TOKEN_DATA["links"]["telegram"]}</a>'
            
            data = {
                "title": title,
                "content": content_html,
                "author_name": "One•Two•Three",
                "author_url": TOKEN_DATA["links"]["website"]
            }
            
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                article_url = result['result']['url']
                print(f"✅ Telegra.ph — статья опубликована: {article_url}")
                self.stats["articles"] += 1
                return article_url
            else:
                print(f"⚠️ Ошибка Telegra.ph: {result}")
                self.stats["failed"] += 1
                return None
                
        except Exception as e:
            print(f"⚠️ Ошибка Telegra.ph: {e}")
            self.stats["failed"] += 1
            return None

# ============================================
# ПОСТЕР НА BINANCE SQUARE
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
        """Генерирует пост для Binance Square"""
        # Посты на английском
        en_posts = [
            f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — the first progressive fintech ecosystem on Solana!

Three tokens. Three currencies. Three price levels. One wallet.

· $ONE — micro-entry — {TOKEN_DATA['prices']['ONE']}
· €TWO — daily spending — {TOKEN_DATA['prices']['TWO']}
· £THREE — large micro-payments — {TOKEN_DATA['prices']['THREE']}

🔹 Tech: Solana (instant txs, fee < $0.001)
🔹 Liquidity: Meteora DAMM V2
🔹 Security: Audited, LP locked 365 days

🌐 Website: {TOKEN_DATA['links']['website']}
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments""",

            f"""💎 One•Two•Three — the smartest payment system on Solana!

· $ONE ({TOKEN_DATA['prices']['ONE']}) — for everyday micro-tips
· €TWO ({TOKEN_DATA['prices']['TWO']}) — for daily purchases
· £THREE ({TOKEN_DATA['prices']['THREE']}) — for premium services

⚡ 65,000 TPS | Fee < $0.001
🔒 Audited | LP locked 365 days

🚀 Start using today: {TOKEN_DATA['links']['website']}
💬 Join community: @onetwothree

#ONE #TWO #THREE #Solana #Payments #Crypto #Web3"""
        ]
        
        # Посты на китайском
        zh_posts = [
            f"""🚀 One•Two•Three ($ONE, €TWO, £THREE) — Solana 上首个金融科技生态系统！

三种代币。三种货币。三个价格层级。一个钱包。

· $ONE — 微支付入口 — {TOKEN_DATA['prices']['ONE']}
· €TWO — 日常消费 — {TOKEN_DATA['prices']['TWO']}
· £THREE — 大额微支付 — {TOKEN_DATA['prices']['THREE']}

🔹 技术: Solana (即时交易, 手续费 < $0.001)
🔹 流动性: Meteora DAMM V2
🔹 安全: 审计, LP锁定365天

🌐 网站: {TOKEN_DATA['links']['website']}
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #加密货币 #DeFi #微支付""",

            f"""💎 One•Two•Three — Solana 上最智能的支付系统！

· $ONE ({TOKEN_DATA['prices']['ONE']}) — 日常微支付
· €TWO ({TOKEN_DATA['prices']['TWO']}) — 日常消费
· £THREE ({TOKEN_DATA['prices']['THREE']}) — 高级服务支付

⚡ 65,000 TPS | 手续费 < $0.001
🔒 已审计 | LP锁定365天

🚀 立即使用: {TOKEN_DATA['links']['website']}
💬 加入社区: @onetwothree

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
            
            headers = {
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "topic": "cryptocurrency",
                "lang": lang,
                "tags": ["ONE", "TWO", "THREE", "Solana", "DeFi"]
            }
            
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
    
    def post_to_telegram(self, text, lang="en"):
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        if not bot_token or not chat_id:
            return False
        
        try:
            label = {"en": "🇬🇧", "zh": "🇨🇳"}.get(lang, "🌍")
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": f"{label}\n\n{text}", "parse_mode": "Markdown"},
                timeout=30
            )
            if response.status_code == 200:
                print(f"✅ Telegram ({lang}) — отправлен!")
                return True
            return False
        except Exception as e:
            print(f"⚠️ Ошибка Telegram: {e}")
            return False
    
    def send_report(self):
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT")
        if bot_token and chat_id:
            try:
                text = f"""
📊 **One•Two•Three | Отчет расклейки**

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
    
    def run(self, posts_per_lang=3):
        """Запуск Binance Square"""
        print("📢 Постим в Binance Square...")
        
        for i in range(posts_per_lang):
            # Пост на английском
            text_en = self.generate_post("en")
            self.post_to_binance_square(text_en, "en")
            self.post_to_telegram(text_en, "en")
            
            # Пауза 5 минут между постами
            if i < posts_per_lang - 1:
                time.sleep(300)
            
            # Пост на китайском
            text_zh = self.generate_post("zh")
            self.post_to_binance_square(text_zh, "zh")
            self.post_to_telegram(text_zh, "zh")
            
            if i < posts_per_lang - 1:
                wait_time = random.randint(3600, 7200)  # 1-2 часа
                wait_hours = wait_time // 3600
                wait_minutes = (wait_time % 3600) // 60
                print(f"  💤 Ждем {wait_hours} часов {wait_minutes} минут...")
                time.sleep(wait_time)
        
        self.save_stats()

# ============================================
# ОСНОВНОЙ БОТ
# ============================================
class MainBot:
    def __init__(self):
        self.binance = BinanceSquarePoster()
        self.telegraph = TelegraphPoster()
        self.article_gen = ArticleGenerator()
    
    def run(self):
        print("🚀 One•Two•Three Расклейщик запущен!")
        print("🌐 Площадки: Binance Square + Telegra.ph + Telegram")
        print("=" * 60)
        
        # 1. Генерируем и публикуем статью в Telegraph
        print("\n📝 Генерируем SEO-статью через Gemini...")
        title, content = self.article_gen.generate_article()
        
        if title and content:
            print(f"📌 Заголовок: {title}")
            print(f"📄 Контент: {len(content)} символов")
            
            # Публикуем в Telegraph
            article_url = self.telegraph.post_to_telegraph(title, content)
            
            if article_url:
                # Отправляем ссылку в Telegram
                self.binance.post_to_telegram(
                    f"📝 **Новая статья про One•Two•Three**\n\n{title}\n\n🔗 Читать: {article_url}",
                    lang="ru"
                )
                print(f"✅ Статья опубликована: {article_url}")
            else:
                print("⚠️ Не удалось опубликовать статью")
        else:
            print("⚠️ Не удалось сгенерировать статью")
        
        # 2. Постим в Binance Square
        print("\n📢 Постим в Binance Square...")
        self.binance.run(posts_per_lang=3)
        
        # 3. Отчет
        self.binance.send_report()
        
        print("\n✅ Все циклы завершены!")

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    bot = MainBot()
    bot.run()
