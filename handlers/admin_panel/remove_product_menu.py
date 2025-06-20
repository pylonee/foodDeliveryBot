# полная очистка меню

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database.db import Database
from keyboards.reply import admin_keyboard, yesno_keyboard

# Состояние для ConversationHandler
DROP_MENU = range(1)

async def start_drop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # подтверждаем
    await update.message.reply_text("Удалить меню полностью?", reply_markup=yesno_keyboard())
    return DROP_MENU


async def drop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # если да, очищаем меню в базе
    if update.message.text == "Нет":
        return await cancel_drop_menu(update, context)

    db = Database()
    if db.remove_menu_items():
        await update.message.reply_text("Меню удалено", reply_markup=admin_keyboard())
    else:
        await update.message.reply_text("Ошибка удаления меню. Попробуйте позже.", reply_markup=admin_keyboard())

    return ConversationHandler.END


async def cancel_drop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отмена обновления меню
    await update.message.reply_text("Удаление меню отменено.", reply_markup=admin_keyboard())

    return ConversationHandler.END