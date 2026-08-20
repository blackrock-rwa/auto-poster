import os
import requests
import time

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT")
    if token and chat:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat, "text": text, "parse_mode": "Markdown"},
                timeout=10
            )
        except Exception as e:
            print(f"Telegram error: {e}")

print("🚀 Бот запущен!")

# Проверяем секреты
token = os.getenv("TELEGRAM_TOKEN")
chat = os.getenv("TELEGRAM_CHAT")
print(f"TELEGRAM_TOKEN: {'✅' if token else '❌'}")
print(f"TELEGRAM_CHAT: {'✅' if chat else '❌'}")

# Отправляем тестовое сообщение
if token and chat:
    send_telegram("✅ **One•Two•Three бот работает!**")
    print("✅ Тестовое сообщение отправлено!")
else:
    print("❌ Ошибка: секреты не найдены")

print("✅ Готово!")
