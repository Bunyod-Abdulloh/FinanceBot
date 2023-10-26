from aiogram.dispatcher.filters.state import StatesGroup, State


class FinanceCategory(StatesGroup):
    add_category = State()
    add_subcategory = State()
    summary = State()
    summary_check = State()


class FinanceSubcategory(StatesGroup):
    aso_subcategory = State()
    aso_summary = State()
    aso_summary_check = State()


class FinanceEdit(StatesGroup):
    category = State()
    subcategory = State()
    product = State()


class MoneyOut(StatesGroup):
    add_money = State()
    reduce_amount = State()


class PayHistoryOut(StatesGroup):
    one = State()
    subcategory = State()
    category = State()


class DownloadHistoryOut(StatesGroup):
    category = State()
    subcategory = State()
    product = State()


class IncomingStates(StatesGroup):
    add_name = State()
    add_summary = State()
    add_check = State()
