import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
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

@dp.message()
async def handle_all(message: types.Message):
    try:
        try:
            photo_id = f"https://api.telegram.org/file/bot{TOKEN}/{message.photo[-1].file_id}" if message.photo else ""
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
        await message.answer('Спасибо! Я получил информацию. 💚')
    except Exception as e:
        await message.answer('Ой, ошибка. Попробуйте позже.')

async def on_startup(bot: Bot):
    webhook_url = "https://squirrel-bot-6hfi.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook установлен: {webhook_url}")

async def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()
    await on_startup(bot)
    logging.info("Сервер запущен!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
