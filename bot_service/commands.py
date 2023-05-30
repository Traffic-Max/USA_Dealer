import time
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from bot_service import dp, bot, config

from bot_service.models import SessionLocal, add_content_to_db
from bot_service.models import register_user, apply_for_admin, User, AdminApplication
from bot_service.menus import send_admin_menu, send_root_menu
from bot_service.states import PostCreation, StatusChange
from bot_service.description_generator import generate_description

ROOT_ADMIN_ID = config.ROOT_ADMIN_ID

async def cmd_start(message: types.Message):
    user = register_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    
    # print(tg_user)
    # await message.answer(f"Your id {message.from_user.id}\nName: {user.user_firstname}")
    if message.from_user.id == ROOT_ADMIN_ID:
            await message.answer("С возвращением шеф! Погнали работать!")
            await send_root_menu(message)
            return
    elif user and user.status == "admin":
            await message.answer(f"Зарова {user.user_firstname}! Погнали работать!")
            await send_admin_menu(message)
            return
    
    await message.answer("Приветствую! Здесь Тревор Филипс!\nЯ помощник по управлению контентом в нашей банде. Я отвечаю за этот движ в MG и буду с тебя спрашивать как со всех!")
    time.sleep(5)
    await message.answer("Понимаю, ты у нас новенький, без особых прав, если хочешь стать админом жми /join\n и давай уже работать, у меня здесь не курорт!")


async def cmd_admin(message: types.Message):
    with Session() as session:
        user = session.query(User).filter(User.user_id == message.from_user.id).first()
        # print(f"User is :{user}")
        # Проверка на рут-админа
        if message.from_user.id == ROOT_ADMIN_ID:
            await send_admin_menu(message)
            return

        # Если пользователь не рут-админ, проверяем его статус
        if user and user.status == "admin":
            await send_admin_menu(message)
            return

        await message.answer("А ты не из наших сынок, куда ломишься!?\n\nНажми /join, если так не терпиться попасть в банду MG.")



async def process_callback_view_applications(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    with Session() as session:
        applications = session.query(AdminApplication).filter(AdminApplication.status == "pending").all()

        if applications:
            for application in applications:
                keyboard = InlineKeyboardMarkup()
                button1 = InlineKeyboardButton('Принять', callback_data=f'accept_{application.user_id}')
                button2 = InlineKeyboardButton('Отклонить', callback_data=f'decline_{application.user_id}')
                keyboard.add(button1, button2)

                await bot.send_message(callback_query.from_user.id, 
                                       f"Заявка от {application.username}\nID {application.user_id}.", 
                                       reply_markup=keyboard)
        else:
            await bot.send_message(callback_query.from_user.id, "Нет заявок.")


async def process_callback_accept(callback_query: types.CallbackQuery):
    application_id = int(callback_query.data.split('_')[1])
    print(application_id)
    with Session() as session:
        user = session.query(User).filter(User.user_id == application_id).first()
        user.status = "admin"
        session.commit()
        await bot.send_message(user.user_id, "Поздравляю, заявка одобрена.\nТеперь ты в банде MG!")
    await bot.answer_callback_query(callback_query.id)


async def process_callback_decline(callback_query: types.CallbackQuery):
    application_id = int(callback_query.data.split('_')[1])
    with Session() as session:
        user = session.query(User).filter(User.id == application_id).first()
        user.status = "declined"
        session.commit()
        await bot.send_message(user.user_id, "Прости, но ты не прошел отбор на должность админа.")
    await bot.answer_callback_query(callback_query.id)


async def cmd_join(message: types.Message):
    with Session() as session:
        user = session.query(User).filter(User.user_id == message.from_user.id).first()
        if user.status == "user":
            apply_for_admin(message.from_user.id, message.from_user.username)
            await message.answer("Заявка на получение админ доступа подана!\nОжидай уведомления о рассмотрении.")

            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton('Просмотреть заявки', callback_data='view_applications')
            keyboard.add(button)

            await bot.send_message(ROOT_ADMIN_ID, f"Заявка на административные права от пользователя {user.username}.", reply_markup=keyboard)
        else:
            await message.answer("Ты уже админ в банде, {username}!".format(username=message.from_user.username))


async def cmd_newpost(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer("[*] Новый пост, а? Ладно, кидай фото контент сюда, и быстрее!")
    await PostCreation.waiting_for_content.set()


async def process_content(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['content'] = message.photo[-1].file_id  # Сохраняем file_id последнего элемента в списке фотографий
    await message.answer("[*] Контент принят. Теперь давай информацию об автомобиле. И не тормози!")
    await PostCreation.waiting_for_auto_info.set()


async def process_auto_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['auto_info'] = message.text
    description = generate_description(data['auto_info'])

    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Принять', callback_data='accept')
    button2 = InlineKeyboardButton('Отклонить', callback_data='decline')
    keyboard.add(button1, button2)

    await message.reply("Твое описание:\n\n" + description + ".\n\nНе самое лучшее, что я видел, но сойдет.")
    await message.reply("Одобряешь?", reply_markup=keyboard)
    await PostCreation.waiting_for_description_approval.set()


async def process_callback_accept_descrition(callback_query: types.CallbackQuery, state:FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        content = data['content']
        description = data['auto_info']
    if add_content_to_db(content, description): # Попытка добавить контент в базу данных
        await callback_query.message.answer(f"Данные по авто:\n{data}")
        await callback_query.message.answer("Пост добавлен в очередь. Ты быстрее работай в следующий раз!")
    else:
        await callback_query.message.answer("Ошибка при добавлении поста в базу данных.\nПопробуй еще раз позже.\nИ только если это не поможет обратись к @badass_marketing")
    await state.finish()


async def process_callback_decline_description(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        auto_info = data['auto_info']
    description = generate_description(auto_info)
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Принять', callback_data='accept')
    button2 = InlineKeyboardButton('Отклонить', callback_data='decline')
    keyboard.add(button1, button2)
    await callback_query.message.edit_text("[*] Вот новое описание: " + description + ". Не самое лучшее, что я видел, но сойдет. Одобряешь?", reply_markup=keyboard)

