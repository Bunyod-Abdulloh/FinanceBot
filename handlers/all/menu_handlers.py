from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import ADMINS
from keyboards.inline.out_keyboards import (
    menu_cd,
    categories_keyboard,
    subcategories_keyboard,
    items_keyboard,
    item_keyboard, main_menu,
)
from loader import dp, db


@dp.message_handler(text="Bosh menyu", state="*")
async def show_menu(message: types.Message, state: FSMContext):
    await message.answer(
        text=message.text,
        reply_markup=await main_menu()
    )
    await state.finish()


async def list_categories(message: Union[CallbackQuery, Message], **kwargs):

    user_id = str(message.from_user.id)

    if user_id in ADMINS:
        user_id = int(ADMINS[0])
    else:
        user_id = int(user_id)

    markup = await categories_keyboard(user_id=user_id)

    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz
    if isinstance(message, Message):
        await message.answer("Bo'lim tanlang", reply_markup=markup)

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):
        call = message

        await call.message.edit_text(text="Bo'lim: <b>📤 Chiqim</b>",
                                     reply_markup=markup)


async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category_name=category, user_id=int(callback.from_user.id))

    summa = await db.get_sum_category(user_id=int(callback.from_user.id),
                                      category_name=category)

    await callback.message.edit_text(text=f"Bo'lim: <b>📤 Chiqim</b>"
                                          f"\nKategoriya: <b>{category}</b>"
                                          f"\n\n{category} uchun jami harajat: <b>{summa} so'm</b>",
                                     reply_markup=markup)
# Ushbu kategoriyadagi


# Ost-kategoriyaga tegishli mahsulotlar ro'yxatini yuboruvchi funksiya
async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category_name=category,
                                  subcategory_name=subcategory,
                                  user_id=int(callback.from_user.id))
    summa = await db.get_sum_subcategory(user_id=callback.from_user.id,
                                         subcategory_name=subcategory)

    await callback.message.edit_text(text="Bo'lim: <b>📤 Chiqim</b>"
                                          f"\nKategoriya: <b>{category}</b>"
                                          f"\nSubkategoriya: <b>{subcategory}</b>"                                          
                                          f"\n\n{subcategory} uchun jami harajat: <b>{summa} so'm</b>",
                                     reply_markup=markup)


# Biror mahsulot uchun Xarid qilish tugmasini yuboruvchi funksiya
async def show_item(callback: CallbackQuery, category, subcategory, item_id):
    markup = item_keyboard(category, subcategory, item_id)

    # Mahsulot haqida ma'lumotni bazadan olamiz
    item = await db.get_product_out(item_id)
    weight_or_item = item['weight_or_item']
    text = (f"Category: <b>{category}</b>"
            f"\nSubcategory: <b>{subcategory}</b>"
            f"\nMahsulot: <b>{item['productname']}\n</b>")

    if weight_or_item == 'kg':
        text += (f"Miqdori: <b>{item['item']} {item['weight_or_item']}</b>"
                 f"\nKilosi: <b>{item['price']} so'm</b>"
                 f"\n\nJami: <b>{item['summary']} so'm</b>")
    else:
        text += (f"Miqdori: <b>{item['item']} {item['weight_or_item']}</b>"
                 f"\nDonasi: <b>{item['price']} so'm</b>"
                 f"\n\nJami: <b>{item['summary']} so'm</b>")

    await callback.message.edit_text(text=text, reply_markup=markup)


# Yuqoridagi barcha funksiyalar uchun yagona handler
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Handlerga kelgan Callback query
    :param callback_data: Tugma bosilganda kelgan ma'lumotlar
    """

    # Foydalanuvchi so'ragan Level (qavat)
    current_level = callback_data.get("level")

    # Foydalanuvchi so'ragan Kategoriya
    category = callback_data.get("category")

    # Ost-kategoriya (har doim ham bo'lavermaydi)
    subcategory = callback_data.get("subcategory")

    # Mahsulot ID raqami (har doim ham bo'lavermaydi)
    item_id = callback_data.get("item_id")

    # Har bir Level (qavatga) mos funksiyalarni yozib chiqamiz
    levels = {
        "0": list_categories,  # Kategoriyalarni qaytaramiz
        "1": list_subcategories,  # Ost-kategoriyalarni qaytaramiz
        "2": list_items,  # Mahsulotlarni qaytaramiz
        "3": show_item,  # Mahsulotni ko'rsatamiz
    }

    # Foydalanuvchidan kelgan Level qiymatiga mos funksiyani chaqiramiz
    current_level_function = levels[current_level]

    # Tanlangan funksiyani chaqiramiz va kerakli parametrlarni uzatamiz
    await current_level_function(
        call, category=category, subcategory=subcategory, item_id=item_id
    )
