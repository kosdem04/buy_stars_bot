from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import app.requests.stars as star_db


back_to_buy_stars_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_buy_stars')]])


back_to_buy_stars_select_user_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_buy_stars_select_user')]])


withdrawal_stars_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_to_withdrawal_stars')]])

buy_stars_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_to_buy_stars')]])


sure_withdrawal_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌟 Да', callback_data='withdrawal_yes'),
     InlineKeyboardButton(text='❌ Отмена', callback_data='back_to_withdrawal_stars')]])

sure_buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌟 Да', callback_data='buy_yes'),
     InlineKeyboardButton(text='❌ Отмена', callback_data='back_to_buy_stars')]])


back_to_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в профиль', callback_data='back_to_profile')]])



async def buy_stars_select_user_kb(amount, username):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Отправить другому пользователю', callback_data='send_stars_to_another_user'))
    kb.add(InlineKeyboardButton(text=f'Оплатить {amount}₽', callback_data=f'send-stars-to-user@{username}@{amount}'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_buy_stars'))
    kb.adjust(1)
    return kb.as_markup()


async def buy_stars_select_method_kb():
    methods = await star_db.get_buy_stars_methods()
    kb = InlineKeyboardBuilder()
    for method in methods:
        kb.add(InlineKeyboardButton(text=f"{method.name}",
                                    callback_data=f"buy-stars-select-method_{method.id}"))
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='back_to_buy_stars'))
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
    kb.row(
        InlineKeyboardButton(text='Отзывы', url='https://t.me/stardark666'),
        InlineKeyboardButton(text='Помощь', url='https://t.me/akmglqq'),
        InlineKeyboardButton(text='TG Канал', url='https://t.me/stardark666')
    )
    kb.add(InlineKeyboardButton(text='Как это работает?', callback_data='how_it_works'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_main'))
    kb.adjust(2)
    return kb.as_markup()