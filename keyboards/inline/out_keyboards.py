import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

# Turli tugmalar uchun CallbackData-obyektlarni yaratib olamiz
menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")


# Quyidagi funksiya yordamida menyudagi har bir element uchun calbback data yaratib olinadi
# Agar mahsulot kategoriyasi, ost-kategoriyasi va id raqami berilmagan bo'lsa 0 ga teng bo'ladi
def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(
        level=level, category=category, subcategory=subcategory, item_id=item_id
    )


# Bizning menu 3 qavat (LEVEL) dan iborat
# 0 - Kategoriyalar
# 1 - Ost-kategoriyalar
# 2 - Mahsulotlar
# 3 - Yagona mahsulot


async def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text='📥 Kirim',
            callback_data='incoming'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='📤 Chiqim',
            callback_data='outgoing'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='📔 Yon daftar',
            callback_data='notebook'
        )
    )
    return markup


# Kategoriyalar uchun keyboard yasab olamiz
async def categories_keyboard(user_id: int):
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=2)

    categories = await db.get_categories_out(user_id=user_id)

    if categories:
        for category in categories:
            callback_data = make_callback_data(
                level=CURRENT_LEVEL + 1, category=f"{category['category_name']}"
            )
            markup.add(
                InlineKeyboardButton(text=f"{category['category_name']}",
                                     callback_data=callback_data)
            )
        markup.add(
            InlineKeyboardButton(text='➕ Kategoriya qo\'shish',
                                 callback_data='add_category')
        )
    else:
        markup.add(
            InlineKeyboardButton(text='➕ Kategoriya qo\'shish',
                                 callback_data='add_category')
        )
    markup.add(
        InlineKeyboardButton(
            text='⬅️ Ortga',
            callback_data='back_main_menu'
        )
    )
    return markup


# Berilgan kategoriya ostidagi kategoriyalarni qaytaruvchi keyboard
async def subcategories_keyboard(category_name, user_id: int):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=3)

    subcategories = await db.get_subdistinct_out(category_name=category_name, user_id=user_id)

    for subcategory in subcategories:

        button_text = f"{subcategory[0]}"

        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_name,
            subcategory=subcategory[0],
        )
        markup.add(
            InlineKeyboardButton(text=button_text,
                                 callback_data=callback_data)
        )

    markup.add(
        InlineKeyboardButton(
            text='➕ Subkategoriya qo\'shish',
            callback_data=f'addsubcategory_{category_name}'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='📝 Kategoriyani o\'zgartirish',
            callback_data=f'editcategory_{category_name}'
        ))
    markup.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1
            )
        )
    )
    return markup


# Ostkategoriyaga tegishli mahsulotlar uchun keyboard yasaymiz
async def items_keyboard(category_name, subcategory_name, user_id: int):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=2)

    # Ost-kategorioyaga tegishli barcha mahsulotlarni olamiz
    items = await db.get_products_out(subcategory_name=subcategory_name, user_id=user_id)

    # for item in items:
        # Tugma matnini yasaymiz
        # button_text = f"{item['productname']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        # callback_data = make_callback_data(
        #     level=CURRENT_LEVEL + 1,
        #     category=category_name,
        #     subcategory=subcategory_name,
        #     item_id=item["id"],
        # )
        # markup.add(
        #     InlineKeyboardButton(
        #         text=button_text,
        #         callback_data=callback_data)
        # )
    markup.add(
        InlineKeyboardButton(
            text='➕ Qo\'shish',
            callback_data=f'addproduct_{category_name}_{subcategory_name}'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='📝 Subkategoriyani o\'zgartirish',
            callback_data=f'editsubcategory_{subcategory_name}'
        )
    )
    # Ortga qaytish tugmasi
    markup.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,
                category=category_name
            ),
        )
    )
    return markup


def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(
            text=f"➕ Add",
            callback_data=f"additem_{item_id}"
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='❌ Delete',
            callback_data=f'deleteproduct_{item_id}'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='📝 Edit product',
            callback_data=f'editproduct_{item_id}'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category, subcategory=subcategory
            ),
        )
    )
    return markup


yes_no_buttons = InlineKeyboardMarkup(row_width=2)
yes_no_buttons.add(InlineKeyboardButton(text="✅ Ha",
                                        callback_data="yes_button"))
yes_no_buttons.insert(InlineKeyboardButton(text="♻️ Qayta kiritish",
                                           callback_data="again_button"))
