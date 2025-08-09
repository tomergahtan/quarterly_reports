
import pytz.exceptions
import requests.exceptions
from pandas import DataFrame

import curl_cffi
from .sqlspeaker import update_shares, update_country, update_sector, update_currency, insert_stockspots, \
    financial_insert_function, StockView, update_last_update, stock_list

import yfinance as yf
from yfinance.exceptions import YFRateLimitError
import time
from datetime import timedelta,date
from typing import Optional
import datetime

# get the quarterly balance_sheet of a stock
def get_quarterly_balancesheet(share: yf.ticker.Ticker) -> Optional[DataFrame]:
    try:
        b_s = share.quarterly_balancesheet.transpose()
        if b_s.empty:
            return None
        b_s.columns = [j.lower().replace(" ", "_") for j in b_s.columns]
        return b_s

    except requests.exceptions.HTTPError:

        return None


    except requests.exceptions.ConnectionError:

        return None


    except pytz.exceptions.UnknownTimeZoneError:

        return None


# get the quarterly cashflow of a stock
def get_quarterly_cashflow(share: yf.ticker.Ticker) -> Optional[DataFrame]:
    try:
        c_f = share.quarterly_cashflow.transpose()
        if c_f.empty:
            return None
        c_f.columns = [j.lower().replace(" ", "_") for j in c_f.columns]
        return c_f


    except requests.exceptions.HTTPError:

        return None



    except requests.exceptions.ConnectionError:

        return None



    except pytz.exceptions.UnknownTimeZoneError:

        return None


# get the quarterly income_statement of a stock
def get_quarterly_income_statement(share: yf.ticker.Ticker) -> Optional[DataFrame]:
    try:
        i_s = share.quarterly_incomestmt.transpose()
        if i_s.empty:
            return None
        i_s.columns = [j.lower().replace(" ", "_") for j in i_s.columns]
        return i_s

    except:

        return None






# the main sync function
def info_generate(symbol_list: list[StockView]):

    # that function gets a list of symbols and updates the market capacity
    # and updates the history of
    trial = 0
    index = 0

    while index< len(symbol_list):

        try:
            stock = symbol_list[index]
            stock_data = yf.Ticker(stock.symbol)

            # Quarterly Balancesheet
            quarter_bs = get_quarterly_balancesheet(share=stock_data)
            if isinstance(quarter_bs, DataFrame):
                financial_insert_function(df=quarter_bs, table_name="quarterly_balance_sheet",stock_id=stock.stock_id)
                # print(f"done with {stock.symbol} quarterly_balancesheet")
            else:
                # print(f"problem with {stock.symbol} at quarterly_balancesheet")
                pass

            # Quarterly Income Statement
            quarter_is = get_quarterly_income_statement(share=stock_data)

            if isinstance(quarter_is, DataFrame):
                financial_insert_function(df=quarter_is, table_name="quarterly_income_statement",stock_id=stock.stock_id)
                # print(f"done with {stock.symbol} quarterly_income_statement")
            else:
                # print(f"problem with {stock.symbol} at quarterly_income_statement")
                pass

           
            quarter_cf = get_quarterly_cashflow(share=stock_data)
            if isinstance(quarter_cf, DataFrame):
                financial_insert_function(df=quarter_cf, table_name="quarterly_cash_flow",stock_id=stock.stock_id)
                # print(f"done with {stock.symbol} quarterly_cashflow")
            else:
                # print(f"problem with {stock.symbol} at quarterly_cashflow")
                pass

            print(f'all done for ticker {stock.symbol}',flush=True)
            index += 1
            trial = 0


        except (YFRateLimitError, requests.exceptions.Timeout, curl_cffi.requests.exceptions.Timeout) as e:
            print(f"Rate limit error with ticker {stock.symbol}: {e}",flush=True)
            print("Pausing for 90 seconds before retrying...", flush=True)
            time.sleep(90)
            if trial < 3:
                trial += 1
            else:
                trial = 0
                index += 1


        # except Exception as e:
        #     print(f"Unhandled error for {stock.symbol}: {e}")
        #     index += 1
        #     trial = 0


