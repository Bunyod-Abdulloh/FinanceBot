import asyncio
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.builtin import CommandStart
from magic_filter import F

from keyboards.inline.out_in_keys import main_menu
from loader import dp, db, bot

category_name = ["Kommunal to`lovlar", "Internet", "Telefon"]
subcategory_name = ["Issiq suv", "Sovuq suv", "Elektr energiya", "Gaz", "Uy", "Mening raqamim"]


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):

    await message.answer(
        text="IqtisodchiRobotga xush kelibsiz!",
        reply_markup=await main_menu()
    )
    await state.finish()


@dp.message_handler(content_types=["video", "audio"])
async def send_media_group(message: types.Message):
    await asyncio.sleep(1)
    youtube = message.caption_entities[1].url
    caption = message.caption.split("Youtube")[0]

    if message.content_type == "video":
        file_id = message.video.file_id
    if message.content_type == "audio":
        file_id = message.audio.file_id

    #
    # user_id = int(message.from_user.id)
    # summary = 0
    #
    # for n in range(100):
    #     summary += 1
    #     await db.add_outgoing(
    #         category_name=category_name[0],
    #         subcategory_name=subcategory_name[0],
    #         user_id=user_id,
    #         summary=summary
    #     )
    #     await db.add_outgoing(
    #         category_name=category_name[0],
    #         subcategory_name=subcategory_name[1],
    #         user_id=user_id,
    #         summary=summary
    #     )
    #     await db.add_outgoing(
    #         category_name=category_name[0],
    #         subcategory_name=subcategory_name[2],
    #         user_id=user_id,
    #         summary=summary
    #     )
    #     await db.add_outgoing(
    #         category_name=category_name[0],
    #         subcategory_name=subcategory_name[3],
    #         user_id=user_id,
    #         summary=summary
    #     )
    #     await db.add_outgoing(
    #         category_name=category_name[1],
    #         subcategory_name=subcategory_name[4],
    #         user_id=user_id,
    #         summary=summary
    #     )
    #     await db.add_outgoing(
    #         category_name=category_name[2],
    #         subcategory_name=subcategory_name[5],
    #         user_id=user_id,
    #         summary=summary
    #     )
    # await db.add_outgoing(
    #             category_name="Telefon",
    #             subcategory_name='O\'zim',
    #             user_id=user_id, summary=summary
    #         )


# @dp.message_handler(text='olma', state='*')
# async def back_main_menu(message: types.Message, state: FSMContext):
#     await message.answer(
#         text='Bosh menu',
#     )
#     await state.set_state('olma')
#
#
# @dp.message_handler(is_media_group=True, state='olma', content_types=['any'])
# async def mediagroup(message: types.Message, album: List):
#     updates = await bot.get_updates()
#     media = types.MediaGroup()
#     print(f'{updates} UPDATES')
#     print(f'{album} ALBUM')
#     for update in updates:
#         if update == updates[-1]:
#             media.attach_photo(photo=update.message.photo[-1].file_id, caption="salommmmm")
#         else:
#             media.attach_photo(photo=update.message.photo[-1].file_id)
#     await message.answer_media_group(media=media)

medias = F.photo | F.video | F.document | F.audio | F.animation

import asyncio
import aioschedule
from aiogram.utils import executor


async def noon_print():
    print("It's noon!")


async def scheduler():
    aioschedule.every().day.at("19:31").do(noon_print)
    while True:
        await aioschedule.run_pending()
        # await asyncio.sleep(1)


async def on_startup(_):
    await asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)

