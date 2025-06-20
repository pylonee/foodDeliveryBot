# вывод клавиатуры для настройки меню заведения

from telegram import Update
from telegram.ext import CallbackContext
from keyboards.reply import edit_product_menu_keyboard
from keyboards.buttons import ButtonsName


async def open_edit_product_menu_panel(update: Update, context: CallbackContext) -> None:
    keyboard = edit_product_menu_keyboard()
    await update.message.reply_text(ButtonsName.EDIT_PRODUCT_MENU, reply_markup=keyboard)