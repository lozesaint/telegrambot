from aiogram.dispatcher.filters.state import StatesGroup, State


class Purchase(StatesGroup):
    EnterQuantity = State()
    Approval = State()
    Payment = State()


class NewItem(StatesGroup):
    Name = State()
    Category = State()
    Photo = State()
    Sizes = State()
    Price = State()
    Confirm = State()


class Mailing(StatesGroup):
    Text = State()
    Language = State()


class Menu(StatesGroup):
    Main_Menu = State()
    Category = State()
    Item = State()
    Cart = State()
    About = State()
    Settings = State()


class Item(StatesGroup):
    Size = State()
    Quantity = State()


class Feedback(StatesGroup):
    Answer = State()


class Settings(StatesGroup):
    InputtingName = State()
    InputtingPhone = State()
    ChangeLanguage = State()


class Order(StatesGroup):
    PhoneNumber = State()
    Location = State()
    PayMethod = State()
    Confirmation = State()
