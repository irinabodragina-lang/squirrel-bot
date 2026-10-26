import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
import os

TOKEN = '8949226817:AAHe6qwcBQj1xXRqnaVFu4TUREhcu7tFtLM'
ADMIN_ID = 348348443 

logging.basicConfig(level=logging.INFO)
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
        await bot.send_message(ADMIN_ID, f'Новая заявка от @{message.from_user.username}!\nТекст: {message.caption or message.text or "Нет текста"}')
        if message.photo:
            await bot.send_photo(ADMIN_ID, photo=message.photo[-1].file_id, caption='Фото белки')
        if message.location:
            await bot.send_location(ADMIN_ID, latitude=message.location.latitude, longitude=message.location.longitude)
        await message.answer('Спасибо! Я получил информацию и скоро проверю её. 💚')
    except Exception as e:
        await message.answer('Ой, произошла ошибка. Попробуйте позже.')

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 8080)))
    await site.start()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
