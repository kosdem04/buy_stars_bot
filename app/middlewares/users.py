from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message, CallbackQuery
from app.requests.users import set_user
from app.utils.check_subscription import is_user_in_channel
from app.keyboards.users import subscribe_to_channel_kb



class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user_in_channel = await is_user_in_channel(event.from_user.id)
        if user_in_channel:
            user = await set_user(event.from_user.id, event.from_user.username)
            data['user_info'] = user
            return await handler(event, data)

        warning_text = "Пожалуйста, подпишитесь на канал, чтобы продолжить."
        if isinstance(event, Message):
            await event.answer(warning_text, reply_markup=subscribe_to_channel_kb)
        elif isinstance(event, CallbackQuery):
            await event.answer('')
            if (event.message.text != warning_text and event.message.reply_markup != subscribe_to_channel_kb):
                await event.message.edit_text(warning_text, reply_markup=subscribe_to_channel_kb)
        return

