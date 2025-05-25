from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import Numeric
from decimal import Decimal
import datetime
from typing import List



class StarCostORM(Base):
    __tablename__ = 'stars_cost'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(default=1)



class StarWithdrawalOption(Base):
    __tablename__ = 'stars_withdrawal_options'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]


class StarBuyOption(Base):
    __tablename__ = 'stars_buy_options'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]


class BuyStarMethodORM(Base):
    __tablename__ = 'buy_stars_methods'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    eng_name: Mapped[str] = mapped_column(String(64), nullable=True)

    buy_stars: Mapped[List["BuyStarsORM"]] = relationship(back_populates="method", cascade='all, delete')


class BuyStarsORM(Base):
    __tablename__ = 'buy_stars'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    order_id: Mapped[str] = mapped_column(String(50))
    method_id: Mapped[int] = mapped_column(ForeignKey('buy_stars_methods.id', ondelete='CASCADE'))
    amount: Mapped[int]
    status: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())

    user: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="buy_stars"
    )

    method: Mapped["BuyStarMethodORM"] = relationship(back_populates="buy_stars")



class WithdrawalORM(Base):
    __tablename__ = 'withdrawals'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    amount: Mapped[int]
    status: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())

    user: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="withdrawals"
    )