# команда /help

from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext) -> None:
    text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить список команд\n"
        "/about - Информация о боте\n"
    )
    await update.message.reply_text(text)