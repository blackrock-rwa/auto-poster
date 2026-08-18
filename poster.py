import os
import time
import random
import json
import requests
from openai import OpenAI

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
# ГЕНЕРАТОР ПОСТОВ
# ============================================
class PostGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.use_ai = bool(api_key)
        if self.use_ai:
            self.client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
        else:
            self.client = None
    
    def generate_posts(self):
        """Генерирует посты на русском, английском и китайском"""
        
        # Базовые посты (русский)
        russian_posts = [
            f"""One•Two•Three ($ONE, €TWO, £THREE) — первая прогрессивная финтех-экосистема на Solana.

Три токена. Три валюты. Три ценовых уровня. Один кошелёк.

· $ONE — микро-вход (доступный каждому) — {TOKEN_DATA['prices']['ONE']}
· €TWO — средний чек (ежедневные траты) — {TOKEN_DATA['prices']['TWO']}
· £THREE — крупные микро-платежи — {TOKEN_DATA['prices']['THREE']}

🔹 Технологии: Solana (мгновенные транзакции, комиссия < $0.001)
🔹 Ликвидность: Meteora DAMM V2
🔹 Безопасность: Аудит, блокировка ликвидности на 365 дней

Сайт: {TOKEN_DATA['links']['website']}
TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments""",

            f"""One•Two•Three — инвестиционная логика на Solana!

📊 Эмиссия:
· $ONE: 9,000,000,000,000,000 ({TOKEN_DATA['prices']['ONE']})
· €TWO: 999,000,000,000,000 ({TOKEN_DATA['prices']['TWO']})
· £THREE: 99,000,000,000,000 ({TOKEN_DATA['prices']['THREE']})

💰 Ценовая лестница: 1¢ → 5¢ → 10¢

🔐 Безопасность: Mint Authority отключён, LP заблокирована на 365 дней
⚡ Solana: 65 000 TPS, комиссия < $0.001

#ONE #TWO #THREE #Solana #DeFi #CryptoInvesting""",

            f"""🚀 Токены One•Two•Three уже на Meteora!

$ONE (${TOKEN_DATA['prices']['ONE']}) — микро-вход
€TWO ({TOKEN_DATA['prices']['TWO']}) — ежедневные траты  
£THREE ({TOKEN_DATA['prices']['THREE']}) — крупные платежи

✅ Мгновенные транзакции на Solana
✅ Комиссия < $0.001
✅ Ликвидность заблокирована

🔗 Сайт: {TOKEN_DATA['links']['website']}
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Web3 #CryptoNews"""
        ]
        
        # Посты на английском
        english_posts = [
            f"""One•Two•Three ($ONE, €TWO, £THREE) — the first progressive fintech ecosystem on Solana.

Three tokens. Three currencies. Three price levels. One wallet.

· $ONE — micro-entry (for everyone) — {TOKEN_DATA['prices']['ONE']}
· €TWO — medium check (daily spending) — {TOKEN_DATA['prices']['TWO']}
· £THREE — large micro-payments — {TOKEN_DATA['prices']['THREE']}

🔹 Tech: Solana (instant txs, fee < $0.001)
🔹 Liquidity: Meteora DAMM V2
🔹 Security: Audited, LP locked 365 days

Website: {TOKEN_DATA['links']['website']}
TG: @onetwothree

#ONE #TWO #THREE #Solana #Crypto #DeFi #MicroPayments""",

            f"""🚀 One•Two•Three tokens are LIVE on Meteora!

$ONE ({TOKEN_DATA['prices']['ONE']}) — micro-entry
€TWO ({TOKEN_DATA['prices']['TWO']}) — daily spending
£THREE ({TOKEN_DATA['prices']['THREE']}) — large payments

✅ Instant txs on Solana
✅ Fee < $0.001
✅ LP locked 365 days

🔗 Website: {TOKEN_DATA['links']['website']}
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Web3 #DeFi #Crypto"""
        ]
        
        # Посты на китайском
        chinese_posts = [
            f"""One•Two•Three ($ONE, €TWO, £THREE) — Solana 上首个渐进式金融科技生态系统。

三种代币。三种货币。三个价格层级。一个钱包。

· $ONE — 微支付入口 {TOKEN_DATA['prices']['ONE']}
· €TWO — 日常消费 {TOKEN_DATA['prices']['TWO']}
· £THREE — 大额微支付 {TOKEN_DATA['prices']['THREE']}

🔹 技术: Solana (即时交易, 手续费 < $0.001)
🔹 流动性: Meteora DAMM V2
🔹 安全: 审计, LP锁定365天

网站: {TOKEN_DATA['links']['website']}
TG: @onetwothree

#ONE #TWO #THREE #Solana #加密货币 #DeFi #微支付""",

            f"""🚀 One•Two•Three 代币已在 Meteora 上线！

$ONE ({TOKEN_DATA['prices']['ONE']}) — 微支付入口
€TWO ({TOKEN_DATA['prices']['TWO']}) — 日常消费
£THREE ({TOKEN_DATA['prices']['THREE']}) — 大额支付

✅ Solana 即时交易
✅ 手续费 < $0.001
✅ LP锁定365天

🔗 网站: {TOKEN_DATA['links']['website']}
📱 TG: @onetwothree

#ONE #TWO #THREE #Solana #Web3 #DeFi #加密货币"""
        ]
        
        # Если есть AI — делаем уникальные посты
        if self.use_ai and self.client:
            try:
                # Генерируем уникальные посты на английском
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "system",
                        "content": "You are a crypto marketer. Generate 3 unique promotional posts for One•Two•Three tokens on Solana. Each post 100-200 words. Include prices, features, and call to action."
                    }, {
                        "role": "user",
                        "content": f"Token: One•Two•Three ($ONE, €TWO, £THREE). Prices: $ONE={TOKEN_DATA['prices']['ONE']}, €TWO={TOKEN_DATA['prices']['TWO']}, £THREE={TOKEN_DATA['prices']['THREE']}. Website: {TOKEN_DATA['links']['website']}"
                    }],
                    temperature=0.9,
                    max_tokens=600
                )
                ai_eng = response.choices[0].message.content.split('\n\n')
                english_posts.extend(ai_eng[:2])
                print("✅ AI сгенерировал дополнительные посты на английском")
            except Exception as e:
                print(f"⚠️ Ошибка AI: {e}")
        
        return {"ru": russian_posts, "en": english_posts, "zh": chinese_posts}

# ============================================
# ПОСТЕР НА ПЛОЩАДКИ (Telegram, Twitter, Discord)
# ============================================
class InternationalPoster:
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
    
    def post_to_telegram(self, text):
        """Отправка в Telegram"""
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
            if response.status_code == 200:
                print("✅ Telegram — отправлено!")
                self.stats["posted"] += 1
                self.stats["platforms"]["telegram"] = self.stats["platforms"].get("telegram", 0) + 1
                return True
            return False
        except Exception as e:
            print(f"⚠️ Ошибка Telegram: {e}")
            return False
    
    def post_to_twitter(self, text):
        """Отправка в Twitter/X через API"""
        try:
            import tweepy
            
            api_key = os.getenv("TWITTER_API_KEY")
            api_secret = os.getenv("TWITTER_API_SECRET")
            access_token = os.getenv("TWITTER_ACCESS_TOKEN")
            access_secret = os.getenv("TWITTER_ACCESS_SECRET")
            
            if not all([api_key, api_secret, access_token, access_secret]):
                print("⚠️ Twitter не настроен (нет ключей)")
                return False
            
            # Twitter API v2
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_secret
            )
            
            # Обрезаем до 280 символов
            tweet_text = text[:277] + "..." if len(text) > 280 else text
            client.create_tweet(text=tweet_text)
            print("✅ Twitter — опубликовано!")
            self.stats["posted"] += 1
            self.stats["platforms"]["twitter"] = self.stats["platforms"].get("twitter", 0) + 1
            return True
            
        except Exception as e:
            print(f"⚠️ Ошибка Twitter: {e}")
            return False
    
    def post_to_discord(self, text):
        """Отправка в Discord через Webhook"""
        webhook_url = os.getenv("DISCORD_WEBHOOK")
        if not webhook_url:
            return False
        
        try:
            # Discord лимит 2000 символов
            discord_text = text[:1900] + "..." if len(text) > 2000 else text
            response = requests.post(webhook_url, json={"content": discord_text}, timeout=30)
            if response.status_code == 204:
                print("✅ Discord — отправлено!")
                self.stats["posted"] += 1
                self.stats["platforms"]["discord"] = self.stats["platforms"].get("discord", 0) + 1
                return True
            return False
        except Exception as e:
            print(f"⚠️ Ошибка Discord: {e}")
            return False
    
    def send_report(self):
        """Отчет в Telegram"""
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
    
    def run(self):
        print("🚀 Международный расклейщик One•Two•Three запущен!")
        print("🌍 Площадки: Telegram, Twitter, Discord")
        print("🌐 Языки: Русский, English, 中文")
        print("=" * 60)
        
        generator = PostGenerator()
        posts = generator.generate_posts()
        
        for lang, texts in posts.items():
            lang_name = {"ru": "Русский", "en": "English", "zh": "中文"}[lang]
            print(f"\n📝 Язык: {lang_name} — {len(texts)} постов")
            
            for i, text in enumerate(texts):
                print(f"\n  Пост {i+1}/{len(texts)}")
                print(f"  📌 {text[:80]}...")
                
                # Отправляем на все площадки
                self.post_to_telegram(text)
                self.post_to_twitter(text)
                self.post_to_discord(text)
                
                if i < len(texts) - 1:
                    wait_time = random.randint(60, 180)
                    print(f"  💤 Ждем {wait_time} секунд...")
                    time.sleep(wait_time)
        
        self.save_stats()
        self.send_report()
        print("\n✅ Все циклы завершены!")

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    poster = InternationalPoster()
    poster.run()
