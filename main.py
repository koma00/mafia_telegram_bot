import config
import logging

from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import CommandHelp, ChatTypeFilter
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.deep_linking import get_startgroup_link
from aiogram.utils.executor import start_webhook
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ChatType


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(ChatTypeFilter([ChatType.PRIVATE, ChatType.SENDER]), commands=['start'])
async def start_bot(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    link = await get_startgroup_link('true')
    button = InlineKeyboardButton('Додати бота в чат', link)
    keyboard.add(button)
    return SendMessage(message.chat.id, 'Привіт!\nЯ 🇺🇦 бот для гри в Мафію!\nБільше інформації: /help', reply_markup=keyboard)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "Це бот для гри в Мафію і йому необхідні права адміністратора.\n"
    text += "\nПовний список доступних команд:\n"
    text += "/start - розпочати роботу з ботом\n"
    text += "/register - розпочати реєстрацію\n"
    text += "/game - завершити реєстрацію і розпочати гру\n"
    text += "/help - довідка\n"
    text += "/leave - покинути гру\n"
    return SendMessage(message.chat.id, text)


async def change_member(chat, chat_member_id):
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id

    if chat_member_id == bot_id:
        text = 'Привіт!\nЯ 🇺🇦 бот для гри в Мафію!\n'
        if chat.type in (ChatType.GROUP,ChatType.SUPERGROUP):
            bot_privs = await bot.get_chat_member(chat.id, bot_id)
            if bot_privs['status'] == 'administrator':
                if bot_privs['can_delete_messages'] and bot_privs['can_pin_messages'] and bot_privs['can_pin_messages']:
                    text += 'Для початку реєстрації, введи /register'
            if text == '':
                text += 'Для роботи боту потрібні наступні права адміністратора:\n'
                text += '- Видалення повідомлень\n'
                text += '- Обмеження інших учасників\n'
                text += '- Закріплення повідомлень'
        else:
            text += 'Бот може працювати тільки в групі\n'
            text += 'Додай бота в групу з іншими учасниками'
        return SendMessage(chat.id, text)
    return 0


@dp.my_chat_member_handler()
async def member_update(my_chat_member: types.ChatMemberUpdated):
    if my_chat_member.new_chat_member.status in ('kicked', 'left'):
        logging.info(f'Kick bot from chat_id = {my_chat_member.chat.id}')
        return 0
    return await change_member(my_chat_member.chat, my_chat_member.new_chat_member.user.id)


@dp.message_handler(content_types=['new_chat_members'])
async def new_member(message: types.Message):
    for chat_member in message.new_chat_members:
        await change_member(message.chat, chat_member.id)


@dp.message_handler()
async def echo(message: types.Message):
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    logging.info("Configure webhook...")
    await bot.delete_webhook()
    if config.WEBHOOK_USE:
        await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


def main():
    if config.WEBHOOK_USE:
        start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=config.SKIP_UPDATES,
            host=config.WEBAPP_HOST,
            port=config.WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp, skip_updates=config.SKIP_UPDATES)


if __name__ == '__main__':
    main()
