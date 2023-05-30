"""
    API Documentation
    https://bybit-exchange.github.io/docs/v5/intro
"""

#API Imports
from pybit import HTTP
from pybit import WebSocket

# CONFIG

mode = "test"
timeframe = 60
kline_limit = 200
z_score_window = 21

#LIVE API
api_key_mainnet = ""
api_secret_mainnet = ""

#TEST API
api_key_testnet = ""
api_secret_testnet = ""

#SELECTED API

api_key = api_key_testnet if mode ==  "test" else api_key_mainnet
api_secret = api_secret_testnet if mode ==  "test" else api_secret_mainnet


api_url = "https://api-testnet.bybit.com" if mode == "test" else "hettps://api.bybit.com"

#SESSION Activation

session = HTTP(api_url)


# Wb Socket Connection

# ws = WebSocket(

# )





