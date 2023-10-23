from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PAGE_COUNT = 50


def buttons_generator(current_page: int, all_pages: int, subcategory: str, category=False):
    key = InlineKeyboardMarkup(
        row_width=3
    )
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="prev"
        )
    )
    key.insert(
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"pages_{current_page}"
        )
    )
    key.insert(
        InlineKeyboardButton(
            text="Oldinga ➡️",
            callback_data="next"
        )
    )
    if category:
        key.add(
            InlineKeyboardButton(
                text=f"↩️ {subcategory}ga qaytish",
                callback_data="back_category"
            )
        )
    else:
        key.add(
            InlineKeyboardButton(
                text=f"↩️ {subcategory}ga qaytish",
                callback_data="back_sub"
            )
        )
    return key
