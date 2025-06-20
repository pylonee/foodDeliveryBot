# Ответы бота на простые сообщения от пользователя

from telegram import Update
from telegram.ext import CallbackContext


async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()

    if 'привет' in text:
        await update.message.reply_text(f"Привет, {update.effective_user.first_name}!")
    elif 'как дела' in text:
        await update.message.reply_text('У ботов всегда отлично!\n А у тебя?')
    elif '^Заказ ' in text:
        await update.message.reply_text('ну ты выдал))')
    else:
        await update.message.reply_text('На такое я пока не научился отвечать. Используй /help для списка команд')