import math
import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import warning_text_uz_latin, warning_number_uz_latin
from keyboards.default.start_keyboard import menu
from keyboards.inline.out_in_keys import yes_again_buttons
from keyboards.inline.outgoing_keyboards import categories_keyboard, subcategories_keyboard
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.callback_query_handler(text_contains='addsubcategory')
async def aso_step_one(call: types.CallbackQuery, state: FSMContext):
    category_name = call.data.split('_')[-1]
    await state.update_data(
        aso_category_name=category_name
    )
    await call.message.delete()

    await call.message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{category_name}</b>"
             f"\n\n{warning_text_uz_latin}"
             f"\n\nSubkategoriya nomini kiriting:",
        reply_markup=menu
    )
    await FinanceSubcategory.aso_subcategory.set()


@dp.message_handler(state=FinanceSubcategory.aso_subcategory)
async def aso_step_two(message: types.Message, state: FSMContext):
    text = re.sub(r"[^\w\s]", "", message.text)

    data = await state.get_data()

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{data['aso_category_name']}</b>"
             f"\nSubkategoriya: <b>{text}</b>"
             f"\n\nHarajat summasini kiriting"
             f"\n{warning_number_uz_latin}:"
    )

    await state.update_data(
        aso_subcategory_name=subcategory_name
    )
    await FinanceSubcategory.aso_summary.set()


@dp.message_handler(state=FinanceSubcategory.aso_summary)
async def subcategory_summary_out(message: types.Message, state: FSMContext):

    if message.text.isdigit():
        await state.update_data(
            aso_summary=int(message.text)
        )
        data = await state.get_data()

        await message.answer(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\nKategoriya: <b>{data['aso_category_name']}</b>"
                 f"\nSubkategoriya: <b>{data['aso_subcategory_name']}</b>"
                 f"\nHarajat summasi: <b>{message.text} so'm</b>"
                 f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
            reply_markup=yes_again_buttons
        )
        await FinanceSubcategory.aso_summary_check.set()
    else:
        await message.answer(
            text=warning_number_uz_latin
        )


@dp.callback_query_handler(state=FinanceSubcategory.aso_summary_check)
async def aso_summary_check(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = call.from_user.id
    category_name = data['aso_category_name']
    subcategory_name = data['aso_subcategory_name']
    summary = data['aso_summary']

    if call.data == "yes":
        await db.first_add_out(
            user_id=user_id,
            category_name=category_name,
            subcategory_name=subcategory_name,
            summary=summary
        )

        await call.message.edit_text(
            text=f"<b>📤 Chiqim > {category_name}</b>",
            reply_markup=await subcategories_keyboard(
                category_name=category_name,
                user_id=user_id
            )
        )
        await call.answer(
            text="Harajat ma'lumotlari saqlandi!",
            show_alert=True)
        await state.finish()

    elif call.data == "again":
        await call.message.edit_text(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\nKategoriya: <b>{category_name}</b>"
                 f"\n\nSubkategoriya nomini kiriting:"
                 f"{warning_text_uz_latin}")
        await FinanceSubcategory.aso_subcategory.set()
