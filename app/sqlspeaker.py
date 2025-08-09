import os

from sqlalchemy import select, create_engine
from .db_orm import (Stock,
                        
                        QuarterlyBalanceSheet, QuarterlyIncomeStatement, QuarterlyCashFlow, StockView)

from datetime import date,timedelta

import pandas as pd

from sqlalchemy.orm import sessionmaker


from sqlalchemy.exc import DBAPIError



import logging
logging.getLogger('yfinance').setLevel(logging.CRITICAL)
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('../../output.log', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add the handler to your logger
logger.addHandler(file_handler)

# Example usage
logger.info("This log will appear in output.log")
logger.debug("Debugging information here.")
psql = os.getenv('PSQL')
engine_dest = create_engine(psql)
Session = sessionmaker(bind=engine_dest)

TABLE_MODLE_MAP = {
    "quarterly_balance_sheet": QuarterlyBalanceSheet,
    "quarterly_income_statement": QuarterlyIncomeStatement,
    "quarterly_cash_flow": QuarterlyCashFlow,
}

# connect to the database investments
with Session() as session:
    try:
        seven_days_ago = date.today() - timedelta(days=7)
        stock_list = session.query(StockView).filter(StockView.last_update >= seven_days_ago).all()


    except DBAPIError as e:
        print(f"Error: {e}")
    finally:
        session.close()






def financial_insert_function(df: pd.DataFrame, stock_id: int,table_name:str):
    with Session() as session:
        try:

            Model = TABLE_MODLE_MAP[table_name]
            # Ensure the DataFrame's index is named 'publish_date' and reset it to a column
            if df.index.name != 'publish_date':
                df = df.reset_index().rename(columns={'index': 'publish_date'})
            else:
                df = df.reset_index()

            # Convert 'publish_date' to datetime.date
            df['publish_date'] = pd.to_datetime(df['publish_date']).dt.date

            # Query existing records for the given stock_id
            existing_dates = session.scalars(
                select(Model.publish_date).
                where(Model.stock_id == stock_id)
            ).all()

            # Filter out rows that already exist in the database
            new_records = df[~df['publish_date'].isin(existing_dates)]

            # Iterate over the new records and add them to the session
            for _, row in new_records.iterrows():
                # Create the data dictionary encapsulated under the 'data' key
                data_dict = row.drop(['publish_date']).dropna().to_dict()
                record_data = {"data": data_dict}

                # Create an instance of the ORM model
                record = Model(
                    stock_id=stock_id,
                    publish_date=row['publish_date'],
                    data=data_dict
                )

                # Add the record to the session
                session.add(record)

            # Commit the session to insert all new records
            session.commit()


        except Exception as e:
            session.rollback()
            print(f"Error during insertion:{stock_id} {e}","\n")
        finally:
            session.close()
