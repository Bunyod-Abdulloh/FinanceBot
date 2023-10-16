
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.start_keyboard import menu
from keyboards.inline.out_keyboards import categories_keyboard, yes_no_buttons
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.callback_query_handler(text_contains='addsubcategory')
async def aso_step_one(call: types.CallbackQuery, state: FSMContext):
    category_name = call.data.split('_')[-1]
    await state.update_data(
        category_name=category_name
    )
    await call.message.delete()

    await call.message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{category_name}</b>"
             f"\n\nSubkategoriya nomini kiriting:",
        reply_markup=menu
    )
    await FinanceSubcategory.aso_subcategory.set()


@dp.message_handler(state=FinanceSubcategory.aso_subcategory)
async def aso_step_two(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{data['category_name']}</b>"
             f"\nSubkategoriya: <b>{message.text}</b>"
             f"\n\nHarajat summasini kiriting"
             f"(faqat raqam kiritilishi lozim!):")

    # await message.answer(
    #     text=f"Bo'lim: <b>📤 Chiqim</b>"
    #          f"\nKategoriya: <b>{data['category_name']}</b>"
    #          f"\nSubkategoriya: <b>{message.text}</b"
    #          f"\n\nHarajat summasini kiriting"
    #          f"(faqat raqam kiritilishi lozim!):"
    # )
    print('39 subcategory')
    await state.update_data(
        subcategory_name=message.text
    )
    await FinanceSubcategory.aso_summary.set()
    print('44 subcategory')

@dp.message_handler(state=FinanceSubcategory.aso_summary)
async def subcategory_summary_out(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await state.update_data(
        summary=int(message.text)
    )
    data = await state.get_data()

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{data['category_name']}</b>"
             f"\nSubkategoriya: <b>{data['subcategory_name']}</b>"
             f"\nHarajat summasi: <b>{message.text}</b>"
             f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=yes_no_buttons
    )
    await FinanceSubcategory.aso_summary_check.set()


@dp.callback_query_handler(state=FinanceSubcategory.aso_summary_check)
async def aso_summary_check(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = call.from_user.id
    category_name = data['category_name']
    subcategory_name = data['subcategory_name']
    summary = data['summary']

    if call.data == "yes_button":
        await db.first_add_out(
            user_id=user_id,
            category_name=category_name,
            subcategory_name=subcategory_name,
            summary=summary
        )
        await call.message.edit_text(
            text="Harajat bazaga qo'shildi!",
            reply_markup=await categories_keyboard(user_id=user_id)
        )
        await state.finish()

    elif call.data == "again_button":
        await call.message.edit_text(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\n\nKategoriya nomini kiriting:")
        await FinanceSubcategory.aso_add_subcategory.set()
