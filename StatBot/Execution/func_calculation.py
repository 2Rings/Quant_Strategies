from config_execution_api import stop_loss_fail_safe, ticker_1, rounding_ticker_1
from config_execution_api import rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2
import math



# PUts all close prices in a list
def extract_close_prices(prices):
    close_prices = []

    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        
        close_prices.append(price_values["close"])
    return close_prices

# Get trade details and latest prices

def get_trade_details(orderbook, direction="Long", capital=0):
    # Set calculation and output variables
    price_rounding = 20
    quantity_rounding = 20
    order_price = 0
    quantity  = 0
    stop_loss = 0
    bid_items_list = []
    ask_items_list = []

    # Get prices, stop loss and quantity

    if orderbook:
        #Set price rounding

        price_rounding = rounding_ticker_1 if orderbook[0]["symbol"] == ticker_1 else rounding_ticker_2
        quantity_rounding = quantity_rounding_ticker_1 if orderbook[0]["symbol"] == ticker_1 else quantity_rounding_ticker_2

        # Organize prices 

        for level in orderbook:
            if level["side"] == 'Buy':
                bid_items_list.append(float(level["price"]))
            else:
                ask_items_list.append(float(level["price"]))


        # Calculate price, size, stop loss and average liquidity

        if len(ask_items_list) > 0 and len(bid_items_list) > 0:
            # Sort lists

            ask_items_list.sort()
            bid_items_list.sort()
            bid_items_list.reverse()


            # Get nearest ask, nearest bid and orderbook spread

            nearest_ask = ask_items_list[0]
            nearesr_bid = bid_items_list[0]

            # Calculate hard stop loss

            if direction == "Long":
                # Placing at bid has high probability of not being cancelled, but may not fill
                order_price = nearesr_bid
                stop_loss = round(order_price*(1-stop_loss_fail_safe), price_rounding)

            else:
                # Placing at ask has high probability of not being cancelled, but may not fill
                order_price = nearest_ask
                stop_loss = round(order_price*(1+stop_loss_fail_safe), price_rounding)


            # Caculate Quantity
            quantity = round(capital/order_price, quantity_rounding)

    # Output results
    return (order_price, stop_loss, quantity)

# from config_ws_connect import subs_public, ws_public
# while True:
#     orderbook = ws_public.fetch(subs_public[0])
#     if orderbook:
#         order_price, stop_loss, quantity = get_trade_details(orderbook, direction="Long", capital=1000)
#         print(order_price, stop_loss, quantity)




