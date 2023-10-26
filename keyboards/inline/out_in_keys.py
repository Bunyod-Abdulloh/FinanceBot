from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


yes_no_buttons = InlineKeyboardMarkup(row_width=2)
yes_no_buttons.add(InlineKeyboardButton(text="✅ Ha",
                                        callback_data="yes_button"))
yes_no_buttons.insert(InlineKeyboardButton(text="♻️ Qayta kiritish",
                                           callback_data="again_button"))

back_download = InlineKeyboardMarkup(row_width=1)
back_download.add(
    InlineKeyboardButton(
        text="⬅️ Ortga",
        callback_data="back_download"
    )
)
