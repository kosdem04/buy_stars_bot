from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import CHANNEL_URL


main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить звёзды ⭐️', callback_data='buy_stars'),
     InlineKeyboardButton(text='Профиль 👤', callback_data='profile')],
    [InlineKeyboardButton(text='Отзывы', url='https://t.me/whitestarchat77'),
     InlineKeyboardButton(text='Поддержка', url='https://t.me/akmglqq')],
    [InlineKeyboardButton(text='TG Канал', url='https://t.me/stardark666'),
     InlineKeyboardButton(text='Как это работает?', callback_data='how_it_works')]])


profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вывод 💫', callback_data='withdrawal_stars')],
    [InlineKeyboardButton(text='Реферальная система', callback_data='referral_system')],
    [InlineKeyboardButton(text='Назад ⏪', callback_data='back_to_main')]])


back_to_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_profile')]])



subscribe_to_channel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться', url=CHANNEL_URL)],
    [InlineKeyboardButton(text='Проверить', callback_data='check_subscribe')]])


