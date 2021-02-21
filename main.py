import requests
import alpaca_trade_api as tradeapi
import json
from flask import Flask, redirect, url_for, render_template, jsonify

APCA_API_KEY_ID="PKYSPGCUDJT8Q2VVPP1S"
APCA_API_SECRET_KEY="gLuoXc2u7smhdj2Iitaugansr6cJRH40sVxMFUm4"
APCA_API_BASE_URL="https://paper-api.alpaca.markets"

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<guest>')
def hello_world(guest):
    return 'Hello, %s!' % guest

@app.route('/admin')
def welcome_admin():
    return 'Welcome admin :)'

@app.route('/user/<name>')
def hello_name(name):
    if name == 'admin':
        return redirect(url_for('welcome_admin'))
    else:
        return redirect(url_for('hello_world', guest = name))

@app.route('/market/<symbol>/<qty>/<side>/<time_in_force>')
def place_market_order(symbol, qty, side, time_in_force):
    return vars(api.submit_order(symbol, qty, side, "market", time_in_force))

@app.route('/limit/<symbol>/<qty>/<side>/<time_in_force>/<limit_price>')
def place_limit_order(symbol, qty, side, time_in_force, limit_price):
    return vars(api.submit_order(symbol, qty, side, "limit", time_in_force, limit_price))
    
@app.route('/stop/<symbol>/<qty>/<side>/<time_in_force>/<stop_price>')
def place_stop_order(symbol, qty, side, time_in_force, stop_price):
    return vars(api.submit_order(symbol, qty, side, "stop", time_in_force, None, stop_price))

@app.route('/stop_limit/<symbol>/<qty>/<side>/<time_in_force>/<limit_price>/<stop_price>')
def place_stop_limit_order(symbol, qty, side, time_in_force, limit_price, stop_price):
    return vars(api.submit_order(symbol, qty, side, "stop_limit", time_in_force, limit_price, stop_price))

@app.route('/trailing_stop/<symbol>/<qty>/<side>/<time_in_force>/<trail_percent>')
def place_trailing_stop_order(symbol, qty, side, time_in_force, trail_percent):
    return vars(api.submit_order(symbol, qty, side, "trailing_stop", time_in_force, None, None, None, False, None, None, None, None, trail_percent))

@app.route('/equity')
def get_equity():
    account = api.get_account()
    return jsonify(account.equity)

@app.route('/buying_power')
def get_buying_power():
    account = api.get_account()
    return jsonify(account.buying_power)

@app.route('/orders')
def get_orders():
    orders_list = api.list_orders()
    orders_dict = {}
    for i in range(len(orders_list)):
        orders_dict[i] = vars(orders_list[i])
    return orders_dict

@app.route('/positions')
def get_positions():
    positions_list = api.list_positions()
    positions_dict = {}
    for i in range(len(positions_list)):
        positions_dict[i] = vars(positions_list[i])
    return positions_dict

if __name__=='__main__': 
   app.run(debug = True) 