# получение меню + обработка выбора

from telegram import Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler
from keyboards.inline import product_keyboard
from keyboards.reply import yesno_keyboard, main_keyboard
from database.db import Database
from database.models import Order
from datetime import datetime

# Состояния для ConversationHandler
MAKE_ORDER = range(1)

async def start_selection(update: Update, context: CallbackContext) -> None:
    # вывод меню заведения
    await update.message.reply_text(
        "Меню:",
        reply_markup=product_keyboard()
    )

async def handle_selection(update: Update, context: CallbackContext):
    # обрабатываем выбор пользователя
    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    if 'selected_items' not in user_data:
        user_data['selected_items'] = set()

    # Обрабатываем нажатие
    if query.data.startswith("toggle_"):
        item = query.data[7:]  # Извлекаем название после "toggle_"

        # Переключаем выбор
        if item in user_data['selected_items']:
            user_data['selected_items'].remove(item)
        else:
            user_data['selected_items'].add(item)

        # Обновляем клавиатуру
        await query.edit_message_reply_markup(
            reply_markup=product_keyboard(user_data['selected_items'])
        )
        return None

    elif query.data == "done":
        # Фиксируем окончательный выбор
        selected = user_data['selected_items']
        # показываем пользователю заказ
        await query.edit_message_text(
            f"Вы выбрали:\n"
            f"{', '.join([item.split("#")[2] for item in selected]) or 'ничего'}\n"
            f"Сумма заказа: {sum([float(item.split("#")[1]) for item in selected])}\n",
            reply_markup=None
        )
        # меняем на reply клавиатуру
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Продолжить?",
            reply_markup=yesno_keyboard()
        )
        return MAKE_ORDER
    return None

async def make_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # если всё ок, добавляем заказ в БД
    if update.message.text == "Нет":
        return await cancel_make_order(update, context)

    db = Database()
    user = db.get_client_by_id(update.effective_user.id)

    # если пользователь не зарегистрирован
    if user is None:
        db.close()
        await update.message.reply_text("Для совершения заказа нужно зарегистрироваться",
                                        reply_markup=main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', [])))
        return ConversationHandler.END

    #  если всё ок обрабатываем заказ
    full_items_data = context.user_data['selected_items']
    order_items_list = list()
    for item in full_items_data:
        order_item_dict = {
            "item_id": item.split("#")[0],
            "item_name": f"{item.split("#")[2]}"
        }
        order_items_list.append(order_item_dict)

    #[order_items_list.append(order_items_dict = {"items_ids": "", "items_names": ""}) for item in full_items_data]
    # order_items_dict = {
    #     "items_ids": f"{', '.join([item.split("#")[0] for item in full_items_data])}",
    #     "items_names": f"{'\n'.join([item.split("#")[3] for item in full_items_data])}"
    # }
    order_items = [item for item in full_items_data]
    order_total = sum([float(item.split("#")[1]) for item in full_items_data])

    address = user.address

    client_order = Order(
        order_id=0,
        user_id=update.effective_user.id,
        items=order_items_list,
        total=order_total,
        address=address,
        status='Active',
        order_date=datetime.now()
    )

    order = db.add_order(client_order)
    db.close()

    if order:
        await update.message.reply_text(
            f"Заказ успешно сформирован\n"
            f"Номер заказа: {order}\n"
            f"Спасибо, что выбрали нас", reply_markup=main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', [])))
    else:
        await update.message.reply_text("Ошибка заказа. Попробуйте позже.", reply_markup=main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', [])))

    return ConversationHandler.END


async def cancel_make_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отмена заказа
    await update.message.reply_text(
        "Создание заказа отменено.",
        reply_markup=main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', []))
    )
    return ConversationHandler.END