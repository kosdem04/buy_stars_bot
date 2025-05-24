from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError

import app.models.stars as stars_models
from app.models.users import UserORM
import app.keyboards.stars as star_kb
import app.keyboards.admins as admin_kb
from app.middlewares.users import UserMiddleware
import app.states.stars as stars_states
from decimal import Decimal
import app.requests.stars as star_db
from config import CHAT_FOR_WITHDRAWAL_ID


star = Router()
star.message.middleware(UserMiddleware())
star.callback_query.middleware(UserMiddleware())


"""
ВЫВОД ЗВЁЗД
"""
@star.callback_query(F.data == 'back_to_withdrawal_stars')
@star.callback_query(F.data == 'withdrawal_stars')
async def withdrawal_stars(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.edit_text('Выберите сумму для вывода',
                                     reply_markup=await star_kb.withdrawal_options_kb())


@star.callback_query(F.data.startswith('withdrawal-option_'))
async def withdrawal_stars_sure(callback: CallbackQuery, user_info: UserORM, state: FSMContext,):
    amount = callback.data.split('_')[1]
    await state.update_data(withdrawal_amount=amount)
    if user_info.balance < Decimal(amount):
        await callback.answer('К сожалению, у Вас недостаточно звёзд на балансе')
    else:
        await callback.message.edit_text(f'Вы уверены, что хотите вывести {amount} звёзд?',
                                         reply_markup=star_kb.sure_withdrawal_kb)


@star.callback_query(F.data == 'enter_withdrawal_option')
async def enter_withdrawal_option(callback: CallbackQuery, state: FSMContext,):
    await callback.answer('')
    msg = await callback.message.edit_text('Введите сумму для вывода',
                                     reply_markup=star_kb.withdrawal_stars_cancel_kb)
    await state.set_state(stars_states.WithdrawalStarState.enter_amount)
    await state.update_data(bot_msg_id=msg.message_id)


@star.message(stars_states.WithdrawalStarState.enter_amount)
async def enter_withdrawal_option_sure(message: Message, user_info: UserORM, state: FSMContext):
    data = await state.get_data()
    bot_msg_id = data.get("bot_msg_id")
    if bot_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_msg_id)
        except:
            pass
    try:
        amount = int(message.text)
        if amount < 500:
            raise ValueError
    except ValueError:
        msg = await message.answer('Введите сумму для вывода',
                             reply_markup=star_kb.withdrawal_stars_cancel_kb
                             )
        await state.update_data(bot_msg_id=msg.message_id)
        return
    if user_info.balance < amount:
        msg = await message.answer('К сожалению, у Вас недостаточно звёзд на балансе\n'
                             'Попробуйте снова',
                             reply_markup=star_kb.withdrawal_stars_cancel_kb
                             )
        await state.update_data(bot_msg_id=msg.message_id)
        return
    await state.update_data(withdrawal_amount=amount)
    await message.answer(f'Вы уверены, что хотите вывести {amount} звёзд?',
                                     reply_markup=star_kb.sure_withdrawal_kb)


@star.callback_query(F.data == 'withdrawal_yes')
async def withdrawal_yes(callback: CallbackQuery, user_info: UserORM, bot: Bot, state: FSMContext,):
    await callback.answer('')
    data = await state.get_data()
    amount = data.get("withdrawal_amount")
    new_balance = user_info.balance - int(amount)
    withdrawal_id = await star_db.withdrawal_stars(user_info.id, new_balance, amount)
    await bot.send_message(chat_id=CHAT_FOR_WITHDRAWAL_ID,
                           text=f'‼️ ВНИМАНИЕ ‼️\n'
                                f'<b>Запрос на вывод:</b>\n\n'
                                f'<b>Пользователь:</b> {callback.from_user.username}\n'
                                f'<b>Количество звёзд:</b> {amount}🌟',
                           reply_markup=await admin_kb.withdrawal_moderation(withdrawal_id))
    await callback.message.edit_text('Запрос на вывод средств отправлен',
                                     reply_markup=star_kb.back_to_profile_kb)
    await state.clear()


"""
ПОКУПКА ЗВЁЗД
"""
@star.callback_query(F.data == 'back_to_select_user_stars')
@star.callback_query(F.data == 'buy_stars')
async def buy_stars(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    text = await star_db.get_buy_star_text()
    text = text.replace("\\n", "\n")
    await callback.message.edit_text(text,
                                     disable_web_page_preview=True,
                                     reply_markup=await star_kb.buy_stars_select_user_kb(callback.from_user.username))
    # await callback.message.edit_text(text,
    #                                  disable_web_page_preview=True,
    #                                  reply_markup=await star_kb.buy_options_kb())


@star.callback_query(F.data.startswith('send-stars-to-user@'))
async def buy_stars_select_option(callback: CallbackQuery, user_info: UserORM, state: FSMContext,):
    username = callback.data.split('@')[1]
    await state.update_data(username=username)
    await callback.message.edit_text('Выберите количество звёзд',
                                     reply_markup=await star_kb.buy_options_kb())
    # amount_money = callback.data.split('@')[2]
    # await callback.message.edit_text(f'Выберите способ оплаты для {amount_money} рублей? (для @{username})',
    #                                      reply_markup=await star_kb.buy_stars_select_method_kb())


@star.callback_query(F.data == 'send_stars_to_another_user')
async def send_stars_to_another_user(callback: CallbackQuery, state: FSMContext,):
    await callback.answer('')
    msg = await callback.message.edit_text('Отправьте имя пользователя (username) в чат',
                                     reply_markup=star_kb.back_to_buy_stars_select_user_kb)
    await state.set_state(stars_states.BuyStarSelectUserState.enter_username)
    await state.update_data(bot_msg_id=msg.message_id)


@star.message(stars_states.BuyStarSelectUserState.enter_username)
async def buy_stars_another_user_select_option(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.set_state(stars_states.BuyStarSelectUserState.smth)
    bot_msg_id = data.get("bot_msg_id")
    # amount_money = data.get("amount_money")
    # number_of_stars = data.get("buy_amount_stars")
    if bot_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_msg_id)
        except:
            pass
    username = message.text
    if username.startswith('@'):
        username = username[1:]
    await state.update_data(username=username)
    await message.answer('Выберите количество звёзд',
                                     reply_markup=await star_kb.buy_options_kb())

    # await message.answer(f'Вы собираетесь купить {number_of_stars} Telegram Stars 🌟 на аккаунт '
    #                      f'@{username} за {amount_money}₽.',
    #                      reply_markup=await star_kb.buy_stars_select_user_kb(amount_money, username))


@star.callback_query(F.data.startswith('buy-option_'))
async def buy_stars_select_method(callback: CallbackQuery, state: FSMContext):
    number_of_stars = int(callback.data.split('_')[1])
    await state.update_data(buy_number_of_stars=number_of_stars)
    star_cost = await star_db.get_star_cost()
    amount = number_of_stars * star_cost.amount
    await state.update_data(amount_money=amount)
    data = await state.get_data()
    username = data.get("username")
    await callback.message.edit_text( f'Вы собираетесь купить {number_of_stars} Telegram Stars 🌟 на аккаунт '
                                     f'@{username} за {amount}₽.\n\n'
                                      f'Выберите способ оплаты',
                                         reply_markup=await star_kb.buy_stars_select_method_kb())
    # await callback.message.edit_text(f'Вы собираетесь купить {number_of_stars} Telegram Stars 🌟 на аккаунт '
    #                                  f'@{callback.from_user.username} за {amount}₽.',
    #                                  reply_markup=await star_kb.buy_stars_select_user_kb(amount, callback.from_user.username))


@star.callback_query(F.data == 'enter_buy_option')
async def enter_buy_option(callback: CallbackQuery, state: FSMContext,):
    await callback.answer('')
    msg = await callback.message.edit_text('Отправьте в чат требуемое количество Звёзд 🌟',
                                     reply_markup=star_kb.buy_stars_cancel_kb)
    await state.set_state(stars_states.BuyStarState.enter_amount)
    await state.update_data(bot_msg_id=msg.message_id)


@star.message(stars_states.BuyStarState.enter_amount)
async def enter_buy_option_select_method(message: Message, user_info: UserORM, state: FSMContext):
    data = await state.get_data()
    bot_msg_id = data.get("bot_msg_id")
    if bot_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_msg_id)
        except:
            pass
    try:
        number_of_stars = int(message.text)
        if number_of_stars < 50 or number_of_stars > 50000:
            raise ValueError
    except ValueError:
        msg = await message.answer('К сожалению, мы не можем отправить такое количество звёзд. Попробуйте ввести ещё раз.',
                             reply_markup=star_kb.buy_stars_cancel_kb
                             )
        await state.update_data(bot_msg_id=msg.message_id)
        return
    await state.update_data(buy_number_of_stars=number_of_stars)
    star_cost = await star_db.get_star_cost()
    amount = number_of_stars * star_cost.amount
    await state.update_data(amount_money=amount)
    await state.set_state(stars_states.BuyStarState.smth)
    username = data.get("username")
    await message.answer(f'Вы собираетесь купить {number_of_stars} Telegram Stars 🌟 на аккаунт '
                                     f'@{username} за {amount}₽.\n\n'
                                     f'Выберите способ оплаты',
                                     reply_markup=await star_kb.buy_stars_select_method_kb())


@star.callback_query(F.data == 'how_it_works')
async def how_it_works(callback: CallbackQuery):
    await callback.answer('')
    text = await star_db.get_how_it_works_text()
    text = text.replace("\\n", "\n")
    await callback.message.edit_text(text,
                                     disable_web_page_preview=True,
                                     reply_markup=star_kb.back_to_buy_stars_kb)