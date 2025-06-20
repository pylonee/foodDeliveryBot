# вывод панели администратора (reply клавиатура)

from telegram import Update
from telegram.ext import CallbackContext
from keyboards.reply import admin_keyboard
from keyboards.buttons import ButtonsName

async def open_admin_panel(update: Update, context: CallbackContext) -> None:
    keyboard = admin_keyboard()
    await update.message.reply_text(ButtonsName.ADMIN_PANEL, reply_markup=keyboard)