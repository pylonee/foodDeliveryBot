# удаление пользователя

from telegram import Update
from keyboards.reply import admin_keyboard
from database.db import Database
from telegram.ext import ContextTypes, ConversationHandler

# Состояние для ConversationHandler
DELETE_CLIENT= range(1)

async def start_remove_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Запрашиваем id клиента
    await update.message.reply_text(
        "Введите id клиента, которого хотите удалить:", reply_markup=admin_keyboard())
    return DELETE_CLIENT


async def remove_user_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Удаляем из БД клиента по id
    try:
        int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Ошибка удаления: id не должен содержать буквы", reply_markup=admin_keyboard())
        return ConversationHandler.END

    user_id = int(update.message.text.strip())
    db = Database()

    existing_client = db.get_client_by_id(user_id)
    if existing_client is None:
        await update.message.reply_text(f"Пользователя с таким id нет в базе", reply_markup=admin_keyboard())
        return ConversationHandler.END

    if db.remove_client_by_id(user_id):
        await update.message.reply_text(f"Пользователь {user_id} удалён.", reply_markup=admin_keyboard())
    else:
        await update.message.reply_text("Ошибка удаления. Попробуйте позже.", reply_markup=admin_keyboard())

    db.close()

    return ConversationHandler.END

async def cancel_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отмена удаления
    await update.message.reply_text("Удаление клиента отменено.", reply_markup = admin_keyboard())
    return ConversationHandler.END