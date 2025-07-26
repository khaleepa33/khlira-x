import MetaTrader5 as mt5
import json
import time

# Load config
with open("khlira_config.json") as f:
    config = json.load(f)

# MT5 connection
def connect():
    if not mt5.initialize():
        raise Exception("MT5 init failed")
    account = mt5.login(12345678, password="yourpassword", server="YourBroker-Server")
    if not account:
        raise Exception("Login failed")

# Buy Order
def place_buy():
    symbol = config["symbol"]
    lot = config["lot_size"]
    price = mt5.symbol_info_tick(symbol).ask
    tp = price + config["take_profit"] * 0.01
    sl = price - config["stop_loss"] * 0.01

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "magic": config["magic_number"],
        "deviation": 20,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    return mt5.order_send(request)

# Sell Order
def place_sell():
    symbol = config["symbol"]
    lot = config["lot_size"]
    price = mt5.symbol_info_tick(symbol).bid
    tp = price - config["take_profit"] * 0.01
    sl = price + config["stop_loss"] * 0.01

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "magic": config["magic_number"],
        "deviation": 20,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    return mt5.order_send(request)
