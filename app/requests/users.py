from app.database import async_session
from app.models.users import UserORM, ReferralORM
from app.models.admin import TextInBotORM
from sqlalchemy import select, update, delete, desc
import datetime
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func


async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(UserORM).where(UserORM.tg_id == tg_id))
        if not user:
            user = UserORM(
                tg_id=tg_id,
                username=username
            )
            session.add(user)
            await session.commit()
        return user


async def get_user_info(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(UserORM).where(UserORM.tg_id == tg_id))
        return user


async def number_of_referrals(user_id):
    async with async_session() as session:
        query = (
            select(func.count())
            .select_from(ReferralORM)
            .where(ReferralORM.referrer_id == user_id)
        )

        result_query = await session.execute(query)
        count = result_query.scalar()
        return count


async def get_start_text():
    async with async_session() as session:
        text = await session.scalar(select(TextInBotORM.text).where(TextInBotORM.type == 'start_text'))
        return text


async def add_referral(referrer_id, referral_id):
    async with async_session() as session:
        if referrer_id == referral_id:
            return
        user = await session.scalar(select(UserORM).where(UserORM.tg_id == referral_id))
        referrer = await session.scalar(select(UserORM).where(UserORM.tg_id == referrer_id))
        referral_in_db = await session.scalar(select(ReferralORM).where(
            ReferralORM.referrer_id == referrer.id,
            ReferralORM.referred_id == user.id
        ))
        if referral_in_db:
            return
        else:
            session.add(ReferralORM(referrer_id=referrer.id, referred_id=user.id))
            await session.commit()