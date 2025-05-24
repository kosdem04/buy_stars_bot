from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import app.models.stars as stars_models
from app.models.users import UserORM

import app.requests.users as user_db
import app.keyboards.users as user_kb
from app.middlewares.users import UserMiddleware, UserSimpleMiddleware
import app.states as st
import re
import datetime


user_start_router = Router()
user = Router()
user_start_router.message.middleware(UserSimpleMiddleware())
user_start_router.callback_query.middleware(UserSimpleMiddleware())
user.message.middleware(UserMiddleware())
user.callback_query.middleware(UserMiddleware())

# user.message.middleware(BaseMiddleware())


@user_start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    referrer_id = args if args else None
    referral_id = message.from_user.id
    if referrer_id:
        await user_db.add_referral(referrer_id, referral_id)
    text = await user_db.get_start_text()
    text = text.replace("\\n", "\n")
    await message.answer(text,
                           disable_web_page_preview=True,
                           reply_markup=user_kb.main_kb)


@user.callback_query(F.data == 'check_subscribe')
@user.callback_query(F.data == 'back_to_main')
async def callback_cmd_start(callback: CallbackQuery, user_info: UserORM, state: FSMContext):
    await state.clear()
    text = await user_db.get_start_text()
    text = text.replace("\\n", "\n")
    await callback.answer('')
    await callback.message.edit_text(text,
                       disable_web_page_preview=True,
                       reply_markup=user_kb.main_kb)


@user.callback_query(F.data == 'back_to_profile')
@user.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery, user_info: UserORM):
    await callback.answer('')
    number_of_referrals = await user_db.number_of_referrals(user_info.id)
    await callback.message.edit_text(f'Username {callback.from_user.username}:\n\n'
                                     f'Баланс: {user_info.balance} ⭐️\n'
                                     f'Куплено звёзд: {user_info.total_stars} ⭐️\n'
                                     f'Количество рефералов: {number_of_referrals} 👥',
                                     reply_markup=user_kb.profile_kb)


@user.callback_query(F.data == 'referral_system')
async def referral_system(callback: CallbackQuery, bot: Bot):
    await callback.answer('')
    me = await bot.get_me()
    await callback.message.edit_text(f'От каждой покупки реферала ты получаешь 3%\n\n'
                                     f'🔗 Твоя личная ссылка: https://t.me/{me.username}?start={callback.from_user.id}',
                                     disable_web_page_preview=True,
                                     reply_markup=user_kb.back_to_profile_kb)


