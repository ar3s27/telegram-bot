import asyncio
import logging
import os

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

# Telegram bot token: BotFather'dan alınır, koda değil ortam değişkenine (sunucuda .env) yazılır.
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]

# Deprem verisinin alındığı API. Ev sunucusunda http://deprem-api:8000 olarak ayarlanır.
earthquake_data_url = os.environ.get("DEPREM_API_URL", "https://deprem-api.veyselerkoyuncu.com.tr")

# Bot oluşturma
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


def fetch_earthquakes():
    """API'den son depremleri alır; alınamazsa None döner."""
    try:
        response = requests.get(earthquake_data_url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        logging.warning("Deprem verisi alınamadı: %s", e)
        return None
    # API, AFAD'a ulaşamazsa {"error": "..."} döndürüyor.
    if not isinstance(data, dict) or "error" in data:
        return None
    return data


# /start komutuna yanıt olarak başlangıç mesajı gönder
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Bot çalışıyor. /sondepremler komutunu kullanarak son deprem bilgilerini alabilirsiniz.")


# /sondepremler komutuna yanıt olarak son depremleri gönder
@dp.message_handler(commands=['sondepremler'])
async def sondepremler(message: types.Message):
    # İstek ayrı bir iş parçacığında yapılır ki bot beklerken diğer mesajlara da yanıt verebilsin.
    data = await asyncio.to_thread(fetch_earthquakes)
    if not data:
        await message.answer("Deprem verilerine erişilemedi.")
        return

    earthquake_info = "Türkiyede Olan Son 10 Deprem:\n\n"
    for quake_data in data.values():
        earthquake_info += f"Deprem ID: {quake_data['quake_id']}\n"
        earthquake_info += f"Konum: {quake_data['location']}\n"
        earthquake_info += f"Enlem: {quake_data['latitude']}\n"
        earthquake_info += f"Boylam: {quake_data['longitude']}\n"
        earthquake_info += f"Derinlik: {quake_data['depth']} km\n"
        earthquake_info += f"Büyüklük: {quake_data['magnitude']}\n"
        earthquake_info += f"Tarih: {quake_data['date']}\n\n"

    # Düz metin: yer adlarındaki _ * gibi karakterler Markdown olarak yorumlanıp mesajı bozmasın.
    await message.answer(earthquake_info)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
