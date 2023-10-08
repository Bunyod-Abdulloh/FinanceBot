from aiogram.dispatcher.filters.state import StatesGroup, State


class FinanceCategory(StatesGroup):
    add_category = State()
    add_product = State()
    summary_or_item = State()
    item = State()
    weight = State()
    price = State()


class FinanceSubcategory(StatesGroup):
    add_date = State()
    add_product = State()
    summary_or_item = State()
    item = State()
    weight = State()
    price = State()
