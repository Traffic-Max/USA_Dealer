from aiogram.dispatcher.filters.state import State, StatesGroup

class PostCreation(StatesGroup):
    waiting_for_content = State()
    waiting_for_auto_info = State()
    waiting_for_description_approval = State()

class StatusChange(StatesGroup):
    new_status = State()

# Здесь определяются все классы состояний.
