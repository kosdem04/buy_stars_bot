from app.database import async_session
from app.models.stars import StarWithdrawalOption, StarBuyOption, StarCostORM, WithdrawalORM
from app.models.users import UserORM
from app.models.admin import TextInBotORM
from sqlalchemy import select, update, delete, desc
import datetime
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func



async def get_withdrawal_options():
    async with async_session() as session:
        query = (
            select(StarWithdrawalOption)
        )
        result_query = await session.execute(query)
        options = result_query.scalars().all()
        return options


async def edit_star_cost(amount: int):
    async with async_session() as session:
        result = await session.execute(select(StarCostORM))
        cost = result.scalars().first()
        query = (
            update(StarCostORM)
            .where(StarCostORM.id == cost.id)
            .values(amount=amount)
        )
        await session.execute(query)
        await session.commit()


async def add_star_cost(amount: int):
    async with async_session() as session:
        session.add(StarCostORM(amount=amount))
        await session.commit()


async def get_all_users():
    async with async_session() as session:
        query = (
            select(UserORM)
        )
        result_query = await session.execute(query)
        users = result_query.scalars().all()
        return users


async def get_texts_in_bot():
    async with async_session() as session:
        query = (
            select(TextInBotORM)
        )
        result_query = await session.execute(query)
        texts = result_query.scalars().all()
        return texts


async def get_text_by_id(text_id):
    async with async_session() as session:
        text = await session.scalar(select(TextInBotORM.text).where(TextInBotORM.id == text_id))
        return text



async def edit_text(text_id, text):
    async with async_session() as session:
        query = (
            update(TextInBotORM)
            .where(TextInBotORM.id == text_id)
            .values(text=text)
        )
        await session.execute(query)
        await session.commit()


async def withdrawal_done(withdrawal_id):
    async with async_session() as session:
        query = (
            select(WithdrawalORM)
            .options(selectinload(WithdrawalORM.user))
            .where(WithdrawalORM.id == withdrawal_id)
        )
        result = await session.execute(query)
        withdrawal = result.scalar()
        withdrawal.status = True
        await session.commit()


async def withdrawal_failed(withdrawal_id):
    async with async_session() as session:
        query = (
            select(WithdrawalORM)
            .options(selectinload(WithdrawalORM.user))
            .where(WithdrawalORM.id == withdrawal_id)
        )
        result = await session.execute(query)
        withdrawal = result.scalar()
        user = await session.scalar(
            select(UserORM).where(UserORM.id == withdrawal.user_id)
        )
        user.balance += withdrawal.amount
        await session.commit()



async def get_withdrawal(withdrawal_id):
    async with async_session() as session:
        query = (
            select(WithdrawalORM)
            .options(selectinload(WithdrawalORM.user))
            .where(WithdrawalORM.id == withdrawal_id)
        )
        result = await session.execute(query)
        withdrawal = result.scalar()
        return withdrawal