from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import Numeric
from decimal import Decimal
import datetime
from typing import List


class UserORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(100))
    balance: Mapped[Decimal] = mapped_column(
        Numeric(7, 2), nullable=False, default=Decimal('0')
    )
    total_stars: Mapped[int] = mapped_column(default=0)

    referrals_referrer: Mapped[List["ReferralORM"]] = relationship(back_populates="referrer",
                                                               cascade='all, delete',
                                                               foreign_keys="[ReferralORM.referrer_id]")
    referral_referred: Mapped[List["ReferralORM"]] = relationship(back_populates="referred",
                                                                cascade='all, delete',
                                                                foreign_keys="[ReferralORM.referred_id]")
    buy_stars: Mapped[List["BuyStarsORM"]] = relationship(
        "BuyStarsORM",
        back_populates="user",
        cascade='all, delete'
    )

    withdrawals: Mapped[List["WithdrawalORM"]] = relationship(
        "WithdrawalORM",
        back_populates="user",
        cascade='all, delete'
    )



class ReferralORM(Base):
    __tablename__ = 'referrals'

    id: Mapped[int] = mapped_column(primary_key=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    referred_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())

    referrer: Mapped["UserORM"] = relationship(back_populates="referrals_referrer", foreign_keys=[referrer_id])
    referred: Mapped["UserORM"] = relationship(back_populates="referral_referred", foreign_keys=[referred_id])
