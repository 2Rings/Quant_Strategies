from config_execution_api import session_private

# Check for open positions
def open_position_confirmation(ticker):
    try:
        position = session_private.my_position(
            symbol=ticker
        )
        if position["ret_msg"] == "OK":
            for item in position["result"]:
                if item["size"] > 0:
                    return True
    except:
        return True     
    return False       


def active_position_confirmation(ticker):
    try:
        active_order = session_private.get_active_order(
            symbol=ticker,
            order_status="Created", #New, PartiallyFilled, Active
        )
        if active_order["ret_msg"] == "OK":
            if active_order["result"]["data"] != None:
                return True
    except:
        return True     
    return False   

def get_open_positions(ticker, direction="Long"):
    # Get position
    position = session_private.my_position(symbol=ticker)

    # Select index to avoid looping through response
    index = 0 if direction == "Long" else 1

    # Construct a response
    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if "symbol" in position["result"][index].keys():
                order_price = position["result"][index]["entry_price"]
                order_quantity = position["result"][index]["size"]
                return order_price, order_quantity
            
    return (0, 0)

def get_active_order(ticker):
    # Get position
    active_order = session_private.get_active_order(
            symbol=ticker,
            order_status="Created,New,PartiallyFilled,Active"
        )

    # Select index to avoid looping through response
    index = 0 if direction == "Long" else 1

    # Construct a response
    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if active_order["result"]["data"] != None:
                order_price = active_order["result"]["data"][0]["price"]
                order_quantity = active_order["result"]["data"][0]["quantity"]
                return order_price, order_quantity
            
    return (0, 0)


