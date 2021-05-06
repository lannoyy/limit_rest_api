from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime, extract
)
from db import engine
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime


Session = sessionmaker(bind=engine)

Base = declarative_base()
CUR = ['RUB', 'USD', 'EUR']
CNT = ['RUS', 'ABH', 'AUS']


class Limit(Base):
    __tablename__ = 'limit'
    user_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        index=True
    )
    currency = Column(
        String,
        nullable=False
    )
    country = Column(
        String,
        nullable=False
    )
    amount = Column(
        Integer,
        nullable=False
    )
    user_transaction = relationship("Transaction", cascade="all")

    def __init__(self, user_id: int,
                 currency: str, country: str, amount: int):
        if country in CNT and currency in CUR and amount >= 0:
            self.user_id = user_id
            self.currency = currency
            self.country = country
            self.amount = amount
        else:
            raise AttributeError

    def update(self, currency: str,
               country: str, amount: int):
        if currency in CUR and country in CNT and amount >= 0:
            self.amount = amount
            self.currency = currency
            self.country = country
        else:
            raise AttributeError

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'country': self.country,
            'currency': self.currency,
            'amount': self.amount
        }

    def check_for_transactions(self, month: int, year: int):
        """
        Accept month and year, returns array limit's transactions, or
        if transactions non exist for this date, returns empty array
        """
        session = Session()
        transactions = session.query(Transaction).filter(
            Transaction.user_id == self.user_id,
            extract('month', Transaction.date) == month,
            extract('year', Transaction.date) == year,
        )
        output = []
        for item in transactions:
            output.append(item.serialize)
        return output

    def check_for_additional_transaction(self, month: int, year: int, amount: int):
        """
        Accept month, year and amount,
        and return bool value,
        true if we can add transaction with this amount,
        false if we can't
        """
        data = self.check_for_transactions(month, year)
        current_amount = 0
        for item in data:
            current_amount += item['amount']
        return self.amount - current_amount >= amount


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey('limit.user_id'),
        nullable=False
    )
    user_limit = relationship("Limit", cascade="all")
    date = Column(
        DateTime,
        nullable=False
    )
    currency = Column(
        String,
        nullable=False
    )
    country = Column(
        String,
        nullable=False
    )
    amount = Column(
        Integer,
        nullable=False
    )

    def __init__(
            self, user_id: int,
            currency: str, country: str,
            date: str, amount: int
    ):
        session = Session()
        limit = session.query(Limit).filter(
            Limit.user_id == user_id
        ).first()
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        if limit.check_for_additional_transaction(
            month=date.month, year=date.year, amount=amount
        ) and amount >= 0:
            if country == limit.country and currency == limit.currency:
                self.user_id = user_id
                self.date = date
                self.currency = currency
                self.country = country
                self.amount = amount
            else:
                raise AttributeError
        else:
            raise ValueError

    def update(
            self, user_id: int,
            currency: str, country: str,
            date: datetime, amount: int
    ):
        session = Session()
        limit = session.query(Limit).get({"user_id": user_id})
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        if limit.check_for_additional_transaction(
            month=date.month, year=date.year, amount=amount
        ) and amount >= 0:
            if country == limit.country and currency == limit.currency:
                self.user_id = user_id
                self.amount = amount
                self.date = date
                self.currency = currency
                self.country = country
            else:
                raise AttributeError
        else:
            raise ValueError

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'date': str(self.date),
            'country': self.country,
            'currency': self.currency,
            'amount': self.amount
        }