# пошаговая регистрация нового пользователя

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes,ConversationHandler
from database.db import Database
from database.models import User
from datetime import datetime
from keyboards.reply import main_keyboard, yesno_keyboard
from keyboards.buttons import ButtonsName

# Состояния для ConversationHandler
REGISTER_NAME, REGISTER_PHONE, REGISTER_ADDRESS, ADD_NEW_CLIENT, CANCEL_REGISTRATION = range(5)

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Начало процесса регистрации
    user = update.effective_user

    # Проверяем регистрацию пользователя
    db = Database()
    existing_client = db.get_client_by_id(user.id)
    db.close()

    if existing_client:
        await update.message.reply_text(f"Вы уже зарегистрированы!")
        return ConversationHandler.END

    # Запрашиваем имя
    await update.message.reply_text(
        "Введите ваше имя:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Использовать имя из Telegram")],
            [KeyboardButton(ButtonsName.REGISTRATION_CANCEL)]
            ], resize_keyboard=True
        )
    )
    return REGISTER_NAME


async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка введенного имени
    if update.message.text == "Отмена регистрации":
        return await cancel_registration(update, context)

    elif update.message.text == "Использовать имя из Telegram":
        context.user_data['first_name'] = update.effective_user.first_name

    else:
        context.user_data['first_name'] = update.message.text

    # Запрашиваем телефон
    await update.message.reply_text(
        "Отправьте ваш номер телефона:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Отправить контакт", request_contact=True)],
            [KeyboardButton(ButtonsName.REGISTRATION_CANCEL)]
             ], resize_keyboard=True
        )
    )
    return REGISTER_PHONE


async def process_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка номера телефона.
    # Получаем телефон из контакта или текста
    if update.message.text == "Отмена регистрации":
        return await cancel_registration(update, context)

    elif update.message.contact:
        context.user_data['phone'] = update.message.contact.phone_number

    else:
        context.user_data['phone'] = update.message.text

    # Запрашиваем адрес
    await update.message.reply_text("Отправьте адрес для доставки:",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton(ButtonsName.REGISTRATION_CANCEL)]], resize_keyboard=True)
    )

    return REGISTER_ADDRESS


async def process_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка введенного адреса
    if update.message.text == "Отмена регистрации":
        return await cancel_registration(update, context)

    else:
        context.user_data['address'] = update.message.text

    # проверка правильности введённых данных
    await update.message.reply_text(
        f"Данные введены правильно?\n"
        f"Имя: {context.user_data['first_name']}\n"
        f"Телефон: {context.user_data['phone']}\n"
        f"Адрес: {context.user_data['address']}",
    reply_markup = yesno_keyboard()
    )

    return ADD_NEW_CLIENT


async def add_new_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Если всё ок, сохраняем клиента в БД
    if update.message.text == "Нет":
        return await cancel_registration(update, context)

    user = update.effective_user
    client = User(
        user_id=user.id,
        username=user.username,
        first_name=context.user_data['first_name'],
        last_name=user.last_name,
        phone=context.user_data['phone'],
        address=context.user_data['address'],
        registration_date=datetime.now()
    )

    db = Database()
    if db.add_client(client):
        await update.message.reply_text(
            "Регистрация завершена! Спасибо.",
            reply_markup = main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', []))
        )
    else:
        await update.message.reply_text("Ошибка регистрации. Попробуйте позже.")

    db.close()
    return ConversationHandler.END


async def cancel_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отмена регистрации
    await update.message.reply_text(
        "Регистрация отменена.",
        reply_markup = main_keyboard(is_admin=update.effective_user.id in context.bot_data.get('admin_ids', []))
    )
    return ConversationHandler.END