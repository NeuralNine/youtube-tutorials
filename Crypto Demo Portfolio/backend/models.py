from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    portfolio = relationship('Portfolio', back_populates='user', uselist=False)


class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_added_money = Column(Float, default=0)
    available_money = Column(Float, default=0)

    user = relationship('User', back_populates='portfolio')
    assets = relationship('Asset', back_populates='portfolio')
    transactions = relationship('Transaction', back_populates='portfolio')


class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    symbol = Column(String)
    quantity = Column(Float)
    
    portfolio = relationship('Portfolio', back_populates='assets')


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    symbol = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    timestamp = Column(DateTime)

    portfolio = relationship('Portfolio', back_populates='transactions')

