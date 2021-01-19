# from aiogram.dispatcher.filters import CommandStart
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
# from data.config import allowed_users
# from loader import dp
# from aiogram import types
#
#
# @dp.inline_handler(text="")
# async def empty_query(query: types.InlineQuery):
#     await query.answer(
#         results=[
#             types.InlineQueryResultArticle(
#                 id="unknown",
#                 title="Input some request",
#                 input_message_content=types.InputTextMessageContent(
#                     message_text="No need to press the button"
#                 )
#             )
#         ],
#         cache_time=5
#     )
#
#
# @dp.inline_handler()
# async def some_query(query: types.InlineQuery):
#     user = query.from_user.id
#     if user not in allowed_users:
#         await query.answer(
#             results=[],
#             switch_pm_text="Bot unavailable. Connect to Bot",
#             switch_pm_parameter="connect_user",
#             cache_time=5
#         )
#         return
#
#     await query.answer(
#         results=[
#             types.InlineQueryResultArticle(
#                 id="1",
#                 title="Title that appears in inline mode",
#                 input_message_content=types.InputTextMessageContent(
#                     message_text="Text that will be sent on the click of the button"
#                 ),
#                 url="https://core.telegram.org/bots/api#inlinequeryresult",
#                 thumb_url="https://picsum.photos/200/300",
#                 description="Description in inline mode"
#             ),
#
#             types.InlineQueryResultVideo(
#                 id="4",
#                 video_url="https://youtu.be/ZoYVZmKSYFg",
#                 caption="Caption of the video",
#                 title="Some title",
#                 description="Some description",
#                 thumb_url="https://picsum.photos/200/300",
#                 mime_type="video/mp4",
#             )
#         ]
#     )
#
#
# @dp.message_handler(CommandStart(deep_link="connect_user"))
# async def connect_user(message: types.Message):
#     allowed_users.append(message.from_user.id)
#     await message.answer("You are now connected!",
#                          reply_markup=InlineKeyboardMarkup(
#                              inline_keyboard=[
#                                  [
#                                      InlineKeyboardButton(
#                                          text="Enter inline mode",
#                                          switch_inline_query_current_chat="Request"
#                                      )
#                                  ]
#                              ]
#                          ))
