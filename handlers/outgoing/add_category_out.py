from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import warning_text_uz_latin, warning_number_uz_latin, all_summary_main_out
from keyboards.default.start_keyboard import menu
from keyboards.inline.out_in_keys import yes_again_buttons
from loader import dp, db
from states.user_states import FinanceCategory


@dp.callback_query_handler(text='add_category', state='*')
async def add_category_call(call: types.CallbackQuery):
    await call.message.delete()

    await call.message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\n\n{warning_text_uz_latin}"
             f"\n\nKategoriya nomini kiriting:",
        reply_markup=menu
    )
    await FinanceCategory.add_category.set()


@dp.message_handler(state=FinanceCategory.add_category)
async def add_category(message: types.Message, state: FSMContext):

    if message.text.isalpha():
        await state.update_data(
            aco_category_name=message.text
        )

        await message.answer(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\nKategoriya: <b>{message.text}</b>"
                 f"\n\n{warning_text_uz_latin}"
                 f"\n\nSubkategoriya nomini kiriting:"
        )
        await FinanceCategory.add_subcategory.set()
    else:
        await message.answer(
            text=warning_text_uz_latin
        )


@dp.message_handler(state=FinanceCategory.add_subcategory)
async def add_subcategory_out(message: types.Message, state: FSMContext):

    if message.text.isalpha():
        await state.update_data(
            aco_subcategory_name=message.text
        )

        data = await state.get_data()

        await message.answer(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\nKategoriya: <b>{data['aco_category_name']}</b>"
                 f"\nSubkategoriya: <b>{message.text}</b>"
                 f"\n\nHarajat summasini kiriting"
                 f"{warning_number_uz_latin}"
        )
        await FinanceCategory.summary.set()
    else:
        await message.answer(
            text=warning_text_uz_latin
        )


@dp.message_handler(state=FinanceCategory.summary)
async def all_users_out(message: types.Message, state: FSMContext):

    if message.text.isdigit():
        data = await state.get_data()

        await state.update_data(
            aco_summary=int(message.text)
        )

        await message.answer(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\nKategoriya: <b>{data['aco_category_name']}</b>"
                 f"\nSubkategoriya: <b>{data['aco_subcategory_name']}</b>"
                 f"\nHarajat summasi: <b>{message.text}</b>"
                 f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
            reply_markup=yes_again_buttons
        )
        await FinanceCategory.summary_check.set()
    else:
        await message.answer(
            text=warning_number_uz_latin
        )


@dp.callback_query_handler(state=FinanceCategory.summary_check)
async def all_users_check_out(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = call.from_user.id
    category_name = data['aco_category_name']
    subcategory_name = data['aco_subcategory_name']
    summary = data['aco_summary']

    if call.data == "yes":
        await db.first_add_out(
            user_id=user_id,
            category_name=category_name,
            subcategory_name=subcategory_name,
            summary=summary
        )

        await all_summary_main_out(
            user_id=user_id,
            callback=call
        )

        await call.answer(
            text="Harajat ma'lumotlari saqlandi!",
            show_alert=True
        )
        await state.finish()

    elif call.data == "again":
        await call.message.edit_text(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\n\nKategoriya nomini kiriting:"
                 f"{warning_text_uz_latin}")
        await FinanceCategory.add_category.set()
