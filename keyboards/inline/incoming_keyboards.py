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


async def incoming_second_page(user_id: int, incoming_name: str):
    markup = InlineKeyboardMarkup(row_width=2)

    incoming = await db.get_user_incoming_(
        user_id=user_id,
        incoming_name=incoming_name
    )
    print(incoming)
    markup.row(
        InlineKeyboardButton(
            text="➕ Summa qo'shish",
            callback_data=f"addincoming_{incoming[0]}"
        ),
        InlineKeyboardButton(
            text="📜 Kirimlar tarixi",
            callback_data=f"historyincoming_{incoming[0]}"
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f"{incoming_name[0]} o'zgatirish",
            callback_data=f"editincoming_{incoming[0]}"
        )
    )
    InlineKeyboardButton(
        text=f'❌ {incoming_name[0]} o\'chirish',
        callback_data=f'deleteincoming_{incoming[0]}'
    )
    markup.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="back_incoming"
        )
    )
    return markup
