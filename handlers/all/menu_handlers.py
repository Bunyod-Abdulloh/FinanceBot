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
    item_keyboard,
)
from loader import dp, db


@dp.message_handler(text="Bosh menyu", state="*")
async def show_menu(message: types.Message, state: FSMContext):
    await list_categories(message)
    await state.finish()


# Kategoriyalarni qaytaruvchi funksiya. Callback query yoki Message qabul qilishi ham mumkin.
# **kwargs yordamida esa boshqa parametrlarni ham qabul qiladi: (category, subcategory, item_id)
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Keyboardni chaqiramiz
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

        await call.message.edit_text(text='Bosh menyu',
                                     reply_markup=markup)


# Ost-kategoriyalarni qaytaruvchi funksiya
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category_name=category, user_id=int(callback.from_user.id))
    # subcategories_summary = await db.get_subsummary_out(
    #     category_name=category,
    #     user_id=callback.from_user.id
    # )

    summ = 0
    # for summary in subcategories_summary:
    #     summ += summary[0]

    await callback.message.edit_text(text=f'Category: <b>{category}</b>'
                                          f'\n\nJami harajat: <b>{summ} so\'m</b>',
                                     reply_markup=markup)


# Ost-kategoriyaga tegishli mahsulotlar ro'yxatini yuboruvchi funksiya
async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category_name=category,
                                  subcategory_name=subcategory,
                                  user_id=int(callback.from_user.id))
    products_summary = await db.get_products_out(
        date=subcategory,
        user_id=callback.from_user.id
    )

    summ = 0
    for summary in products_summary:
        summ += summary[7]

    await callback.message.edit_text(text=f"Category: <b>{category}</b>"
                                          f"\nSubcategory: <b>{subcategory}</b>"
                                          f"\n\nJami harajat: <b>{summ} so'm</b>",
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
