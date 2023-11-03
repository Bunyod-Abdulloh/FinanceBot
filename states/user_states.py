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
    delete_subcategory = State()


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


# Incoming States
class IncomingMainMenu(StatesGroup):
    add_name = State()
    add_summary = State()
    add_check = State()


class IncomingCategory(StatesGroup):
    add_name = State()
    add_summary = State()
    check_summary = State()


class PayHistoryIncoming(StatesGroup):
    category = State()
    back_main = State()
    chi_one = State()


class EditIncoming(StatesGroup):
    add_name = State()
    add_summary = State()
    check = State()
