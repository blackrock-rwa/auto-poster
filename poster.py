import os
import requests
import time

print("🚀 Бот запущен!")

# Проверяем секреты
api_key = os.getenv("GROQ_API_KEY")
tg_token = os.getenv("TELEGRAM_TOKEN")
tg_chat = os.getenv("TELEGRAM_CHAT")

print(f"🔑 GROQ_API_KEY: {'✅ Найден' if api_key else '❌ НЕ НАЙДЕН'}")
print(f"🔑 TELEGRAM_TOKEN: {'✅ Найден' if tg_token else '❌ НЕ НАЙДЕН'}")
print(f"🔑 TELEGRAM_CHAT: {'✅ Найден' if tg_chat else '❌ НЕ НАЙДЕН'}")

# Пытаемся отправить тестовое сообщение в Telegram
if tg_token and tg_chat:
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{tg_token}/sendMessage",
            json={"chat_id": tg_chat, "text": "🚀 Бот успешно запущен на GitHub Actions!"},
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Тестовое сообщение отправлено в Telegram!")
        else:
            print(f"⚠️ Ошибка Telegram: {response.text}")
    except Exception as e:
        print(f"⚠️ Ошибка отправки: {e}")
else:
    print("⚠️ Telegram не настроен, пропускаем отправку")

print("✅ Тест завершен!")
