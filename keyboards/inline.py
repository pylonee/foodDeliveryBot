# inline клавиатура для вывода меню заведения

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.db import Database

def product_keyboard(selected_options: set = None) -> InlineKeyboardMarkup:
    # Клавиатура с возможностью множественного выбора из меню
    if selected_options is None:
        selected_options = set()

    db = Database()
    menu = db.get_menu_items()
    db.close()

    if menu is None:
        return InlineKeyboardMarkup([])

    options = (f'{item[0]}#{item[3]}#{item[1]} - {item[3]} p.' for item in menu)

    keyboard = []
    for option in options:
        # Добавляем галочку для выбранных вариантов
        prefix = "✅ " if option in selected_options else ""
        callback_data = f"toggle_{option}"
        keyboard.append([InlineKeyboardButton(f"{prefix}{option.split('#')[2]}", callback_data=callback_data)])

    keyboard.append([InlineKeyboardButton("Готово", callback_data="done")])

    return InlineKeyboardMarkup(keyboard)