from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

# Login Keyboard
contact_keyboard = KeyboardButton('Войти', request_contact=True)
custom_keyboard_login = [[contact_keyboard]]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(custom_keyboard_login, resize_keyboard=True)

CALLBACK_MM = "cb_mm"
CALLBACK_MM_HUB = "cb_mm_hs"
CALLBACK_MM_CHATS = "cb_mm_ch"
CALLBACK_MM_SCHEDULE = "cb_mm_sch"
CALLBACK_MM_TASKS = "cb_mm_ts"
CALLBACK_MM_TODO = "cb_mm_todo"
CALLBACK_MM_MUSIC = "cb_mm_mus"
CALLBACK_MM_SETTING = "cb_mm_setting"
CALLBACK_MM_ARRadio = "cb_mm_arr"
CALLBACK_MM_SHOP = "cb_mm_shop"
CALLBACK_MM_CORNER = "cb_mm_corner"
CALLBACK_MM_PROJECTS = "cb_mm_projects"
CALLBACK_MM_CANCEL = "cb_nav_cancel"
CALLBACK_CORNER_LEFT = "cb_cr_lf"
CALLBACK_CORNER_RIGHT = "cb_cr_rhg"
CALLBACK_RR = "cb_rr"

CALLBACK_PROJECTS_PUB = "cb_pr_PlanetDotHub"
CALLBACK_PROJECTS_GS = "cb_pr_RedHex Game Studio"
CALLBACK_PROJECTS_HM = "cb_pr_HUB MEDIA"
CALLBACK_PROJECTS_WS = "cb_pr_theHub Web Studio"
CALLBACK_PROJECTS_HS = "cb_pr_HUB SCHOOL"
CALLBACK_PROJECTS_UP = "cb_pr_user_projects"


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
        keyboard.append([InlineKeyboardButton("🎮   GEEK.HUB", url="https://t.me/HramBoginiBABISA")])
    keyboard.append([InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM)])

    return InlineKeyboardMarkup(keyboard)


def get_social_networks():
    keyboard = [
        [
            InlineKeyboardButton("🌐  Web Site", url='https://www.thehub.su/'),
        ],
        [
            InlineKeyboardButton("📸 Instagram", url='https://instagram.com/thehub.su'),
        ],
        [
            InlineKeyboardButton("✈  Telegram Chanel", url='https://t.me/thehub_su'),
        ],
        [
            InlineKeyboardButton("️🎥  YouTube", url='https://www.youtube.com/channel/UC8luLtn3EhGh0wWqE92sUZA'),
        ],
        [
            InlineKeyboardButton("🎙  Discord", url='https://discord.gg/y6CsTWxtwA'),
        ],
        [
            InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_corner_nav(full_name, username):
    keyboard = [
        [
            InlineKeyboardButton(full_name, url='https://t.me/' + username),
        ],
        [
            InlineKeyboardButton("⬅️", callback_data=CALLBACK_CORNER_LEFT),
            InlineKeyboardButton("➡️", callback_data=CALLBACK_CORNER_RIGHT),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_mm():
    keyboard = [[InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM)]]
    return InlineKeyboardMarkup(keyboard)


def get_cancel():
    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data=CALLBACK_MM_CANCEL)]]
    return InlineKeyboardMarkup(keyboard)


# Main Menu
def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🕸  Small HUBs", callback_data=CALLBACK_MM_HUB),
        ],
        [
            InlineKeyboardButton("📆 Расписание", callback_data=CALLBACK_MM_SCHEDULE),
            InlineKeyboardButton("📋 Задачи", callback_data=CALLBACK_MM_TASKS),
        ],
        [
            InlineKeyboardButton("💡 Проекты", callback_data=CALLBACK_MM_PROJECTS),
        ],
        [
            InlineKeyboardButton("▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰", callback_data='null'),
        ],
        [
            InlineKeyboardButton("🎵  Art.Hub Radio", url='https://t.me/arthub_radio'),
        ],
        [
            InlineKeyboardButton("💎  Corner", callback_data=CALLBACK_MM_CORNER),
        ],
        [
            InlineKeyboardButton("🛒  Shop", callback_data=CALLBACK_MM_SHOP),
        ],
        [
            InlineKeyboardButton("ℹ️  Дополнительно️", callback_data=CALLBACK_MM_SETTING),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# Projects Menu
def get_projects_menu():
    keyboard = [
        [
            InlineKeyboardButton("🪐  PlanetDotHub", callback_data=CALLBACK_PROJECTS_PUB),
        ],
        [
            InlineKeyboardButton("🕹 Game Studio", callback_data=CALLBACK_PROJECTS_GS),
        ],
        [
            InlineKeyboardButton("🎥 HUB.MEDIA", callback_data=CALLBACK_PROJECTS_HM),
        ],
        [
            InlineKeyboardButton("🏫 the Hub School", callback_data=CALLBACK_PROJECTS_HS),
        ],
        [
            InlineKeyboardButton("🖥 Web Studio", callback_data=CALLBACK_PROJECTS_WS),
        ],
        [
            InlineKeyboardButton("🎒\"Я со своим!\"", callback_data=CALLBACK_PROJECTS_UP),
        ],
        [
            InlineKeyboardButton(" Назад", callback_data=CALLBACK_MM),
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
