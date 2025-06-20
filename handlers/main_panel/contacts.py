# Контакты

from telegram import Update
from telegram.ext import CallbackContext
from keyboards.buttons import ButtonsName

async def show_contacts(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"{ButtonsName.CONTACTS}:")
    await update.message.reply_text(f"Тел.: 0-000-000-00-00\n Email: kakay-to-pochta@kakoyto-yashik.a")