# Открываем главное меню

from telegram import Update
from telegram.ext import CallbackContext
from keyboards.reply import main_keyboard
from keyboards.buttons import ButtonsName

async def open_main_panel(update: Update, context: CallbackContext) -> None:
    keyboard = main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', []))
    await update.message.reply_text(ButtonsName.MAIN_MENU, reply_markup=keyboard)