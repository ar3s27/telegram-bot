import requests
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

# Telegram bot token
bot_token = '6977354306:AAG8iefJfhMyAAL_JymxuCY-tbiSW1FAnb8'

# Sitenin API'si veya veri kaynağı URL'si
earthquake_data_url = 'https://deprem-gorsellestirme.vercel.app'

# Bot oluşturma
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# /start komutuna yanıt olarak başlangıç mesajı gönder
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Bot çalışıyor. /sondepremler komutunu kullanarak son deprem bilgilerini alabilirsiniz.")

# /sondepremler komutuna yanıt olarak son depremleri gönder
@dp.message_handler(commands=['sondepremler'])
async def sondepremler(message: types.Message):
    response = requests.get(earthquake_data_url)
    if response.status_code == 200:
        data = response.json()
        earthquake_info = "Türkiyede Olan Son 10 Deprem:\n\n"
        for quake_id, quake_data in data.items():
            earthquake_info += f"Deprem ID: {quake_data['quake_id']}\n"
            earthquake_info += f"Konum: {quake_data['location']}\n"
            earthquake_info += f"Enlem: {quake_data['latitude']}\n"
            earthquake_info += f"Boylam: {quake_data['longitude']}\n"
            earthquake_info += f"Derinlik: {quake_data['depth']} km\n"
            earthquake_info += f"Büyüklük: {quake_data['magnitude']}\n"
            earthquake_info += f"Tarih: {quake_data['date']}\n\n"

        await message.answer(earthquake_info, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("Deprem verilerine erişilemedi.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)