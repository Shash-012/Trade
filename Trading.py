import alpaca_trade_api as tradeapi
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas

# Authentication of API using API key and secret
API_KEY = 'Enter your key'
API_SECRET = 'Enter your secret'
BASE_URL = 'https://paper-api.alpaca.markets'

#initialize the api
api=tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Check account info
account = api.get_account()

def check_balance():
    print("Account balance = ",account.cash)

# Place a paper trade order/Buy (1 share of nvidia)
def Buy_Nvidia_shares():
    global order
    order = api.submit_order(
        symbol="NVDA", # The symbol assigned to nvidia
        qty=1, # Buying 2 shares of apple
        side='buy', # Buy Action
        type='market', # Market Order (Executed immediately)
        time_in_force='gtc'
    )
    print("Buy order submitted for NVDA")

#Check Open Orders
def check_open_orders():
    open_orders=api.list_orders(status='open')
    if open_orders:
        print("Open Orders:")
        for order in open_orders:
            print(f"Order ID: {order.id} - {order.side} {order.qty} of {order.symbol} at {order.created_at}")
    else:
        print("No Open Orders")

# Check Current Holdings or Positions
def check_current_positions():
    positions=api.list_positions()
    if positions:
        print("Current Positions:")
        for position in positions:
            print(f"Symbol: {position.symbol} | Quantity: {position.qty} shares")

#Sell a share
def Sell_share():
    import time
    while True:
        status = api.get_order(order.id).status
        if status == "filled":
            print("Order Filled")
            break
        time.sleep(1)

    api.submit_order(
        symbol="NVDA",
        qty=1,
        side='sell',
        type='market',
        time_in_force='day'
    )
    print("Sell order submitted for NVDA")

def close_all_positions():
    positions = api.list_positions()
    for position in positions:
        side = 'sell' if float(position.qty) > 0 else 'buy'
        api.submit_order(
            symbol=position.symbol,
            qty=abs(int(float(position.qty))),
            side=side,
            type='market',
            time_in_force='day'
        )

def check_status():
    status = api.get_order(order.id).status
    print(status)

def get_btc_history():
    client=CryptoHistoricalDataClient()
    request_params=CryptoBarsRequest(
        symbol_or_symbols='BTC/USD',
        timeframe=TimeFrame.Day,
        start='2025-01-01'
    )
    bars=client.get_crypto_bars(request_params)
    
    # Converts the data into a pandas dataframe
    df=bars.df
    print(df)

def get_NVDA_history():
    client = StockHistoricalDataClient(api_key=API_KEY,secret_key=API_SECRET)
    req_params = StockBarsRequest(
        symbol_or_symbols=['NVDA'],
        timeframe=TimeFrame.Day,
        start='2025-06-12'
    )
    bars=client.get_stock_bars(req_params)

    df=bars.df
    with pandas.option_context('display.max_rows',None,'display.max_columns',None):
        print(df)
    #df.to_csv('NVDA_stocks_12to18June2025.csv')

get_NVDA_history()

