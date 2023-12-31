from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PAGE_COUNT = 25


def buttons_generator(current_page: int, all_pages: int, subcategory: str = None, category=False, incoming_main=False,
                      incoming_category=False):
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
    elif incoming_main:
        key.add(
            InlineKeyboardButton(
                text="↩️ 📥 Kirim bo'limiga qaytish",
                callback_data="back-inc-main"
            )
        )
    elif incoming_category:
        key.add(
            InlineKeyboardButton(
                text=f"↩️ {subcategory}ga qaytish",
                callback_data="back-inc-category"
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
