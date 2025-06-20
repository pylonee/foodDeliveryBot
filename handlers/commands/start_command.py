# команда /start

from telegram import Update
from telegram.ext import CallbackContext
from keyboards.reply import main_keyboard

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    existing_user = True

    if existing_user:
        text = f'С возвращением, {user.first_name}!'
        keyboard = main_keyboard(is_admin=user.id in context.bot_data.get('admin_ids', []))
    else:
        text = (
            f"Привет, {user.first_name}!\n"
            f"Я бот по доставке еды.\n"
            f"Чтобы сделать заказ нужно зарегистрироваться"
        )
        # keyboard = registration_keyboard()
        keyboard = main_keyboard(is_admin=user.id in context.bot_data.get('admin_ids', []))

    await update.message.reply_text(text, reply_markup=keyboard)

start_handler = start