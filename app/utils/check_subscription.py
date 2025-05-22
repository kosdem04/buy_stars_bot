from config import CHANNEL_ID, TOKEN
from aiogram.types import ChatMember, ChatMemberLeft
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

bot = Bot(token=TOKEN)

async def is_user_in_channel(user_id) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Проверим, не покинул ли пользователь канал
        return not isinstance(member, ChatMemberLeft)
    except TelegramForbiddenError:
        # Бот не имеет доступа к каналу
        print("Нет доступа к каналу. Проверь, что бот админ.")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False