from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text='📥 Kirim',
            callback_data='incomingmenu'
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


yes_again_buttons = InlineKeyboardMarkup(row_width=2)
yes_again_buttons.add(InlineKeyboardButton(text="✅ Ha",
                                           callback_data="yes"))
yes_again_buttons.insert(InlineKeyboardButton(text="♻️ Qayta kiritish",
                                              callback_data="again"))

back_download = InlineKeyboardMarkup(row_width=1)
back_download.add(
    InlineKeyboardButton(
        text="⬅️ Ortga",
        callback_data="back_download"
    )
)

back_history_inc_button = InlineKeyboardMarkup(row_width=1)
back_history_inc_button.add(
    InlineKeyboardButton(
        text="⬅️ Ortga",
        callback_data="back-history-inc"
    )
)

check_no_button = InlineKeyboardMarkup(row_width=2)
check_no_button.row(
    InlineKeyboardButton(
        text="✅ Ha",
        callback_data="yes_delete"
    ),
    InlineKeyboardButton(
        text="🛑 Yo'q",
        callback_data="no_delete"
    )
)
