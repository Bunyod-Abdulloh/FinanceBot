from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def incoming_main_menu(user_id: int):
    user = await db.get_user_incoming(user_id=user_id)
    markup = InlineKeyboardMarkup(row_width=2)
    if user:
        for data in user:
            markup.add(
                InlineKeyboardButton(
                    text=f"{data[0]} | {data[1]} so'm",
                    callback_data=f"incoming_{data[0]}"
                )
            )
        markup.row(
            InlineKeyboardButton(
                text="ℹ️ Excel yuklab olish",
                callback_data="dowload_incoming"
            ),
            InlineKeyboardButton(
                text="📜 Kirimlar tarixi",
                callback_data="history_incoming"
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="back_incomingmain"
        ),
        InlineKeyboardButton(
            text="➕ Qo'shish",
            callback_data="incoming_add"
        )
    )
    return markup
