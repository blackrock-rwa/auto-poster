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
# ГЕНЕРАТОР ПОСТОВ (только EN + ZH)
# ============================================
class PostGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.use_ai = bool(api_key)
        if self.use_ai:
            self.client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
        else:
            self.client = None
    
    def generate_posts(self, count=5):
        """Генерирует посты на английском и китайском"""
        
        # Базовые посты на английском
        english_posts = [
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
        
        # Базовые посты на китайском
        chinese_posts = [
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
        
        # Если есть Groq AI — генерируем дополнительные уникальные посты
        if self.use_ai and self.client:
            try:
                # Генерация на английском
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "system",
                        "content": "You are a crypto marketer. Generate 2 unique promotional posts for One•Two•Three tokens on Solana. Each post 100-200 words. Include prices, features, and call to action. Use emojis and hashtags."
                    }, {
                        "role": "user",
                        "content": f"Token: One•Two•Three ($ONE, €TWO, £THREE). Prices: $ONE={TOKEN_DATA['prices']['ONE']}, €TWO={TOKEN_DATA['prices']['TWO']}, £THREE={TOKEN_DATA['prices']['THREE']}. Website: {TOKEN_DATA['links']['website']}"
                    }],
                    temperature=0.9,
                    max_tokens=500
                )
                ai_eng = response.choices[0].message.content.split('\n\n')
                english_posts.extend(ai_eng[:2])
                print("✅ AI сгенерировал посты на английском")
                
                # Генерация на китайском
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "system",
                        "content": "You are a crypto marketer. Generate 2 unique promotional posts for One•Two•Three tokens on Solana in Chinese (Simplified). Each post 100-200 words. Use emojis and hashtags."
                    }, {
                        "role": "user",
                        "content": f"Token: One•Two•Three ($ONE, €TWO, £THREE). Prices: $ONE={TOKEN_DATA['prices']['ONE']}, €TWO={TOKEN_DATA['prices']['TWO']}, £THREE={TOKEN_DATA['prices']['THREE']}. Website: {TOKEN_DATA['links']['website']}"
                    }],
                    temperature=0.9,
                    max_tokens=500
                )
                ai_zh = response.choices[0].message.content.split('\n\n')
                chinese_posts.extend(ai_zh[:2])
                print("✅ AI сгенерировал посты на китайском")
                
            except Exception as e:
                print(f"⚠️ Ошибка AI: {e}")
        
        # Перемешиваем и возвращаем
        all_posts = []
        for post in english_posts[:count]:
            all_posts.append({"lang": "en", "text": post})
        for post in chinese_posts[:count]:
            all_posts.append({"lang": "zh", "text": post})
        
        random.shuffle(all_posts)
        return all_posts

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
    
    def post_to_binance_square(self, text, lang="en"):
        """Публикация поста в Binance Square через API"""
        if not self.api_key:
            print("⚠️ BINANCE_SQUARE_API_KEY не найден!")
            return False
        
        try:
            # Binance Square API endpoint (по документации)
            url = "https://api.binance.com/sapi/v1/square/post"
            
            headers = {
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            # Данные поста
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
        """Отправка в Telegram (как отчет)"""
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
    
    def run(self, posts_count=5):
        """Запуск"""
        print("🚀 Binance Square + Telegram расклейщик запущен!")
        print(f"🌐 Языки: English 🇬🇧 + 中文 🇨🇳")
        print(f"📊 Постов за цикл: {posts_count} на каждом языке")
        print(f"⏰ Пауза: 1-2 часа")
        print("=" * 60)
        
        generator = PostGenerator()
        posts = generator.generate_posts(posts_count)
        
        for i, post_data in enumerate(posts):
            lang_name = {"en": "English 🇬🇧", "zh": "中文 🇨🇳"}[post_data["lang"]]
            print(f"\n📝 Пост {i+1}/{len(posts)} ({lang_name})")
            print(f"  📌 {post_data['text'][:80]}...")
            
            # Публикуем в Binance Square
            self.post_to_binance_square(post_data["text"], post_data["lang"])
            
            # Дублируем в Telegram
            self.post_to_telegram(post_data["text"], post_data["lang"])
            
            # ⏰ ПАУЗА 1-2 ЧАСА
            if i < len(posts) - 1:
                wait_time = random.randint(3600, 7200)  # 1-2 часа
                wait_hours = wait_time // 3600
                wait_minutes = (wait_time % 3600) // 60
                print(f"  💤 Ждем {wait_hours} часов {wait_minutes} минут...")
                time.sleep(wait_time)
        
        self.save_stats()
        self.send_report()
        print("\n✅ Все циклы завершены!")

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    poster = BinanceSquarePoster()
    poster.run(posts_count=3)
