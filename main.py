import logging
from config import TOKEN, ADMIN_IDS

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

from handlers import message_handler, registration
from handlers.commands import about_command, help_command, start_command

from handlers.admin_panel import admin, statistics, active_orders, remove_client, edit_product_menu, update_product_menu, remove_product_menu
from handlers.main_panel import main_panel, products, client_orders, contacts

from keyboards.buttons import ButtonsName

# логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
REGISTER_NAME, REGISTER_PHONE, REGISTER_ADDRESS, ADD_NEW_CLIENT, CANCEL_REGISTRATION = range(5)
DELETE_CLIENT = range(1)
UPDATE_MENU = range(1)
DROP_MENU = range(1)
MAKE_ORDER = range(1)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.bot_data['admin_ids'] = ADMIN_IDS

    # ============================ Commands ============================
    application.add_handler(CommandHandler('start', start_command.start))
    application.add_handler(CommandHandler('help', help_command.help_command))
    application.add_handler(CommandHandler('about', about_command.about_command))
    application.add_handler(CommandHandler('main_menu', main_panel.open_main_panel))

    # ============================ Main-panel ============================
    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.MY_ORDERS}$'), client_orders.show_client_orders))
    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.CONTACTS}$'), contacts.show_contacts))

    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.PRODUCT_MENU}$'), products.start_selection))
    application.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(products.handle_selection, pattern="^(toggle_.*|done)$")],
        states={
            MAKE_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, products.make_order)]
        },
        fallbacks=[CommandHandler('cancel_make_order', products.cancel_make_order)]
    ))


    # ============== Registration ==============
    application.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(f'^{ButtonsName.REGISTRATION}$'), registration.start_registration)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration.process_name)],
            REGISTER_PHONE: [
                MessageHandler(filters.CONTACT, registration.process_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, registration.process_phone)
            ],
            REGISTER_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration.process_address)],
            ADD_NEW_CLIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration.add_new_client)],
            CANCEL_REGISTRATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration.cancel_registration)],
        },
        fallbacks=[
            CommandHandler('cancel_registration', registration.cancel_registration)
        ]
    ))


    # ============================ Admin-panel ============================
    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.ADMIN_PANEL}$'), admin.open_admin_panel))
    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.STATISTIC}$'), statistics.show_stats))
    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.ACTIVE_ORDERS}$'), active_orders.show_active_orders))
    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.EDIT_PRODUCT_MENU}$'), edit_product_menu.open_edit_product_menu_panel))
    application.add_handler(MessageHandler(filters.Regex(f'^{ButtonsName.MAIN_MENU}$'), main_panel.open_main_panel))

    # ============== Delete client ==============
    application.add_handler(ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^{ButtonsName.DELETE_CLIENT}$'), remove_client.start_remove_client)],
        states={
            DELETE_CLIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_client.remove_user_by_id)]
        },
        fallbacks=[CommandHandler('cancel_delete_client', remove_client.cancel_delete)]
    ))


    # ============== Edit product menu ==============
    # ======= Edit =======
    application.add_handler(ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^{ButtonsName.ADD_NEW_MENU_POSITION}$'), update_product_menu.start_update_menu)],
        states={
            UPDATE_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_product_menu.update_menu)]
        },
        fallbacks=[
            CommandHandler('cancel_update_menu', update_product_menu.cancel_update_menu)
        ]
    ))
    # ======= Drop menu =======
    application.add_handler(ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^{ButtonsName.DROP_PRODUCT_MENU}$'), remove_product_menu.start_drop_menu)],
        states={
            DROP_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_product_menu.drop_menu)]
        },
        fallbacks=[
            CommandHandler('cancel_drop_menu', remove_product_menu.cancel_drop_menu)
        ]
    ))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler.handle_message))


    application.run_polling()


if __name__ == '__main__':
    main()