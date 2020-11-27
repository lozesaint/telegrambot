from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionsOnStart(StatesGroup):
    users_pref_language = State()
    users_name = State()
    users_phone_number = State()
    users_address = State()
    users_email = State()
