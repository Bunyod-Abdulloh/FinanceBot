from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_float, replace_point_bottom_line, warning_text
from keyboards.default.start_keyboard import menu
from keyboards.inline.out_in_keys import yes_again_buttons
from keyboards.inline.outgoing_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceCategory


@dp.callback_query_handler(text='add_category', state='*')
async def add_category_call(call: types.CallbackQuery):
    await call.message.delete()

    await call.message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\n\n{warning_text}"
             f"\n\nKategoriya nomini kiriting:",
        reply_markup=menu
    )
    await FinanceCategory.add_category.set()


@dp.message_handler(state=FinanceCategory.add_category)
async def add_category(message: types.Message, state: FSMContext):

    category_name = await replace_point_bottom_line(message=message.text)

    await state.update_data(
        category_name=category_name
    )

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{category_name}</b>"
             f"\n\n{warning_text}"
             f"\n\nSubkategoriya nomini kiriting:"
    )
    await FinanceCategory.add_subcategory.set()


@dp.message_handler(state=FinanceCategory.add_subcategory)
async def add_subcategory_out(message: types.Message, state: FSMContext):

    subcategory_name = await replace_point_bottom_line(message=message.text)

    await state.update_data(
        subcategory_name=subcategory_name
    )

    data = await state.get_data()

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{data['category_name']}</b>"
             f"\nSubkategoriya: <b>{message.text}</b>"
             f"\n\nHarajat summasini kiriting"
             f"{raqam}"
    )
    await FinanceCategory.summary.set()


@dp.message_handler(state=FinanceCategory.summary)
async def all_users_out(message: types.Message, state: FSMContext):

    summary = await replace_float(message=message.text)

    data = await state.get_data()

    await state.update_data(
        summary=int(summary)
    )

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{data['category_name']}</b>"
             f"\nSubkategoriya: <b>{data['subcategory_name']}</b>"
             f"\nHarajat summasi: <b>{summary}</b>"
             f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=yes_again_buttons
    )
    await FinanceCategory.summary_check.set()


@dp.callback_query_handler(state=FinanceCategory.summary_check)
async def all_users_check_out(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = call.from_user.id
    category_name = data['category_name']
    subcategory_name = data['subcategory_name']
    summary = data['summary']

    if call.data == "yes":
        await db.first_add_out(
            user_id=user_id,
            category_name=category_name,
            subcategory_name=subcategory_name,
            summary=summary
        )
        await call.message.edit_text(
            text="<b>📤 Chiqim</b>",
            reply_markup=await categories_keyboard(user_id=user_id)
        )
        await call.answer(
            text="Harajat ma'lumotlari saqlandi!",
            show_alert=True
        )
        await state.finish()

    elif call.data == "again":
        await call.message.edit_text(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\n\nKategoriya nomini kiriting:")
        await FinanceCategory.add_category.set()
