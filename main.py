""" Altair8 HUB Interface telegram bot ver 0.1
    Vladimir Monomakh, Kambarov Nadir
"""

# Import
from pymongo import MongoClient

import logging

from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
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
# Connect to DataBase
mondb = MongoClient(MONGODB_LINK)[MONGO_DB]

# Login Keyboard
contact_keyboard = KeyboardButton('Войти', request_contact=True)
custom_keyboard_login = [[contact_keyboard]]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(custom_keyboard_login, resize_keyboard=True)

CALLBACK_MM = "cb_mm"
CALLBACK_MM_HUB = "cb_mm_hs"
CALLBACK_MM_CHATS = "cb_mm_ch"
CALLBACK_MM_SCHLED = "cb_mm_sch"
CALLBACK_MM_TASKS = "cb_mm_ts"
CALLBACK_MM_TODO = "cb_mm_todo"
CALLBACK_MM_MUSIC = "cb_mm_mus"
CALLBACK_MM_SETTING = "cb_mm_setng"

CALLBACK_RR = "cb_rr"


def get_hubs(bool_list):
    keyboard = []
    if int(bool_list[1]):
        keyboard.append([InlineKeyboardButton("🖥    DEV.HUB", url="https://t.me/joinchat/OPPf1lTKYcszVxfih0m2jw")])
    if int(bool_list[2]):
        keyboard.append([InlineKeyboardButton("🔌   HARD.HUB", url="https://t.me/joinchat/OPPf1lh2GTulebNiu34jEw")])
    if int(bool_list[3]):
        keyboard.append([InlineKeyboardButton("🗣    SOC.HUB", url="https://t.me/joinchat/OPPf1laFJhzZ6Sx88P0YOQ")])
    if int(bool_list[4]):
        keyboard.append([InlineKeyboardButton("🔳    ART.HUB", url="https://t.me/joinchat/OPPf1leFxg4vdBbkler_Xg")])
    if int(bool_list[5]):
        keyboard.append([InlineKeyboardButton("🎮   GEEK.HUB", url="https://t.me/joinchat/OPPf1lDF0qoKXq7Wnn71eA")])
    if int(bool_list[6]):
        keyboard.append([InlineKeyboardButton("🏴‍☠   DARK.HUB️", url="https://t.me/joinchat/OPPf1ldtdd0CxeejqWUDdg")])

    keyboard.append([InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM)])
    return InlineKeyboardMarkup(keyboard)


def get_back_mm():
    keyboard = [[InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM)]]
    return InlineKeyboardMarkup(keyboard)

# Main Menu
def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🕸  Small HUBs", callback_data=CALLBACK_MM_HUB),
        ],
        [
            InlineKeyboardButton("📆 Расписание", callback_data=CALLBACK_MM_SCHLED),
            InlineKeyboardButton("📋 Задачи", callback_data=CALLBACK_MM_TASKS),
        ],
        [
            InlineKeyboardButton("🌐  Мои Чаты", callback_data=CALLBACK_MM_CHATS),
            InlineKeyboardButton("📝  TO DO", callback_data=CALLBACK_MM_TODO),
        ],
        [
            InlineKeyboardButton("🎵  Музыка Дня", callback_data=CALLBACK_MM_MUSIC),
        ],
        [
            InlineKeyboardButton("ℹ️  Дополнительно️", callback_data=CALLBACK_MM_SETTING),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_rereg_button():
    keyboard = [
        [
            InlineKeyboardButton("📲  Сменить номер", callback_data=CALLBACK_RR),
        ],
        [
            InlineKeyboardButton("Служба поддержки", url="https://t.me/HUBsup"),
        ],
        [
            InlineKeyboardButton("🔥 Наш сайт! ", url="https://www.thehub.su")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def on_start(update: Update, context: CallbackContext):
    message = update.message
    user = mondb.users.find_one({"user_id": message.chat.id})
    if not user:
        message.reply_text(
            'Добро пожаловать в Хаб!  Вы не авторизованный пользователь. Пожалуйста войдите в систему!',
            reply_markup=REPLY_KEYBOARD_MARKUP
        )
        logging.warning(message.chat.id)
    else:
        message.reply_text(
            "Основное меню: ",
            reply_markup=get_main_menu()
        )

# IF user message == contact
def on_contact(update: Update, context: CallbackContext):
    message = update.message
    user_phone_number = 0
    user_chat_id = 0
    # IF user get another Contact
    if message.chat_id == int(message.contact['user_id']):
        if message.contact:
            num1 = str(message.contact['phone_number'])
            user_phone_number = 0
            # F*CKING TELEGRAM output various number, IDK
            for i in range(-10, 0):
                user_phone_number += int(num1[i]) * (10 ** ((i + 1) * -1))
            user_chat_id += int(message.contact['user_id'])
            logging.info("User ID: " + str(message.contact['user_id']))
            logging.warning("User Phone: " + str(user_phone_number))
        user = login_user(mondb, user_chat_id, user_phone_number)
        logging.warning(user)
        if not user:
            message.reply_text(
                'Ошибка! Указанный пользователь не найден.',
                reply_markup=ReplyKeyboardRemove()
            )
            message.reply_text(
                'Возможный проблемы: \
                \n1. Если в Анкете вы указали некорректный номер можете сменить его нажав кнопку ниже. \
                \n2. Если вы заполнили анкету более чем 1 неделю назад, пожалуйста обратитесь к службе поддержки.\
                \n3. Если вы еще не заполняли анкету, самое время сделать это перейдя на наш сайт!',
                reply_markup=get_rereg_button()
            )

        else:
            message.reply_text(
                'Вы успешно авторизированы!',
                reply_markup=ReplyKeyboardRemove()
            )
            message.reply_text(
                'Вас приветсвует Altair8 - интерфейс взаимодействия с H.U.B. ver 0.1. Интересного вам времяпрепровождения!\
                 \nОсновное меню:',
                reply_markup=get_main_menu()
            )
    else:
        message.reply_text(
            'Ошибка доступа! Указанный номер не соответсвует UserID.',
            reply_markup=ReplyKeyboardRemove()
        )

# User Register
def login_user(mondb, user_id, user_phone_number):
    user = mondb.users.find_one({"user_phone": user_phone_number})
    logging.warning("user_phone: " + str(user_phone_number))
    if user != None and user.get('user_id') is None:
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'user_id': user_id}}
        )
        return user
    else:
        return None

# Command to edit phone number from DB
def do_changephone(update: Update, context: CallbackContext):
    # IF incorrect command input
    try:
        # Parcing user input
        old_phone_number = int(update.message.text[13:23])
        user_new_phone_number = int(update.message.text[26:36])
        user_name = update.message.text[37:]
        user = mondb.users.find_one({"user_phone": old_phone_number})
    except:
        user = None
        user_name = ''

    if not user:
        update.message.reply_text(
            'Ошибка! Указаный номер не найден!',
        )
    elif user.get('user_id') is None and user.get("user_name") == user_name:
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'user_phone': user_new_phone_number,
                      'user_id': update.message.chat_id
                      }}
        )
        update.message.reply_text(
            'Номер успешно изменен! Перезапустите бота /start',
        )
    else:
        update.message.reply_text(
            'Ошибка! Не соответсвие данных!',
        )
# Sticker Time! Dont Touch!
#
# def handle_docs_audio(update: Update, context: CallbackContext):
#     # Получим ID Стикера
#     sticker_id = update.message.sticker.file_id
#     logging.warning(sticker_id)

# Command to event new day to small HUB Schledule
def do_addevent(update: Update, context: CallbackContext):
    text = update.message.text
    user = mondb.users.find_one({"user_id": update.message.chat_id})
    user_lead = int(user.get("user_hubs")/1000000)
    if user_lead == 1:
        update.message.reply_text(
            'Только Лид может изменять расписание!',
        )
    else:
        # Slot choice
        # TODO Edit this command, automatic slot choice
        if text[10] == '1':
            mondb.allschledule.update_one(
                {'hub_id': user_lead-1},
                {'$set': {'event1': text[12:]}}
            )
        if text[10] == '2':
            mondb.allschledule.update_one(
                {'hub_id': user_lead-1},
                {'$set': {'event2': text[12:]}}
            )
        if text[10] == '3':
            mondb.allschledule.update_one(
                {'hub_id': user_lead-1},
                {'$set': {'event3': text[12:]}}
            )

# Telegram inline menu buttons handler
def keyboard_call_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data == CALLBACK_MM:
        query.edit_message_text(
            text="Основное меню: ",
            reply_markup=get_main_menu()
        )
    elif data == CALLBACK_MM_HUB:
        user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
        query.edit_message_text(
            text="Ваши активные Хабы: ",
            reply_markup=get_hubs(str(user.get("user_hubs")))
        )
        # TODO Inline music add
    elif data == CALLBACK_MM_MUSIC:
        chatid = update.effective_message.chat_id
        query.edit_message_text(
            text="Музыка дня, для души и работы от участников Хаба. Сегодня в честь запуска музыка от @MON0makh\
         \nЗаказать плейлист можно у @MON0makh 🎧",
        )
        # TODO Local audio need
        context.bot.send_sticker(chatid, 'CAACAgEAAxkBAAIDMV92U2Sk4DVLErXtBFPWgQhfmqh1AAJhAAPArAgjT8wG8ZJFRc0bBA')
        for i in range(1, 2):
            context.bot.send_audio(
                chat_id=chatid,
                audio='https://cdndl.zaycev.net/track/1824177/4Ehsii9FgoD6ZoprRLM9h3rm2gX5qEZ9SjYWXSxJqLHXr3rmeJSPaWwMoYF2V1iKUW9H4UEmyfd6aMNSXbtSKJjQpUuucgvW5s6kfvqauwLRyBkrGm1ktbB78DDtQUF3vDbnWZBdJhU91rCtpz8pSJcxtM5E7Cd7x2cE1UL6ia5xJJVwVPwyuFnBzA2XiVmWTYkX3DsGLUGxiPHEQ4ehtrvSiprexHRwnHp5uvbm2S5VzZPiMP2CJSB5o1n5GFAqSLpT1bjS8VmW49Vhnya1FZBx3VXH5soVsf2QzddYkHNaFyBmpfdgRCz9Z4JbscxiVZ9izQNuFYCDhpJ5H1vMFTVmR6Ag3TUu3dsjXMFJB5CrfdCKSw1L',
            )
        context.bot.send_message(
            chat_id=chatid,
            text="Основное меню",
            reply_markup=get_main_menu(),
        )
    elif data == CALLBACK_MM_SCHLED:
        chatid = update.effective_message.chat_id
        user = mondb.users.find_one({"user_id": update.message.chat_id})
        # TODO add BIGHUB Schledule
        for i in range(1, 7):
            if str(user.get("user_hubs"))[i]:
                table = mondb.allschledule.find_one({"hub_id": i})
                if table != None:
                    text = table.get('hub_name') + ": "
                    if table.get('event1') != None:
                        text += "\n" + table.get('event1')
                    if table.get('event2') != None:
                        text += "\n" + table.get('event2')
                    if table.get('event3') != None:
                        text += "\n" + table.get('event3')

                    # IF schledule empty
                    if len(text) > 10:
                        context.bot.send_message(
                            chat_id=chatid,
                            text="{}".format(text),
                        )
                    else:
                        context.bot.send_message(
                            chat_id=chatid,
                            text="{}".format(text + "Пока ничего..."),
                        )

    elif data == CALLBACK_MM_SETTING:
        query.edit_message_text(
            text="Altair8 все еще находится в разработке, на данный момент эта функция не доступна, но скоро мы это испраим.\
            \nНадеемся на ваше понимание! Если вы обнаружили какие либо баги в работе системы Altair8, пожалуйста сообщите нам: @HUBsup",
            reply_markup=get_back_mm()
        )
    elif data == CALLBACK_MM_TASKS:
        query.edit_message_text(
            text="Altair8 все еще находится в разработке, на данный момент эта функция не доступна, но скоро мы это испраим.\
            \nНадеемся на ваше понимание! Если вы обнаружили какие либо баги в работе системы Altair8, пожалуйста сообщите нам: @HUBsup",
            reply_markup=get_back_mm()
        )
    elif data == CALLBACK_MM_TODO:
        query.edit_message_text(
            text="Altair8 все еще находится в разработке, на данный момент эта функция не доступна, но скоро мы это испраим.\
            \nНадеемся на ваше понимание! Если вы обнаружили какие либо баги в работе системы Altair8, пожалуйста сообщите нам: @HUBsup",
            reply_markup=get_back_mm()
        )
    elif data == CALLBACK_MM_CHATS:
        query.edit_message_text(
            text="Altair8 все еще находится в разработке, на данный момент эта функция не доступна, но скоро мы это испраим.\
            \nНадеемся на ваше понимание! Если вы обнаружили какие либо баги в работе системы Altair8, пожалуйста сообщите нам: @HUBsup",
            reply_markup=get_back_mm()
        )
    elif data == CALLBACK_RR:
        query.edit_message_text(
            text="Если вы ввели некорректный номер телефона в анкете, вы можете сменить номер следующей командой:\
            \nВведите /editphone <старый номер телефона> <новый номер телефона> <имя-фамилию как в анкете>. Пример:\
            \n/editphone +7XXXXXXXXXX +7YYYYYYYYYY Владимир Мономах\
            \nРаботает только для не авторизованных пользователей! Номер важно вводить без пробелов с одну строку."
        )


def main():
    updater = Updater(
        token=TG_TOKEN,
        use_context=True,
    )

    # Commands handler add, IF you u need add new command use it
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(CommandHandler('editphone', do_changephone))
    dp.add_handler(CommandHandler('addevent', do_addevent))
    #dp.add_handler(MessageHandler(Filters.sticker, handle_docs_audio))
    dp.add_handler(CallbackQueryHandler(callback=keyboard_call_handler, pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.contact, on_contact))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
