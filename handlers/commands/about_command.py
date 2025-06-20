# команда /about

from telegram import Update
from telegram.ext import CallbackContext

async def about_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Демонстрационный бот заказов еды.\n"
        "Версия: 1.0\n"
    )