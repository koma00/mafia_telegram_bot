import asyncio
from envparse import env
from aiogram import Bot


env.read_envfile()

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

loop = asyncio.get_event_loop()
bot = Bot(token=TELEGRAM_BOT_TOKEN, loop=loop)


async def main():
    user = await bot.me
    print(f"Bot: {user.full_name} [@{user.username}]")

if __name__ == '__main__':
    asyncio.run(main())