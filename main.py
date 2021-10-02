""" Altair8 HUB Interface Telegram bot ver 0.3
    Vladimir Monomakh
"""

# Import
from pymongo import MongoClient

import logging


from telegram import Bot
from telegram import Update

from telegram import ReplyKeyboardRemove

from telegram.ext import CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext

from config import TG_TOKEN
from config import MONGODB_LINK
from config import MONGO_DB

from keyboards import *

import certifi

ca = certifi.where()
# tele_Bot = telebot.TeleBot(TG_TOKEN, parse_mode=None)

# -------------------------------
# Bot Logic
# -------------------------------

# bot = Bot(TG_TOKEN)

# Connect to DataBase
mondb = MongoClient(MONGODB_LINK, tlsCAFile=ca)[MONGO_DB]


def on_start(update: Update, context: CallbackContext):
    message = update.message
    user = mondb.users.find_one({"user_id": message.chat.id})
    logging.info(message.chat.id)

    if not user:
        message.reply_text(
            'Добро пожаловать в Хаб!  Вы не авторизованный пользователь. Пожалуйста войдите в систему!',
            reply_markup=REPLY_KEYBOARD_MARKUP
        )
    else:
        message.reply_text(
            "Основное меню: ",
            reply_markup=get_main_menu()
        )
        # mondb.users.update_one(
        #     {'_id': user['_id']},
        #     {'$set':
        #          {'user_photo': "user_photos/" + str(user['user_id']) + ".jpg"}
        #      })


# def get_photo(update: Update, context: CallbackContext):
#     user = mondb.users.find_one({"user_id": update.message.chat.id})
#     query = update.callback_query
#     if user.get('user_photo') is not None:
#         if user.get('user_photo') == "need":
#             fileID = update.message.photo[-1].file_id
#             file_info = tele_Bot.get_file(fileID)
#             downloaded_file = tele_Bot.download_file(file_info.file_path)
#             with open("user_photos/" + str(user['user_id']) + ".jpg", 'wb') as new_file:
#                 new_file.write(downloaded_file)
#
#             mondb.users.update_one(
#                 {'_id': user['_id']},
#                 {'$set':
#                      {'user_photo': "user_photos/" + str(user['user_id']) + ".jpg"}
#                  })
#
#             context.bot.send_message(
#                 chat_id=user['user_id'],
#                 text="Фото успешно добавлено!",
#                 reply_markup=ReplyKeyboardRemove(),
#             )
#             context.bot.send_message(
#                 chat_id=user['user_id'],
#                 text="Главное меню:",
#                 reply_markup=get_projects_menu(),
#             )


def handle_text(update: Update, context: CallbackContext):
    message = update.message
    query = update.callback_query
    user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
    text = update.message.text

    if user is None:
        return
    #
    # if user.get('user_description') is not None:
    #     if user.get('user_description') == "need":
    #         mondb.ValentineEvent_users.update_one(
    #             {'_id': user['_id']},
    #             {'$set': {'user_description': text,
    #                       }
    #              })
    #         context.bot.send_message(
    #             chat_id=user['user_id'],
    #             text="Описание успешно добавлено!",
    #             reply_markup=ReplyKeyboardRemove(),
    #         )
    #         context.bot.send_message(
    #             chat_id=user['user_id'],
    #             text="Главное меню:",
    #             reply_markup=get_main_menu(),
    #         )
    if user.get('wait_project') is not None:
        if user.get('wait_project') != "n":
            try:
                mondb.projects_applic.insert_one({'user_full_name': user.get('user_name'),
                                                  'user_phone': user.get('user_phone'),
                                                  'project': user.get('wait_project'),
                                                  'text': text})
                mondb.users.update_one(
                    {'_id': user['_id']},
                    {'$set': {'wait_project': "n"}})
                context.bot.send_message(chat_id=user['user_id'],
                                         text="*Заявка на участие в проекте " + user.get('wait_project').split('_')[
                                             -1] +
                                              " принята! Координатор проекта обработает заявку в течении нескольких дней.",
                                         reply_markup=get_back_mm())
            except:
                context.bot.send_message(chat_id=user['user_id'],
                                         text="Ooops... \n\nКажется что то пошло не так, повторите попытку позже.",
                                         reply_markup=get_back_mm())


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
        logging.info(user)
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
                'Вас приветсвует Altair8 - интерфейс взаимодействия с H.U.B. ver 0.2.5 Интересного вам времяпрепровождения!\
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
    logging.info("user_phone: " + str(user_phone_number))
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
    user_new_phone_number = 0
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


def do_sendmessage(update: Update, context: CallbackContext):
    user_lead = 0
    try:
        lead_message = update.message.text
        user = mondb.users.find_one({"user_id": update.message.chat_id})

        if user.get('user_hubs') is not None:
            user_lead = int(user.get("user_hubs") / 1000000)
    except:
        update.message.reply_text(
            'Пожалуйста пройдите регистрацию!',
        )
        return
    if user_lead == 1:
        update.message.reply_text(
            'Только Лид может отправлять общую задачу!',
        )
    else:
        # Slot choice
        # TODO inline mode
        if len(lead_message) > 11:
            if lead_message[10] == '0':
                for x in mondb.users.find({"lead": True}):
                    if not (x.get("user_id") is None):
                        if str(x.get("user_hubs"))[0] == lead_message[12]:
                            context.bot.send_message(
                                chat_id=x.get("user_id"),
                                text=lead_message[11:],
                            )
            if lead_message[10] == '1':
                for x in mondb.users.find({"lead": True}):
                    if not (x.get("user_id") is None):
                        context.bot.send_message(
                            chat_id=x.get("user_id"),
                            text=lead_message[11:],
                        )
            if lead_message[10] == '2':
                for x in mondb.users.find():
                    if not (x.get("user_id") is None):
                        if str(x.get("user_hubs"))[user_lead - 1] == '1':
                            context.bot.send_message(
                                chat_id=x.get("user_id"),
                                text=lead_message[11:],
                            )
            if lead_message[10] == '3':
                for x in mondb.users.find():
                    if not (x.get("user_id") is None):
                        context.bot.send_message(
                            chat_id=x.get("user_id"),
                            text=lead_message[11:],
                        )
            else:
                update.message.reply_text(
                    'Неверно указан ключ отправления!',
                )
        else:
            update.message.reply_text(
                'Слишком короткое сообщение!',
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

    user_lead = 0
    if user.get('user_hubs') is not None:
        user_lead = int(user.get("user_hubs") / 1000000)
    if user_lead == 1:
        update.message.reply_text(
            'Только Лид может изменять расписание!',
        )
    else:
        # Slot choice
        # TODO Edit this command, automatic slot choice
        if text[10] == '1':
            mondb.allschledule.update_one(
                {'hub_id': user_lead - 1},
                {'$set': {'event1': text[12:]}}
            )
        if text[10] == '2':
            mondb.allschledule.update_one(
                {'hub_id': user_lead - 1},
                {'$set': {'event2': text[12:]}}
            )
        if text[10] == '3':
            mondb.allschledule.update_one(
                {'hub_id': user_lead - 1},
                {'$set': {'event3': text[12:]}}
            )


# Telegram inline menu buttons handler
def keyboard_call_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    # query.answer_callback_query(query.id, text="Всплывашка!", show_alert=True)

    if data == CALLBACK_MM:
        query.edit_message_text(
            text="Основное меню: ",
            reply_markup=get_main_menu()
        )
    elif data == CALLBACK_MM_HUB:
        user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
        query.edit_message_text(
            text="Все двери открыты! \nВся пятерка открытых Хабов полностью доступна вам: ",
            reply_markup=get_hubs(str(user.get("user_hubs")))
        )
    #    # TODO Inline music add
    # elif data == CALLBACK_MM_MUSIC:
    #    chatid = update.effective_message.chat_id
    #    query.edit_message_text(
    #        text="Музыка дня, для души и работы от участников Хаба. Сегодня в честь запуска музыка от @MON0makh\
    #     \nЗаказать плейлист можно у @MON0makh 🎧",
    #    )
    #    # TODO Local audio need
    #    context.bot.send_sticker(chatid, 'CAACAgEAAxkBAAIDMV92U2Sk4DVLErXtBFPWgQhfmqh1AAJhAAPArAgjT8wG8ZJFRc0bBA')
    #    for i in range(1, 7):
    #        context.bot.send_audio(
    #            chat_id=chatid,
    #            audio='https://raw.githubusercontent.com/POSE1D0N-AP/Altair8tb/master/music%20of%20day/{}.mp3'.format(i),
    #        )
    #    context.bot.send_message(
    #        chat_id=chatid,
    #        text="Основное меню",
    #        reply_markup=get_main_menu(),
    #   )

    elif data == CALLBACK_MM_SCHEDULE:
        chatid = update.effective_message.chat_id
        user = mondb.users.find_one({"user_id": chatid})
        # TODO add BIGHUB Schledule

        no_event = 0
        for i in range(1, 7):
            table = mondb.allschledule.find_one({"hub_id": i})
            if table != None:
                text = table.get('hub_name') + ": "
                if table.get('event1') != None:
                    text += "\n" + table.get('event1')
                if table.get('event2') != None:
                    text += "\n" + table.get('event2')
                if table.get('event3') != None:
                    text += "\n" + table.get('event3')

                # IF schedule empty
                if len(text) > 10:
                    context.bot.send_message(
                        chat_id=chatid,
                        text="{}".format(text),
                    )
                else:
                    no_event += 1
        if no_event == 6:
            context.bot.send_message(
                chat_id=chatid,
                text="Либо здесь что то не так либо в ближайшее время нет запланированных мероприятий.",
            )
    elif data == CALLBACK_MM_CORNER:
        # user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
        # mondb.users.update_one(
        #    {'_id': user['_id']},
        #    {'$set': {'user_photo': "need"}})

        query.edit_message_text(
            text="В разделе #CORNER вы можете оставлять информацию о себе и смотреть анкеты других, в поисках \
                    друзей и единомышлеников!\
                    \n\nОбщайтесь и разивайтесь вместе с Хабом! \
                    \n**Данный раздел находится в разработке",
            reply_markup=get_back_mm()
        )
        context.bot.answer_callback_query(query.id, text="Функция CORNER в разработке 🛠", show_alert=True)

    elif data == CALLBACK_MM_PROJECTS:
        query.edit_message_text(
            text="Выберите проект на который вы хотите подать заявку:",
            reply_markup=get_projects_menu()
        )

    elif data == CALLBACK_PROJECTS_WS or \
            data == CALLBACK_PROJECTS_HS or \
            data == CALLBACK_PROJECTS_HM or \
            data == CALLBACK_PROJECTS_PUB or \
            data == CALLBACK_PROJECTS_GS:
        project_name = data.split("_")[-1]
        user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'wait_project': data}})

        query.edit_message_text(
            text="Проект: \"" + project_name + "\"\n\nОпишите одним сообщением какая деятельность " +
                 "в проекте вас интересует, свой опыт в сфере и чем бы вы хотели заниматься в рамках этого проекта.",
            reply_markup=get_cancel(),
        )



    elif data == CALLBACK_PROJECTS_UP:
        user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'wait_project': data}})

        query.edit_message_text(
            text="Опишите свой проект который вы хотели бы реализовать вместе с сообществом Хаб.",
            reply_markup=get_cancel(),
        )

    elif data == CALLBACK_MM_CANCEL:
        user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'wait_project': 'n'}})
        query.edit_message_text(
            text="Основное меню: ",
            reply_markup=get_main_menu()
        )


    elif data == CALLBACK_CORNER_RIGHT or data == CALLBACK_CORNER_LEFT:
        user = mondb.users.find_one({"user_id": update.effective_message.chat_id})
        corn_users = mondb.users.find({"user_in_corner": True})
        if data == CALLBACK_CORNER_RIGHT:
            user['corner_page'] += 1
            if user.get('corner_page') > len(corn_users):
                user['corner_page'] = 0
        else:
            user['corner_page'] -= 1
            if user.get('corner_page') < 0:
                user['corner_page'] = len(corn_users)

        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'corner_page': user['corner_page']
                      }}
        )
        query.edit_message_text(
            text=corn_users[user['corner_page']]  # ,
            # reply_markup=get_corner_nav()
        )


    elif data == CALLBACK_MM_SHOP:
        context.bot.answer_callback_query(query.id, text="Функция SHOP в разработке 🛠", show_alert=True)

    elif data == CALLBACK_MM_SETTING:
        query.edit_message_text(
            text="Интерфейс взаимодействия для сообщества Хаб\
            \nЕсли вы столкнулись с проблемой взаимодействия с ботом обращаться к - @HUBsup\
            \n\nПодписывайтесь на нас в социальных сетях, что бы ничего не пропустить!",
            reply_markup=get_social_networks()
        )
    elif data == CALLBACK_MM_TASKS:
        context.bot.answer_callback_query(query.id, text="У вас нет активных задач!", show_alert=True)

    elif data == CALLBACK_RR:
        query.edit_message_text(
            text="Если вы ввели некорректный номер телефона в анкете, вы можете сменить номер следующей командой:\
            \nВведите /editphone <старый номер телефона> <новый номер телефона> <имя-фамилию как в анкете>. Пример:\
            \n/editphone +7XXXXXXXXXX +7YYYYYYYYYY Владимир Мономах\
            \nРаботает только для не авторизованных пользователей! Номер важно вводить без пробелов с одну строку.\
            \n\nВ случае возникновения проблем обратитесь в тех.поддержку: @HUBsup"
        )


def main():
    updater = Updater(
        token=TG_TOKEN,
        use_context=True,
    )
    logging.info("Altair8 started")
    # Commands handler add, IF you u need add new command use it
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(CommandHandler('editphone', do_changephone))
    dp.add_handler(CommandHandler('addevent', do_addevent))
    dp.add_handler(CommandHandler('sendtask', do_sendmessage))
    # dp.add_handler(MessageHandler(Filters.sticker, handle_docs_audio))
    dp.add_handler(CallbackQueryHandler(callback=keyboard_call_handler, pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.contact, on_contact))
    # dp.add_handler(MessageHandler(Filters.photo, get_photo))
    dp.add_handler(MessageHandler(Filters.text, handle_text))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
