import logging

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


# Kategoriyalar uchun keyboard yasab olamiz
async def categories_keyboard():
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=1)

    categories = await db.get_categories()

    for category in categories:
        print(category)

        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, category=f"{category['category_name']}"
        )

        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=f"{category['category_name']}",
                                 callback_data=callback_data)
        )
    markup.insert(
        InlineKeyboardButton(text='➕ Add',
                             callback_data='add_category')
    )
    # Keyboardni qaytaramiz
    return markup


# Berilgan kategoriya ostidagi kategoriyalarni qaytaruvchi keyboard
async def subcategories_keyboard(category_name):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)

    # Kategoriya ostidagi kategoriyalarni bazadan olamiz
    subcategories = await db.get_subcategories_distinct(category_name)
    for subcategory in subcategories:

        button_text = f"{subcategory[0]}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
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
            text='➕ Add',
            callback_data=f'addsubcategory_{category_name}'
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='📝 Edit category',
            callback_data=f'editcategory_{category_name}'
        ))
    markup.row(
        InlineKeyboardButton(
            text="⬅️ Back",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1
            )
        )
    )
    return markup


def summary_or_item_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text='Soni',
            callback_data='item'
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='Kg',
            callback_data='item_kg'
        )
    )
    return markup


# Ostkategoriyaga tegishli mahsulotlar uchun keyboard yasaymiz
async def items_keyboard(category_name, subcategory_name):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=1)

    # Ost-kategorioyaga tegishli barcha mahsulotlarni olamiz
    items = await db.get_products(category_name, subcategory_name)
    for item in items:
        # Tugma matnini yasaymiz
        button_text = f"{item['productname']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_name,
            subcategory=subcategory_name,
            item_id=item["id"],
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data)
        )
    markup.insert(
        InlineKeyboardButton(
            text='➕ Add',
            callback_data=f'addproduct_{category_name}_{subcategory_name}'
        )
    )
    # Ortga qaytish tugmasi
    markup.row(
        InlineKeyboardButton(
            text="⬅️ Back",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,
                category=category_name
            ),
        )
    )
    return markup


# Berilgan mahsulot uchun Xarid qilish va Ortga yozuvlarini chiqaruvchi tugma keyboard
def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=2)

    markup.insert(
        InlineKeyboardButton(
            text='❌ Delete',
            callback_data=f'deleteproduct_{item_id}'
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text=f"➕ Add",
            callback_data=f"additem_{item_id}"
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="⬅️ Back",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category, subcategory=subcategory
            ),
        )
    )
    return markup
