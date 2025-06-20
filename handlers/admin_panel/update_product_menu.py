# Обновление/очистка меню заведения

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database.db import Database
from database.models import MenuItem
from keyboards.reply import admin_keyboard

# Состояние для ConversationHandler
UPDATE_MENU = range(1)

async def start_update_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # команда для обновления
    await update.message.reply_text(
        "Если нужно добавить новую позицию введите (БЕЗ ПРОБЕЛОВ МЕЖДУ ПАРАМЕТРАМИ, ТОЛЬКО _):\n"
        "add_id позиции(пример 0000)_название_описание_цена(без валюты)_категория_наличие(1 - да, 0 - нет)\n\n"
        "Если нужно удалить позицию из меню введите (БЕЗ ПРОБЕЛОВ МЕЖДУ ПАРАМЕТРАМИ, ТОЛЬКО _):\n"
        "remove_id позиции(пример 00000)"
    )

    return UPDATE_MENU

async def update_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # обрабатываем введенные строки и выполняем команды
    db = Database()
    not_done_ids = ''

    items_str = update.message.text.split("\n")
    for item in items_str:
        # item_str = update.message.text.split("_")
        item_str = item.split("_")
        print(item_str)
        if item_str[0].lower() == 'add':
            # добавление новой позиции
            new_item = MenuItem(
                item_id=int(item_str[1]),
                name=item_str[2],
                description=item_str[3],
                price=float(item_str[4]),
                category=item_str[5],
                available=bool(item_str[6])
            )
            if db.add_menu_item(new_item) is None:
                not_done_ids += f'{item_str[1]}, '

        elif item_str[0].lower() == 'remove' and item_str[1].isnumeric():
            # удаление позиции из меню по id
            existing_item = db.get_menu_item_by_id(int(item_str[1]))
            if existing_item is None:
                db.close()
                await update.message.reply_text(f"Позиции с таким id нет в базе", reply_markup=admin_keyboard())
                return ConversationHandler.END

            if not db.remove_menu_item_by_id(int(item_str[1])):
                not_done_ids += f'{item_str[1]}, '

        else:
            await update.message.reply_text(
                'Ошибка обновления меню: введена неправильная команда или указан неправильный id.\n'
                'Правильные команды:\n'
                'add - добавить\n'
                'remove - удалить\n'
                'id - только числа. Пример - 00000'
            )
            return ConversationHandler.END
    db.close()

    # если всё ок, то not_done_ids будет пустой (иначе там будут id не обновившихся позиций)
    if not_done_ids == '':
        await update.message.reply_text('Меню обновлено', reply_markup=admin_keyboard())
    else:
        await update.message.reply_text(f'Ошибка обновления меню в строках с id: {not_done_ids}. Попробуйте позже.', reply_markup=admin_keyboard())

    return ConversationHandler.END

    # new_item = MenuItem(
    #     item_id=int(item_str[0]),
    #     name=item_str[1],
    #     description=item_str[2],
    #     price=float(item_str[3]),
    #     category=item_str[4],
    #     available=bool(item_str[5])
    # )

    # db = Database()
    # if db.add_menu_item(new_item):
    #     await update.message.reply_text('Меню обновлено')
    # else:
    #     await update.message.reply_text('Ошибка обновления меню. Попробуйте позже.')


    #return ConversationHandler.END


async def cancel_update_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отмена обновления меню
    await update.message.reply_text("Обновление меню отменено.", reply_markup = admin_keyboard())

    return ConversationHandler.END