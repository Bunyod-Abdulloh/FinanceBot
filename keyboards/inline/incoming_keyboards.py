from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def incoming_main_menu(user_id: int):
    user = await db.get_userall_inc(user_id=user_id,
                                    distinct=True)

    markup = InlineKeyboardMarkup(row_width=2)
    if user:
        for data in user:
            summary = await db.summary_category_inc(
                user_id=user_id,
                incoming_name=data[0]
            )
            markup.add(
                InlineKeyboardButton(
                    text=f"{data[0]} | {summary} so'm",
                    callback_data=f"incoming_{data[0]}"
                )
            )
        markup.row(
            InlineKeyboardButton(
                text="ℹ️ Excel yuklab olish",
                callback_data="download-inc"
            ),
            InlineKeyboardButton(
                text="📜 Kirimlar tarixi",
                callback_data="historymain-inc"
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="back-main-menu"
        ),
        InlineKeyboardButton(
            text="➕ Qo'shish",
            callback_data="inc-add"
        )
    )
    return markup


async def incoming_category(user_id: int, incoming_name: str):
    markup = InlineKeyboardMarkup(row_width=2)

    incoming = await db.get_user_inc(
        user_id=user_id,
        incoming_name=incoming_name
    )
    markup.row(
        InlineKeyboardButton(
            text="➕ Summa qo'shish",
            callback_data=f"addsummaryinc_{incoming[0][0]}"
        ),
        InlineKeyboardButton(
            text="📜 Kirimlar tarixi",
            callback_data=f"historycategoryinc_{incoming[0][0]}"
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f"📝 {incoming[0][0]}ni o'zgatirish",
            callback_data=f"editinc_{incoming[0][0]}"
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f'❌ {incoming[0][0]}ni o\'chirish',
            callback_data=f'deleteinc_{incoming[0][0]}'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="back-inc-main"
        )
    )
    return markup
