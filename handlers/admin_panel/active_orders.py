# показываем администратору все активные заказы

import json
from telegram import Update
from telegram.ext import CallbackContext
from database.db import Database
from keyboards.reply import admin_keyboard

async def show_active_orders(update: Update, context: CallbackContext) -> None:
    db = Database()

    active_orders = db.get_orders()

    if active_orders:
        # print ([order[2] for order in active_orders])
        # full_item_list = [item['items_id'] + ": " + item['items_name'] for order in active_orders for item in json.loads(order[2]) ]
        text = (
            '\n'.join([f"id заказа: {order[0]}\n\n"
                       f"Заказ: \n"
                       f"  {'\n  '.join([item['item_id'] + ": " + item['item_name'] for item in json.loads(order[2])])}\n\n"
                       f"Стоимость: {order[3]}\n"
                       f"Адрес: {order[4]}\n"
                       f"Дата: {order[6]}\n"
                       f"Cтатус: {order[5]}\n"
                       f"------------------------------------------------------------\n" for order in active_orders]))
        await update.message.reply_text(text, reply_markup=admin_keyboard())
    else:
        await update.message.reply_text("Нет активных заказов", reply_markup=admin_keyboard())

    db.close()