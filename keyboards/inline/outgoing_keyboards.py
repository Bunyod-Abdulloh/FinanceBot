from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

menu_cd = CallbackData("show_menu", "level", "category", "subcategory")


def make_callback_data(level, category="0", subcategory="0"):
    return menu_cd.new(
        level=level, category=category, subcategory=subcategory
    )


# Kategoriyalar uchun keyboard yasab olamiz
async def categories_keyboard(user_id: int):
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=2)

    categories = await db.get_categories_out(user_id=user_id)

    if categories:
        for category in categories:
            summary = await db.get_sum_category(user_id=user_id, category_name=category[0])
            callback_data = make_callback_data(
                level=CURRENT_LEVEL + 1, category=f"{category[0]}"
            )
            markup.add(
                InlineKeyboardButton(
                    text=f"{category[0]} | {summary} so'm",
                    callback_data=callback_data
                )
            )
        markup.row(
            InlineKeyboardButton(
                text="ℹ️ Excel yuklab olish",
                callback_data="downloadall"
            ),
            InlineKeyboardButton(
                text="📜 To'lovlar tarixi",
                callback_data=f"historycategory"
            )
        )
        markup.row(
            InlineKeyboardButton(
                text='⬅️ Ortga',
                callback_data='back_main_menu'
            ),
            InlineKeyboardButton(
                text='➕ Qo\'shish',
                callback_data='add_category'
            )
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text='⬅️ Ortga',
                callback_data='back_main_menu'
            ),
            InlineKeyboardButton(
                text='➕ Qo\'shish',
                callback_data='add_category'
            )
        )
    return markup


async def subcategories_keyboard(category_name, user_id: int):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=3)

    subcategories = await db.get_subdistinct_out(category_name=category_name, user_id=user_id)

    for subcategory in subcategories:
        summary = await db.get_sum_subcategory(user_id=user_id, subcategory_name=subcategory[0])
        button_text = f"{subcategory[0]} | {summary} so'm"

        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_name,
            subcategory=subcategory[0],
        )
        markup.add(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=f'📝 {category_name} o\'zgartirish',
            callback_data=f'editcategory'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="📜 To'lovlar tarixi",
            callback_data=f"historysub_{category_name}"
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1
            )
        ),
        InlineKeyboardButton(
            text='➕ Qo\'shish',
            callback_data=f'addsubcategory_{category_name}'
        )
    )
    return markup


async def items_keyboard(category_name, subcategory_name, user_id: int):
    CURRENT_LEVEL = 2

    subcategory = await db.get_products_out(subcategory_name=subcategory_name, user_id=user_id)

    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(
            text="➕ Summa qo'shish",
            callback_data=f"addmoney_{subcategory[0]}"
        ),
        InlineKeyboardButton(
            text="📜 To'lovlar tarixi",
            callback_data=f"historyproduct_{subcategory_name}"
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f'📝 {subcategory_name} o\'zgartirish',
            callback_data=f'editsubcategory'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f'❌ {subcategory_name} o\'chirish',
            callback_data=f'deletesubcategory_{subcategory_name}'
        )
    )
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
