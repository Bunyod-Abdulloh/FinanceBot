from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import ADMINS
from keyboards.inline.out_in_keys import main_menu

from keyboards.inline.outgoing_keyboards import (
    menu_cd,
    categories_keyboard,
    subcategories_keyboard,
    items_keyboard
)
from loader import dp, db


@dp.message_handler(text="Bosh menyu", state="*")
async def show_menu(message: types.Message, state: FSMContext):
    await message.answer(
        text="IqtisodchiRobotga xush kelibsiz!",
        reply_markup=await main_menu()
    )
    await state.finish()


async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    user_id = str(message.from_user.id)

    if user_id in ADMINS:
        user_id = int(ADMINS[0])
    else:
        user_id = int(user_id)

    summary = await db.get_summary_out(
        all_outgoing=True,
        user_id=user_id
    )
    markup = await categories_keyboard(user_id=user_id)

    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz
    if isinstance(message, Message):
        await message.answer(text=f"<b>📤 Chiqim</b>"
                                  f"\n\n📤 Chiqim bo'limi uchun jami harajat: <b>{summary} so`m</b>",
                             reply_markup=markup)

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):
        call = message

        await call.message.edit_text(text=f"<b>📤 Chiqim</b>"
                                          f"\n\n📤 Chiqim bo'limi uchun jami harajat: <b>{summary} so`m</b>",
                                     reply_markup=markup)


async def list_subcategories(callback: CallbackQuery, category):
    markup = await subcategories_keyboard(category_name=category, user_id=callback.from_user.id)

    summa = await db.get_summary_out(
        subcategory=True,
        user_id=callback.from_user.id,
        category_name=category
    )
    await callback.message.edit_text(text=f"<b>📤 Chiqim > "
                                          f"{category}</b>"
                                          f"\n\n{category} uchun jami harajat: <b>{summa} so`m</b>",
                                     reply_markup=markup)


# Ost-kategoriyaga tegishli mahsulotlar ro'yxatini yuboruvchi funksiya
async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category_name=category,
                                  subcategory_name=subcategory,
                                  user_id=callback.from_user.id)
    summa = await db.get_summary_out(
        subcategory=True,
        user_id=callback.from_user.id,
        subcategory_name=subcategory
    )
    await callback.message.edit_text(text="<b>📤 Chiqim > "
                                          f"{category} > "
                                          f"{subcategory}</b>"
                                          f"\n\n{subcategory} uchun jami harajat: <b>{summa} so`m</b>",
                                     reply_markup=markup)


# Yuqoridagi barcha funksiyalar uchun yagona handler
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    :param call: Handlerga kelgan Callback query
    :param callback_data: Tugma bosilganda kelgan ma'lumotlar
    :param state: Levelni stateda saqlash
    """
    await state.finish()

    current_level = callback_data.get("level")
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")

    for key, value in callback_data.items():
        await state.update_data(
            {key: value}
        )

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items
    }

    current_level_function = levels[current_level]

    if subcategory == "0":
        await current_level_function(
            call, category=category
        )
    else:
        await current_level_function(
            call, category=category, subcategory=subcategory
        )
