from config_execution_api import ws_public_url, ticker_1, ticker_2

from pybit import WebSocket

# Public ws socket

subs_public = [
    f"orderBookL2_25.{ticker_1}",
    f"orderBookL2_25.{ticker_2}"
]

ws_public = WebSocket(ws_public_url,
               subscriptions= subs_public
               )

# while True:
#     data = ws_public.fetch(subs_public[0])
#     if data:
#         print(data)