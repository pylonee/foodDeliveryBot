# reply клавиатуры для действий

from telegram import KeyboardButton, ReplyKeyboardMarkup
from keyboards.buttons import ButtonsName

# основная клавиатура
def main_keyboard(is_admin: bool = False, is_register: bool = False) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(ButtonsName.PRODUCT_MENU)],
        [KeyboardButton(ButtonsName.MY_ORDERS), KeyboardButton(ButtonsName.CONTACTS)]
    ]

    if not is_register:
        buttons.append([KeyboardButton(ButtonsName.REGISTRATION)])

    if is_admin:
        buttons.append([KeyboardButton(ButtonsName.ADMIN_PANEL)])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# да/нет клавиатура
def yesno_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(ButtonsName.YES), KeyboardButton(ButtonsName.NO)]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# регистрация (пока не нужна)
# def registration_keyboard() -> ReplyKeyboardMarkup:
#     buttons = [[KeyboardButton(ButtonsName.SEND_CONTACT, request_contact=True)]]
#     return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# клавиатура админа
def admin_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(ButtonsName.STATISTIC)],
        [KeyboardButton(ButtonsName.ACTIVE_ORDERS)],
        [KeyboardButton(ButtonsName.EDIT_PRODUCT_MENU)],
        [KeyboardButton(ButtonsName.DELETE_CLIENT)],
        [KeyboardButton(ButtonsName.MAIN_MENU)],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# клавиатура настройки меню заведения
def edit_product_menu_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(ButtonsName.ADD_NEW_MENU_POSITION)],
        [KeyboardButton(ButtonsName.DROP_PRODUCT_MENU)],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

