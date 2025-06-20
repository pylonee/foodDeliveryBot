# получение статистики

from telegram import Update
from telegram.ext import CallbackContext
from keyboards.buttons import ButtonsName

async def show_stats(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"{ButtonsName.STATISTIC}:")
    await update.message.reply_text(f"1. AAA\n 2. SSS\n 3. DDD")