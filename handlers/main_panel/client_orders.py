# Активные заказы пользователя

from telegram import Update
from telegram.ext import CallbackContext
from database.db import Database
from keyboards.reply import main_keyboard

async def show_client_orders(update: Update, context: CallbackContext) -> None:
    db = Database()
    active_order = db.get_order_by_client_id(update.effective_user.id)
    db.close()

    if active_order:
        text = (f"Номер заказа: {active_order.order_id}\n"
                f"Вы заказали: \n"
                f"  {'\n  '.join([item['item_name'] for item in active_order.items])}\n"
                f"Стоимость заказа: {active_order.total}\n"
                f"Статус заказа: {active_order.status}")
        await update.message.reply_text(text, reply_markup=main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', [])))
    else:
        await update.message.reply_text("У вас нет активных заказов", reply_markup=main_keyboard(
            is_admin=update.effective_user.id in context.bot_data.get('admin_ids', [])))