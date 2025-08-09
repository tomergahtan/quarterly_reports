from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String,  ForeignKey, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from datetime import date
class Base(DeclarativeBase):
    pass


# Stocks table
class Stock(Base):
    __tablename__ = 'stocks'

    stock_id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Stock(stock_id={self.stock_id}, symbol='{self.symbol}')>"

class QuarterlyBalanceSheet(Base):
    __tablename__ = 'quarterly_balance_sheet'

    stock_id: Mapped[int] = mapped_column(ForeignKey('stocks.stock_id', ondelete='CASCADE'), primary_key=True)
    publish_date: Mapped[date] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONB), nullable=False)

    

    def __repr__(self):
        return f"<QuarterlyBalanceSheet(stock_id={self.stock_id}, publish_date={self.publish_date})>"

class QuarterlyIncomeStatement(Base):
    __tablename__ = 'quarterly_income_statement'

    stock_id: Mapped[int] = mapped_column(ForeignKey('stocks.stock_id', ondelete='CASCADE'), primary_key=True)
    publish_date: Mapped[date] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONB), nullable=False)

    

    def __repr__(self):
        return f"<QuarterlyIncomeStatement(stock_id={self.stock_id}, publish_date={self.publish_date})>"

class QuarterlyCashFlow(Base):
    __tablename__ = 'quarterly_cash_flow'

    stock_id: Mapped[int] = mapped_column(ForeignKey('stocks.stock_id', ondelete='CASCADE'), primary_key=True)
    publish_date: Mapped[date] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONB), nullable=False)



    def __repr__(self):
        return f"<QuarterlyCashFlow(stock_id={self.stock_id}, publish_date={self.publish_date})>"

class StockView(Base):
    __tablename__ = 'stockview'

    stock_id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String)
    last_update: Mapped[Date] = mapped_column(Date)
   

    def __repr__(self):
        return f"<StockView(stock_id={self.stock_id}, symbol='{self.symbol}')>"

class LastSpot(Base):
    __tablename__ = 'last_spot'

    stock_id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String)
    last_spot_date: Mapped[date] = mapped_column(Date)

    def __repr__(self):
        return f"<LastSpot(stock_id={self.stock_id}, symbol='{self.symbol}')>"


