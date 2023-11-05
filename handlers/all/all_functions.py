from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from keyboards.inline.incoming_keyboards import incoming_main_menu
from keyboards.inline.outgoing_keyboards import categories_keyboard
from loader import db


#  CHECK SUMMARY OUTGOING
async def all_summary_main_out(user_id: int, callback: types.CallbackQuery, section_name: str, total: str,
                               currency: str):
    all_summ = await db.get_sum_all_out(
        user_id=user_id
    )
    if all_summ is None:
        all_summ = 0

    await callback.message.edit_text(
        text=f"<b>{section_name}</b>"
             f"\n\n{total}: <b>{all_summ} {currency}</b>",
        reply_markup=await categories_keyboard(user_id=user_id)
    )


# CHECK SUMMARY INCOMING
async def check_summary_main_inc(user_id: int, callback: types.CallbackQuery, section_name: str, total: str,
                                 currency: str, no_edit=False):
    all_summary = await db.summary_all_inc(
        user_id=user_id
    )

    if all_summary is None:
        all_summary = 0
    if no_edit:
        await callback.message.answer(
            text=f"<b>{section_name}</b>"
                 f"\n\n{total} <b>{all_summary}</b> {currency}",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )
    else:
        await callback.message.edit_text(
            text=f"<b>{section_name}</b>"
                 f"\n\n{total}: <b>{all_summary}</b> {currency}",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )


# BUTTONS GENERATOR

async def first_button_all_history_inc(
        current_page: int,
        database: list,
        call: types.CallbackQuery,
        state: FSMContext,
        back_name: str,
        currency: str,
        section_one: str,
        section_two: str,
        total: str,
        all_summary: int
):
    if len(database) % PAGE_COUNT == 0:
        all_pages = len(database) // PAGE_COUNT
    else:
        all_pages = len(database) // PAGE_COUNT + 1

    history = " "

    key = buttons_generator(current_page=current_page,
                            all_pages=all_pages,
                            subcategory=back_name,
                            incoming_main=True)
    for data in database[:PAGE_COUNT]:
        data_two = await db.summary_category_inc(
            user_id=call.from_user.id,
            incoming_name=data[0])
        history += f"{data[0]} | {data_two} {currency}\n"
    await call.message.answer(
        text=f"<b>{section_one} > {section_two}</b>"
             f"\n\n{history}\n{total}: {all_summary} {currency}",
        reply_markup=key
    )
    await state.update_data(
        current_page=current_page,
        all_pages=all_pages
    )
    history = " "


async def second_button_all_history_inc(
        call: types.CallbackQuery,
        current_page: int,
        all_pages: int,
        database: list,
        back_button: str,
        currency: str
):

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
                            subcategory=back_button, incoming_category=True)

    history = " "
    for data in all_messages:
        data_two = await db.summary_category_inc(
            user_id=call.from_user.id,
            incoming_name=data[0])
        history += f"{data[0]} | {data_two} {currency}\n"


async def generate_history_button_one(current_page: int, database: list, back_name: str, call: types.CallbackQuery,
                                      state: FSMContext, section_one: str, section_two: str,
                                      total: str, currency: str, summary_section: int = None, section_three: str = None,
                                      all_summary: int = None, incoming_category=False, two_columns=False,
                                      three_columns=False, summary_inc=False, summary_out=False):
    if len(database) % PAGE_COUNT == 0:
        all_pages = len(database) // PAGE_COUNT
    else:
        all_pages = len(database) // PAGE_COUNT + 1

    history = " "
    if two_columns:
        if summary_inc:
            key = buttons_generator(current_page=current_page, all_pages=all_pages,
                                    subcategory=back_name, incoming_category=incoming_category,
                                    incoming_main=True)

            for data in database[:PAGE_COUNT]:
                data_two = await db.summary_category_inc(
                    user_id=call.from_user.id,
                    incoming_name=data[0])
                history += f"{data[0]} | {data_two} {currency}\n"
            await call.message.answer(
                text=f"<b>{section_one} > {section_two}</b>"
                     f"\n\n{history}\n{total}: {all_summary} {currency}",
                reply_markup=key
            )
        elif summary_out:
            pass

        # for data in database[:PAGE_COUNT]:
        #     history += f"{data[0]} | {summary} {currency}\n"

    elif three_columns:
        key = buttons_generator(current_page=current_page, all_pages=all_pages,
                                subcategory=back_name, incoming_category=incoming_category)
        for data in database[:PAGE_COUNT]:
            history += f"{data[2]} | {data[0]} | {data[1]} {currency}\n"

        await call.message.answer(
            text=f"<b>{section_one} > {section_two} > {section_three}</b>"
                 f"\n\n{history}\n{total}: {summary_section} {currency}",
            reply_markup=key
        )
    await state.update_data(
        current_page=current_page,
        all_pages=all_pages
    )
    history = " "


async def generate_history_button_two(call: types.CallbackQuery, current_page: int, all_pages: int, database: list,
                                      back_name: str, section_one: str, section_two: str, currency: str, total: str,
                                      state: FSMContext, summary_section: int, all_summary: int = None,
                                      section_three: str = None, section_four: str = None, two_columns=False,
                                      three_columns=False, incoming_category=False, summary_inc=False,
                                      summary_out=False):
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
        if summary_inc:
            for data in all_messages:
                data_two = await db.summary_category_inc(
                    user_id=call.from_user.id,
                    incoming_name=data[0])
                history += f"{data[0]} | {data_two} {currency}\n"
        elif summary_out:
            pass

        await call.message.answer(text=f"<b>{section_one} > {section_two}</b>"
                                       f"\n\n{history}\n{total}: {all_summary} {currency}",
                                  reply_markup=key)
    elif three_columns:
        for data in all_messages:
            history += f"{data[2]} | {data[0]} | {data[1]} {currency}\n"

        await call.message.answer(
            text=f"<b>{section_one} > {section_two} > {section_three}</b>"
                 f"\n\n{history}\n{total}: {summary_section} {currency}",
            reply_markup=key
        )

    history = " "

    await state.update_data(
        current_page=current_page, all_pages=all_pages
    )


warning_text_uz_latin = ("Bot ishlashida muammo bo'lmasligi uchun faqat harflar kiritilishi hamda ularning "
                         "uzunligi 64 tadan oshmasligi lozim!")

warning_text_uz_kirill = ("Бот ишлашида муаммо бўлмаслиги учун киритилаётган матнда _, !, ? каби белгилардан"
                          "фойдаланмаслигингизни ҳамда 64 та белгидан кўп белги киритмаслигингизни илтимос қиламиз!")

# warning_text_ru = ("Bot ishlashida muammo bo'lmasligi uchun kiritilayotgan matnda _, !, ? kabi belgilardan "
#                          "foydalanmasligingizni hamda 64 ta belgidan ko'p belgi kiritmaslingizni iltimos qilamiz!")

warning_number_uz_latin = "\n\n(faqat raqam kiritilishi lozim!\nMasalan: 15000)"

warning_number_uz_kirill = "\n(faqat raqam kiritilishi lozim!):"

warning_number_ru = "\n(faqat raqam kiritilishi lozim!):"
