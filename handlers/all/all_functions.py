from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from keyboards.inline.incoming_keyboards import incoming_main_menu
from keyboards.inline.outgoing_keyboards import categories_keyboard
from loader import db


async def replace_point_bottom_line(message):
    if "'" in message:
        incoming = message.replace("'", "`")

    elif "_" in message:
        incoming = message.replace("_", "")

    else:
        incoming = message

    return incoming


async def replace_float(message):
    if "." in message:
        incoming = message.replace(".", "")

    elif "," in message:
        incoming = message.replace(",", "")

    else:
        incoming = message

    return int(incoming)


#  CHECK SUMMARY OUTGOING
async def all_summary_main_out(user_id: int, callback: types.CallbackQuery):
    all_summ = await db.get_sum_all_out(
        user_id=user_id
    )
    if all_summ is None:
        all_summ = 0

    await callback.message.edit_text(
        text=f"<b>📤 Chiqim</b>"
             f"\n\n📤 Chiqim bo'limi uchun jami harajat: <b>{all_summ} so'm</b>",
        reply_markup=await categories_keyboard(user_id=user_id)
    )


# CHECK SUMMARY INCOMING
async def check_summary_main_inc(user_id: int, callback: types.CallbackQuery, no_edit=False):
    all_summary = await db.summary_all_inc(
        user_id=user_id
    )

    if all_summary is None:
        all_summary = 0
    if no_edit:
        await callback.message.answer(
            text=f"<b>📥 Kirim bo'limi</b>"
                 f"\n\n📥 Kirim bo'limi uchun jami: <b>{all_summary}</b> so'm",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )
    else:
        await callback.message.edit_text(
            text=f"<b>📥 Kirim bo'limi</b>"
                 f"\n\n📥 Kirim bo'limi uchun jami: <b>{all_summary}</b> so'm",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )


# BUTTONS GENERATOR
async def generate_history_button_one(current_page: int, database: list, back_name: str, all_summary: int,
                                      call: types.CallbackQuery, state: FSMContext, section_one: str, section_two: str,
                                      section_three: str, total: str, currency: str, incoming_category=False,
                                      two_columns=False, three_columns=False):
    if len(database) % PAGE_COUNT == 0:
        all_pages = len(database) // PAGE_COUNT
    else:
        all_pages = len(database) // PAGE_COUNT + 1

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory=back_name, incoming_category=incoming_category)

    history = " "
    if two_columns:
        pass
    elif three_columns:
        for data in database[:PAGE_COUNT]:
            history += f"{data[2]} | {data[0]} | {data[1]} {currency}\n"

    await call.message.answer(
        text=f"<b>{section_one} > {section_two} > {section_three}</b>"
             f"\n\n{history}\n{total}: {all_summary} {currency}",
        reply_markup=key
    )
    await state.update_data(
        current_page=current_page,
        all_pages=all_pages
    )
    history = " "


async def generate_history_button_two(call: types.CallbackQuery, current_page: int, all_pages: int, database: list,
                                      back_name: str, section_one: str, section_two: str, currency: str, total: str,
                                      all_summary: int, state: FSMContext, section_three: str = None,
                                      section_four: str = None, two_columns=False, three_columns=False,
                                      incoming_category=False):
    if call.data == "prev":
        if current_page == 1:
            current_page = all_pages
        else:
            current_page -= 1
    if call.data == 'next':
        if current_page == all_pages:
            current_page = 1
        else:
            current_page += 1

    all_messages = database[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory=back_name, incoming_category=incoming_category)

    history = " "

    if two_columns:
        for data in all_messages:
            history += f"{data[0]} | {data[1]} {currency}\n"

        await call.message.answer(text=f"<b>{section_one} > {section_two} > {section_three} > {section_four}</b>"
                                       f"\n\n{history}\n{total}: {all_summary} {currency}",
                                  reply_markup=key)
    elif three_columns:
        for data in all_messages:
            history += f"{data[2]} | {data[0]} | {data[1]} {currency}\n"

        await call.message.answer(
            text=f"<b>{section_one} > {section_two} > {section_three}</b>"
                 f"\n\n{history}\n{total}: {all_summary} {currency}",
            reply_markup=key
        )

    history = " "

    await state.update_data(
        current_page=current_page, all_pages=all_pages
    )


warning_text_uz_latin = ("Bot ishlashida muammo bo'lmasligi uchun 64 ta belgidan ko'p belgi kiritmaslingizni hamda "
                         "faqat harflardan foydalanishingizni iltimos qilamiz!")

warning_text_uz_kirill = ("Бот ишлашида муаммо бўлмаслиги учун киритилаётган матнда _, !, ? каби белгилардан"
                          "фойдаланмаслигингизни ҳамда 64 та белгидан кўп белги киритмаслигингизни илтимос қиламиз!")

# warning_text_ru = ("Bot ishlashida muammo bo'lmasligi uchun kiritilayotgan matnda _, !, ? kabi belgilardan "
#                          "foydalanmasligingizni hamda 64 ta belgidan ko'p belgi kiritmaslingizni iltimos qilamiz!")

warning_number_uz_latin = "\n\n(faqat raqam kiritilishi lozim!\nMasalan: 15000)"

warning_number_uz_kirill = "\n(faqat raqam kiritilishi lozim!):"

warning_number_ru = "\n(faqat raqam kiritilishi lozim!):"
