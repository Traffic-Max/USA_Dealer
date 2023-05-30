from bot_service import dp

from bot_service.states import PostCreation, StatusChange

# Импортируйте сюда свои обработчики команд
from bot_service.commands import cmd_start, cmd_admin, cmd_join, cmd_newpost, process_content, process_auto_info, process_callback_accept, process_callback_decline, process_callback_view_applications, process_callback_accept_descrition, process_callback_decline_description

from bot_service.menus import send_admin_menu, send_root_menu

from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram import types


# Регистрация обработчиков команд
dp.register_message_handler(cmd_start, Command("start"))
dp.register_message_handler(cmd_admin, Command("admin"))
dp.register_message_handler(cmd_join, Command("join"))

# Регистрация обработчиков callback запросов
dp.register_callback_query_handler(process_callback_view_applications, text='view_applications')
dp.register_callback_query_handler(process_callback_accept, lambda callback_query: callback_query.data.startswith('accept_'))
dp.register_callback_query_handler(process_callback_decline, lambda callback_query: callback_query.data.startswith('decline_'))
dp.register_callback_query_handler(cmd_newpost, text='new_post')
dp.register_callback_query_handler(process_callback_decline_description, text='accept', state=PostCreation.waiting_for_description_approval)
dp.register_callback_query_handler(process_callback_decline_description, text='decline', state=PostCreation.waiting_for_description_approval)

# Регистрация обработчиков сообщений в состояниях машины состояний
dp.register_message_handler(process_content, content_types=types.ContentTypes.PHOTO, state=PostCreation.waiting_for_content)
dp.register_message_handler(process_auto_info, state=PostCreation.waiting_for_auto_info)