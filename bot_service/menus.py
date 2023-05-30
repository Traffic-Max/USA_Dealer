from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def send_admin_menu(message):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Создать пост', callback_data='new_post')
    button2 = InlineKeyboardButton('Очередь публикаций', callback_data='view_queue')
    keyboard.add(button1)
    keyboard.add(button2)

    await message.answer("Это меню админа в MG.\nВыбирай что будешь делать, и не трать мое время!", reply_markup=keyboard)


async def send_root_menu(message):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Создать пост', callback_data='new_post')
    button2 = InlineKeyboardButton('Просмотреть очередь', callback_data='view_queue')
    button3 = InlineKeyboardButton('Назначить админа', callback_data='view_applications')
    keyboard.add(button1, button2, button3)

    await message.answer("[*] Это меню админа в MG.\nВыбирай что будешь делать, и не трать мое время!", reply_markup=keyboard)
