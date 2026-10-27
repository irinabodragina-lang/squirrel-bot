import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

TOKEN = '8949226817:AAHe6qwcBQj1xXRqnaVFu4TUREhcu7tFtLM'
ADMIN_ID = 348348443
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_dict = {
  "type": "service_account",
  "project_id": "squirrelbot-512912",
  "private_key_id": "0556d9fbe5203ca9c61907206f96d0ff50daeb60",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCtKytJLWpAVSgw\nl73gY7CLOFLhH9JYaEZFlZurqQ/B+6C5/NERlALtbNw6xp0kQpDtq4GT6OyU/APU\npknty+2Vf8XznS6nSyA/XSU7lHmzs/6G/6UXUBnfQAk8W8D7REU26Bs1uuXSeE9O\nbw+no2bhAzFOED5WBfeMWBuyZvn0opvR03PvzgElmEz8Ej25boGP2Qi/J2eEsWq5\n23rwKydwlWdJwt3VWLL2j/ehYRZWeKmmE+qrxkOwDwzzXg7bZFILED8s1Ffe3VmO\nJ9W+GuDxjKLryFF/7Wnj5dU1tMaBIlj4YCP2J/XufggA9vwmTSF4ChDxHCGlrNVT\nypDV44+NAgMBAAECggEACg0jag/0xt8qggeMweWHbc1LIj4Sm4cR7SAN9RzPCVdt\nsN331KlesiFLdy3oGR60AtedodQ3Rz6JimJMkDzyAWd1Ofq5poQ5zvO9IYQwvDmK\nYJOeJYhEuCyjXJmGzg7cZZ97VNcQV/Mbx1Wy9uwJIK5qwjk3JQ8bm03R7b0EbSqa\nmtbg6s1Ky5ogRWTXCieErbIZRmSSQkULfP3TJSofPHP7k42mtC1U7BqY60Ps2IyH\nSDYdmBj+a4RFG7ctGPOAZcu59F1KSE8/b8+FPtW+Ws7iFmyXTtC55cF1U2l7cVU3\nBdKttAvXtpmoqCt1qjDs+hjcKez+mkut3cWAvpIZgQKBgQDgYQ7zNI8JLc5ON8aN\nATlUoAzZ6LxmVw7uvWXR/G3zF+hWCugbv7dwAwA5hDF1xi5+Dy60oOhBKqawwvb8\nOrIOWB5AmMZmbpDWvhiexKSBBynOo4BKCLg3LbNcW/vvT5MJN40HxR6gaDwzU5LQ\nn6E2OEPzVbJVLr4befvW00z0qQKBgQDFkpXzBjOOHa7QxH12Go8p5NfT0XLEa1N+\nRZdMsBZHjgc+gC9mtLgRl8zHrfQg732Y1LcO3GRvgkP6NGvdDN7b+TIUG4IOImZe\nzfngrM+qcbSaUYXTjUd0fw52XoNZStHHEbyHry7EiSA7Yoxs1AYnWCWGrEtYON18\npaCGlv1uRQKBgQC3+53wmkY29pJV3LI36KsD0wD2pTnmiLg71p1o452cWRwvgV31\ncuyNMki64MRVmB2DTBu2DMKkvL5V7mfrRo296U9VFHCKiVrGWrWBaiihjCghwjtt\neVzkEdsifmJERnGAe0Zu+pk0WoQSahLWci4UcWp2WuyRoHRNv2ZbLoPJkQKBgDeP\nd3e2YL0wf77Z4uZZpbUEU+WPWxT9kadK7rd0NW+98y+SYMIjRDg+Vio5MxQoBUv7\nVddqBxyMp40vPL4XJnz54SliavqKlftHNWQHdQbbnwxerKHHczbBnFGRVqK/taqj\nxD7r9tzyKwxINHFOVsStty/eN/oBU9f/w9rVj0N5AoGABW3G2/GC9iDsmD06B6wO\n2z8tnvtc+gxAvdnRIhqkQaqXYOCcI7F6y1QiVIgdjX3AYsgosndXhQBMMSDmshH2\nO7W0PhRfDX4xhqZia4xK0aAwLlP51fLB6w1seTLeDhZt1xFLS3yjnEZX0pkwo5sb\nNGAukTUnxdx1o4ZJKwTWVGk=\n-----END PRIVATE KEY-----\n",
  "client_email": "bot-writer@squirrelbot-512912.iam.gserviceaccount.com",
  "client_id": "112138783942439888011",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-writer%40squirrelbot-512912.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("База белок").sheet1

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
