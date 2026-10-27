import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

logging.basicConfig(level=logging.INFO)

TOKEN = '8949226817:AAHVDlIOV1yM1pusTSeRr2jQbiO3_uqpBA4'
ADMIN_ID = 348348443

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("База белок").get_worksheet(0)
    logging.info("=== УСПЕШНО ПОДКЛЮЧИЛИСЬ К ТАБЛИЦЕ! ===")
except Exception as e:
    logging.error(f"!!! ОШИБКА ПРИ ПОДКЛЮЧЕНИИ К ТАБЛИЦЕ: {e} !!!")
    raise e

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Добро пожаловать в Беличью карту. 🐿️🤍\nПришли мне фото белки и напиши адрес, где ты её видел.')

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer('Как это работает:\n1. Отправь геолокацию или напиши адрес.\n2. Прикрепи фото.\n3. Напиши пару слов о белке.\nЯ проверю и добавлю её на карту!')

@dp.message(Command('map'))
async def cmd_map(message: types.Message):
    await message.answer('Ссылка на карту: https://yandex.ru/maps/?um=constructor%3Abcb9c067dd410bbccf73bfa96bac805b7b61fa653c476d33cc59745a37ae09de&source=constructorLink')

@dp.message()
async def handle_all(message: types.Message):
    try:
        # Сохранение в Google Таблицу
        try:
            photo_id = message.photo[-1].file_id if message.photo else ""
            lat = message.location.latitude if message.location else ""
            lon = message.location.longitude if message.location else ""
            text = message.caption or message.text or "Нет текста"
            username = f"@{message.from_user.username}" if message.from_user.username else str(message.from_user.id)
            
            sheet.append_row([str(datetime.now()), username, text, photo_id, lat, lon])
        except Exception as e:
            logging.error(f"Ошибка записи в таблицу: {e}")

        await bot.send_message(ADMIN_ID, f'Новая заявка от @{message.from_user.username}!\nТекст: {message.caption or message.text or "Нет текста"}')
        
        if message.photo:
            await bot.send_photo(ADMIN_ID, photo=message.photo[-1].file_id, caption='Фото белки')
        if message.location:
            await bot.send_location(ADMIN_ID, latitude=message.location.latitude, longitude=message.location.longitude)
            
        await message.answer('Спасибо! Я получил информацию и скоро проверю её. 💚')
    except Exception as e:
        await message.answer('Ой, произошла ошибка. Попробуйте позже.')

if __name__ == "__main__":
    dp.run_polling(bot)
