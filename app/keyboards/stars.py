from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import app.requests.stars as star_db


back_to_buy_stars_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]])


back_to_buy_stars_select_user_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_select_user_stars')]])


withdrawal_stars_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_to_withdrawal_stars')]])

buy_stars_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_to_select_user_stars')]])


sure_withdrawal_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌟 Да', callback_data='withdrawal_yes'),
     InlineKeyboardButton(text='❌ Отмена', callback_data='back_to_withdrawal_stars')]])

sure_buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌟 Да', callback_data='buy_yes'),
     InlineKeyboardButton(text='❌ Отмена', callback_data='back_to_buy_stars')]])


back_to_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в профиль', callback_data='back_to_profile')]])



async def buy_stars_select_user_kb(username):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=f'Отправить себе', callback_data=f'send-stars-to-user@{username}'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_main'))
    kb.adjust(1)
    return kb.as_markup()


async def buy_stars_select_method_kb():
    methods = await star_db.get_buy_stars_methods()
    kb = InlineKeyboardBuilder()
    for method in methods:
        kb.add(InlineKeyboardButton(text=f"{method.name}",
                                    callback_data=f"buy_stars_select_method_{method.eng_name}"))
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='back_to_select_user_stars'))
    kb.adjust(1)
    return kb.as_markup()


async def withdrawal_options_kb():
    options = await star_db.get_withdrawal_options()
    kb = InlineKeyboardBuilder()
    for option in options:
        kb.add(InlineKeyboardButton(text=f"🌟 {option.amount} Звёзд",
                                    callback_data=f"withdrawal-option_{option.amount}"))
    kb.add(InlineKeyboardButton(text='🌟 Ввести свой вариант', callback_data='enter_withdrawal_option'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_profile'))
    kb.adjust(1)
    return kb.as_markup()


async def buy_options_kb():
    options = await star_db.get_buy_options()
    star_cost = await star_db.get_star_cost()
    kb = InlineKeyboardBuilder()
    for option in options:
        kb.add(InlineKeyboardButton(text=f"🌟 {option.amount} Звёзд - {option.amount * star_cost.amount}₽",
                                    callback_data=f"buy-option_{option.amount}"))
    kb.add(InlineKeyboardButton(text='🌟 Ввести свой вариант', callback_data='enter_buy_option'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_select_user_stars'))
    kb.adjust(2)
    return kb.as_markup()



async def buy_stars_crypto_bot_kb(pay_url, order_id):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Оплатить",
                                    url=pay_url))
    kb.add(InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_buy_stars_crypto_bot#{order_id}'))
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='back_to_select_user_stars'))
    kb.adjust(1)
    return kb.as_markup()