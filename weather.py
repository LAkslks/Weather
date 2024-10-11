import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command


TOKEN = '7897107338:AAHgUpNXW_c3nByTTg1FOb3Gd5vMUvlaR7o'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Привет! Чтобы получить погоду, пришлите название города:')

@dp.message(F.text)
async def get_weather(message: types.Message):
    city = message.text
    API_key='28fa51ea5574f794fa9f0e36146efb9b'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                    response.raise_for_status()  
                    weather_data = await response.json()
                    
                    temperature = weather_data["main"]["temp"]
                    feels_like = weather_data["main"]["feels_like"]
                    description = weather_data["weather"][0]["description"]
                    wind_speed = weather_data["wind"]["speed"]
                    humidity = weather_data["main"]["humidity"]

                    response_message = (
                        f"Погода в {city}:\n"
                        f"Температура: {temperature}°C\n"
                        f"Ощущается как: {feels_like}°C\n"
                        f"Описание: {description}\n"
                        f"Скорость ветра: {wind_speed} м/с\n"
                        f"Влажность: {humidity}%\n"
                    )
              
            await message.answer(response_message)
    except Exception as e:
        await message.answer(f'Не удалось определить город: {city}')
        print(f'Ошибка {e}')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())