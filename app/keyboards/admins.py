from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import app.requests.admins as admin_db


admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Курс стоимости звёзд', callback_data='stars_cost')],
    [InlineKeyboardButton(text='Изменить тексты', callback_data='edit_text_in_bot')],
    [InlineKeyboardButton(text='Сделать рассылку', callback_data='send_message_everyone')],
    [InlineKeyboardButton(text='Выйти', callback_data='back_to_main')]])


edit_star_cost_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_stars_cost')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_admin_panel')]])


add_star_cost_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_stars_cost')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_admin_panel')]])


back_to_admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_admin_panel')]])


edit_text_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_text')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_types_text')]])


cancel_edit_text_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_to_types_text')]])


admin_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_to_admin_panel')]])


sure_edit_text_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌟 Да', callback_data='edit_text_yes'),
     InlineKeyboardButton(text='❌ Отмена', callback_data='back_to_types_text')]])


async def types_text_in_bot_kb():
    texts = await admin_db.get_texts_in_bot()
    kb = InlineKeyboardBuilder()
    for text in texts:
        kb.add(InlineKeyboardButton(text=f"{text.type}",
                                    callback_data=f"edit-text_{text.id}"))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_admin_panel'))
    kb.adjust(1)
    return kb.as_markup()


async def withdrawal_moderation(withdrawal_id):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Выполнено",
                                callback_data=f"withdrawal-done_{withdrawal_id}"))
    kb.add(InlineKeyboardButton(text="Отказано",
                                callback_data=f"withdrawal-failed_{withdrawal_id}"))
    kb.adjust(1)
    return kb.as_markup()


