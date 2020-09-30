# Import

from pymongo import MongoClient

from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext

from echo.config import TG_TOKEN
from echo.config import MONGODB_LINK
from echo.config import MONGO_DB

# -------------------------------
# Bot Logic
# -------------------------------

mondb = MongoClient(MONGODB_LINK)[MONGO_DB]

contact_keyboard = KeyboardButton('Войти', request_contact=True)
custom_keyboard_login = [[contact_keyboard]]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(custom_keyboard_login, resize_keyboard=True)


def on_start(update: Update, context: CallbackContext):
    message = update.message
    user = mondb.users.find_one({"user_id": str(message.chat.id)})
    if not user:
        message.reply_text(
            'Добро пожаловать в Хаб!  Вы не авторизованный пользователь. Пожалуйста войдите в систему!',
            reply_markup=REPLY_KEYBOARD_MARKUP
        )
    else:
        message.reply_text(
            'Добро пожаловать в Хаб!'
        )


def on_contact(update: Update, context: CallbackContext):
    message = update.message
    user_phone_number = ''
    user_chat_id = ''
    if message.contact:
        user_phone_number += str(message.contact['phone_number'])
        user_chat_id += str(message.contact['user_id'])

    user = login_user(mondb, user_chat_id, user_phone_number)
    if not user:
        message.reply_text(
            'Ошибка! Указанный пользователь не найден. Если вы заполнили анкету на сайте www.thehub.su более чем 1 неделю назад, пожалуйста обратитесь к службе поддержки: @HUBsup',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        message.reply_text(
            'Вы успешно авторизированы!',
            reply_markup=ReplyKeyboardRemove()
        )

def login_user(mondb, user_id, user_phone_number):
    user = mondb.users.find_one({"user_phone": user_phone_number})
    if user:
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'user_id': user_id}}
        )
        return user
    if not user:
        return None


def main():
    updater = Updater(
        token=TG_TOKEN,
        use_context=True
    )

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', on_start))
    # dp.add_handler(MessageHandler(Filters.text, on_request))
    dp.add_handler(MessageHandler(Filters.contact, on_contact))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
