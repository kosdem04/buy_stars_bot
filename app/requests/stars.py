from app.database import async_session
from app.models.users import UserORM
from app.models.stars import StarWithdrawalOption, StarBuyOption, StarCostORM, BuyStarMethodORM, WithdrawalORM
from app.models.admin import TextInBotORM
from sqlalchemy import select, update, delete, desc
import datetime
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func



async def get_buy_stars_methods():
    async with async_session() as session:
        query = (
            select(BuyStarMethodORM)
        )
        result_query = await session.execute(query)
        methods = result_query.scalars().all()
        return methods



async def get_withdrawal_options():
    async with async_session() as session:
        query = (
            select(StarWithdrawalOption)
        )
        result_query = await session.execute(query)
        options = result_query.scalars().all()
        return options


async def get_buy_options():
    async with async_session() as session:
        query = (
            select(StarBuyOption)
        )
        result_query = await session.execute(query)
        options = result_query.scalars().all()
        return options


async def get_star_cost():
    async with async_session() as session:
        result = await session.execute(select(StarCostORM))
        cost = result.scalars().first()
        return cost


async def get_buy_star_text():
    async with async_session() as session:
        text = await session.scalar(select(TextInBotORM.text).where(TextInBotORM.type == 'buy_star_text'))
        return text


async def get_how_it_works_text():
    async with async_session() as session:
        text = await session.scalar(select(TextInBotORM.text).where(TextInBotORM.type == 'how_it_works_text'))
        return text


async def withdrawal_stars(user_id, new_balance, amount):
    async with async_session() as session:
        query = (
            update(UserORM)
            .where(UserORM.id == user_id)
            .values(balance=new_balance)
        )
        await session.execute(query)

        withdrawal = WithdrawalORM(user_id=user_id, amount=amount)
        session.add(withdrawal)
        await session.flush()
        withdrawal_id = withdrawal.id
        await session.commit()
        return withdrawal_id