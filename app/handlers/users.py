from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import app.models.stars as stars_models
from app.models.users import UserORM

import app.requests.users as user_db
import app.keyboards.users as user_kb
from app.middlewares.users import UserMiddleware
import app.states as st
import re
import datetime

user = Router()
user.message.middleware(UserMiddleware())
user.callback_query.middleware(UserMiddleware())

# user.message.middleware(BaseMiddleware())

# @user.message(Command("get_chat_id"))
# async def get_chat_id(message: Message):
#     await message.answer(f"Chat ID: {message.chat.id}")

@user.callback_query(F.data == 'check_subscribe')
@user.callback_query(F.data == 'back_to_main')
@user.message(CommandStart())
async def cmd_start(event: Message | CallbackQuery, user_info: UserORM, state: FSMContext):
    await state.clear()
    text = await user_db.get_start_text()
    text = text.replace("\\n", "\n")
    if isinstance(event, Message):
        await event.answer(text,
                           disable_web_page_preview=True,
                           reply_markup=user_kb.main_kb)
    elif isinstance(event, CallbackQuery):
        await event.answer('')
        await event.message.edit_text(text,
                           disable_web_page_preview=True,
                           reply_markup=user_kb.main_kb)


@user.callback_query(F.data == 'back_to_profile')
@user.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery, user_info: UserORM):
    await callback.answer('')
    number_of_referrals = await user_db.number_of_referrals(user_info.id)
    await callback.message.edit_text(f'Профиль:\n\n'
                                     f'Баланс: {user_info.balance} ⭐️\n'
                                     f'Куплено звёзд: {user_info.total_stars} ⭐️\n'
                                     f'Количество рефералов: {number_of_referrals} 👥',
                                     reply_markup=user_kb.profile_kb)


@user.callback_query(F.data == 'referral_system')
async def referral_system(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'От каждой покупки реферала ты получаешь 3%\n\n'
                                     f'🔗 Твоя личная ссылка: https://t.me/StarsShoppinbot?start={callback.from_user.id}',
                                     reply_markup=user_kb.back_to_profile_kb)


