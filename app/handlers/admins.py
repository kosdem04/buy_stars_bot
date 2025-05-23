from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, CommandStart, Command
from config import ADMINS, CHAT_FOR_WITHDRAWAL_ID
import app.keyboards.admins as admin_kb
import app.requests.admins as admin_db
import app.states.admin as admin_states
import asyncio
import app.requests.stars as star_db
import html

admin = Router()


class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


@admin.channel_post(F.text == "Как дела")
async def handle_channel_post(message: Message):
    print("Канал:", message.chat.id)
    await message.answer(f"Всё отлично!, {message.chat.id}")


@admin.message(Command("get_chat_id"))
async def get_chat_id(message: Message):
    await message.answer(f"Chat ID: {message.chat.id}")


@admin.callback_query(AdminProtect(), F.data == 'back_to_admin_panel')
@admin.message(AdminProtect(), Command("admin_panel"))
async def admin_panel(event: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if isinstance(event, Message):
        await event.answer('Добро пожаловать в Админ-панель?',
                             reply_markup=admin_kb.admin_panel_kb)
    elif isinstance(event, CallbackQuery):
        await event.answer('')
        await event.message.edit_text('Добро пожаловать в Админ-панель?',
                           reply_markup=admin_kb.admin_panel_kb)


"""
КУРС СТОИМОСТИ ЗВЁЗД
"""
@admin.callback_query(AdminProtect(), F.data == 'stars_cost')
async def stars_cost(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    star_cost = await star_db.get_star_cost()
    if star_cost:
        await callback.message.edit_text(f'1 Telegram Star 🌟 = {star_cost.amount}₽',
                                         reply_markup=admin_kb.edit_star_cost_kb)
    else:
        await callback.message.edit_text(f'Добавьте курс стоимости 1 Telegram Star 🌟',
                                         reply_markup=admin_kb.add_star_cost_kb)


@admin.callback_query(AdminProtect(), F.data == 'add_stars_cost')
async def add_stars_cost(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    msg = await callback.message.edit_text(f'Введите, сколько будет стоить 1 Telegram Star 🌟',
                                     reply_markup=admin_kb.admin_cancel_kb)
    await state.set_state(admin_states.AddStarCostState.amount)
    await state.update_data(bot_msg_id=msg.message_id)


@admin.message(AdminProtect(), admin_states.AddStarCostState.amount)
async def add_stars_cost_ok(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_msg_id = data.get("bot_msg_id")
    if bot_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_msg_id)
        except:
            pass
    try:
        amount = int(message.text)
        if amount < 1:
            raise ValueError
    except ValueError:
        msg = await message.answer('Введённое Вами значение некорректно. Попробуйте ввести ещё раз.',
                             reply_markup=admin_kb.admin_cancel_kb
                             )
        await state.update_data(bot_msg_id=msg.message_id)
        return
    await admin_db.add_star_cost(amount)
    await state.clear()
    star_cost = await star_db.get_star_cost()
    await message.answer(f'1 Telegram Star 🌟 = {star_cost.amount}₽',
                                     reply_markup=admin_kb.edit_star_cost_kb)


@admin.callback_query(AdminProtect(), F.data == 'edit_stars_cost')
async def edit_stars_cost(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    msg = await callback.message.edit_text(f'Введите, сколько будет стоить 1 Telegram Star 🌟',
                                     reply_markup=admin_kb.admin_cancel_kb)
    await state.set_state(admin_states.EditStarCostState.amount)
    await state.update_data(bot_msg_id=msg.message_id)


@admin.message(AdminProtect(), admin_states.EditStarCostState.amount)
async def edit_stars_cost_ok(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_msg_id = data.get("bot_msg_id")
    if bot_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_msg_id)
        except:
            pass
    try:
        amount = int(message.text)
        if amount < 1:
            raise ValueError
    except ValueError:
        msg = await message.answer('Введённое Вами значение некорректно. Попробуйте ввести ещё раз.',
                             reply_markup=admin_kb.admin_cancel_kb
                             )
        await state.update_data(bot_msg_id=msg.message_id)
        return
    await admin_db.edit_star_cost(amount)
    await state.clear()
    star_cost = await star_db.get_star_cost()
    await message.answer(f'1 Telegram Star 🌟 = {star_cost.amount}₽',
                                     reply_markup=admin_kb.edit_star_cost_kb)


"""
РАССЫЛКА
"""
@admin.callback_query(AdminProtect(), F.data == 'send_message_everyone')
async def send_message_everyone(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    msg = await callback.message.answer('Введите сообщение для рассылки',
                                        reply_markup=admin_kb.admin_cancel_kb)
    await state.set_state(admin_states.SendAllState.text)
    await state.update_data(bot_msg_id=msg.message_id)


@admin.message(AdminProtect(), admin_states.SendAllState.text)
async def send_message_everyone_ok(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_msg_id = data.get("bot_msg_id")
    if bot_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_msg_id)
        except:
            pass
    users = await admin_db.get_all_users()
    for user in users:
        await asyncio.sleep(1)
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            continue
    await state.clear()
    await message.answer('Сообщение отправлено всем пользователям')



"""
ТЕКСТ В БОТЕ
"""
@admin.callback_query(AdminProtect(), F.data == 'back_to_types_text')
@admin.callback_query(AdminProtect(), F.data == 'edit_text_in_bot')
async def edit_text_in_bot(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.edit_text('Выберите, какой текст хотите изменить',
                                  reply_markup=await admin_kb.types_text_in_bot_kb())



@admin.callback_query(AdminProtect(), F.data.startswith('edit-text_'))
async def edit_text_show(callback: CallbackQuery, state: FSMContext):
    text_id = callback.data.split('_')[1]
    text = await admin_db.get_text_by_id(text_id)
    text_in_bot = text.replace("\\n", "\n")
    await state.update_data(text_id=text_id)
    await callback.message.edit_text(f'<b>ТАК ТЕКСТ ВЫГЛЯДИТ В БД</b>\n\n'
                                     f'{html.escape(text)}'
                                     f'\n\n<b>ТАК ТЕКСТ ВЫГЛЯДИТ В БОТЕ</b>\n\n'
                                     f'{text_in_bot}',
                                     disable_web_page_preview=True,
                                     reply_markup=admin_kb.edit_text_kb)


@admin.callback_query(AdminProtect(), F.data == 'edit_text')
async def edit_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    msg = await callback.message.edit_text('Напишите новый текст',
                                  reply_markup=admin_kb.cancel_edit_text_kb)
    await state.set_state(admin_states.EditTextState.text)
    await state.update_data(bot_msg_id=msg.message_id)



@admin.message(AdminProtect(), admin_states.EditTextState.text)
async def enter_withdrawal_option_sure(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_msg_id = data.get("bot_msg_id")
    if bot_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_msg_id)
        except:
            pass
    text = message.text
    await state.update_data(text=text)
    text_in_bot = text.replace("\\n", "\n")
    await message.answer(f'Вы уверены, что хотите изменить текст?\n\n'
                         f'<b>ТАК ТЕКСТ БУДЕТ ВЫГЛЯДЕТЬ В БД</b>\n\n'
                         f'{html.escape(text)}'
                         f'\n\n<b>ТАК ТЕКСТ БУДЕТ ВЫГЛЯДЕТЬ В БОТЕ</b>\n\n'
                         f'{text_in_bot}',
                         disable_web_page_preview=True,
                         reply_markup=admin_kb.sure_edit_text_kb)


@admin.callback_query(AdminProtect(), F.data == 'edit_text_yes')
async def edit_text_yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    data = await state.get_data()
    text_id = data.get("text_id")
    text = data.get("text")
    print('!!! ', text_id, text)
    await admin_db.edit_text(text_id, text)
    await state.clear()
    await callback.message.edit_text('Текст изменён',
                                  reply_markup=await admin_kb.types_text_in_bot_kb())



"""

Чтение сообщений из закрытого чата (модерация)
----------------------------------------------------------------------------------------------

"""


@admin.callback_query(lambda callback: callback.message.chat.id == CHAT_FOR_WITHDRAWAL_ID,
                      F.data.startswith('withdrawal-done_'))
async def withdrawal_done(callback: CallbackQuery, bot: Bot):
    await callback.answer('Спасибо за работу')
    withdrawal_id = callback.data.split('_')[1]
    await callback.message.delete()
    await admin_db.withdrawal_done(withdrawal_id)
    withdrawal = await admin_db.get_withdrawal(withdrawal_id)
    await bot.send_message(chat_id=withdrawal.user.tg_id, text=f'<b>‼️ Одобрен запрос на вывод '
                                                               f'{withdrawal.amount} звёзд</b>')


@admin.callback_query(lambda callback: callback.message.chat.id == CHAT_FOR_WITHDRAWAL_ID,
                       F.data.startswith('withdrawal-failed_'))
async def withdrawal_failed(callback: CallbackQuery, bot: Bot):
    await callback.answer('Спасибо за работу')
    withdrawal_id = callback.data.split('_')[1]
    await callback.message.delete()
    await admin_db.withdrawal_failed(withdrawal_id)
    withdrawal = await admin_db.get_withdrawal(withdrawal_id)
    await bot.send_message(chat_id=withdrawal.user.tg_id, text=f'<b>‼️ Не одобрен запрос на вывод '
                                                               f'{withdrawal.amount} звёзд</b>')

