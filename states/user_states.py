from aiogram.dispatcher.filters.state import StatesGroup, State


class FinanceUser(StatesGroup):
    add_category = State()
    add_product = State()
    summary_or_item = State()
    item = State()
    kg = State()
    summary = State()
    price = State()


class FinanceSubcategory(StatesGroup):
    add_date = State()
    add_product = State()
    summary_or_item = State()
    item = State()
    summary = State()
    price = State()
