import sqlite3
import hashlib
import hmac
import json
import math
import time
import requests,datetime,random
import sys
from pyxt.spot import Spot

try:
    # creating file path
    dbfile = '/home/ahmad/Documents/mmbot2/apps/db.sqlite3'
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(dbfile)

    # creating cursor
    cur = con.cursor()

    # reading all table names
    api = cur.execute('''SELECT * FROM binance;''')
    # here is you table list
    api=(api.fetchall())
    apikey=str(api[0][2])
    api_key=apikey
    secret=str(api[0][3])
    secret_key=secret

    set = cur.execute('''SELECT * FROM set2;''')
    # here is you table list
    set=(set.fetchall())
    delay=int(set[0][2])
    qty=float(set[0][3])
    symbol=str(set[0][4])
    # Be sure to close the connection
    con.close()
except:
    time.sleep(60)
    sys.exit("Database Error")
xt=Spot(host="https://sapi.xt.com", access_key=api_key, secret_key=secret_key)


tt=xt.get_depth(symbol,2)
p_pre=(xt.get_symbol_config(symbol=symbol)[0]['pricePrecision'])
q_pre=(xt.get_symbol_config(symbol=symbol)[0]['quantityPrecision'])
high=float(tt['asks'][0][0])
low=float(tt['bids'][0][0])
pp=((high+low)/2)
pp=round(pp,p_pre)
if pp==high:
    time.sleep(delay)
    sys.exit("price Error")
if pp==low:
    time.sleep(delay)
    sys.exit("price Error")
print(xt.balance("usdt"))
try:
    sell = xt.order(symbol='ramsena_usdt', price=pp, quantity=qty, side='SELL', type='LIMIT')
    print(sell)
except:
    # dtm=str(datetime.datetime.utcnow())
    # urlll = 'http://159.65.12.9:80/trades'
    # myobj = {"trade_id":'Buy_failed',"price":0,"status":"Buy_failed","coins":00,"time":dtm,"volume":00}

    # x = requests.post(urlll, json = myobj)
    sys.exit("Error ")
try:
    buy = xt.order(symbol='ramsena_usdt', price=pp, quantity=qty, side='BUY', type='LIMIT')
    print(buy)
except:
    # dtm=str(datetime.datetime.utcnow())
    # urlll = 'http://159.65.12.9:80/trades'
    # myobj = {"trade_id":'Buy_failed',"price":0,"status":"Buy_failed","coins":00,"time":dtm,"volume":00}

    # x = requests.post(urlll, json = myobj)
    sys.exit("Error ")

time.sleep(delay)
print(xt.balance("usdt"))
try:
    res = xt.cancel_order(order_id=buy['orderId'])
    res = xt.cancel_order(order_id=sell['orderId'])
except:pass

# aci=account_info(api_key,secret_key)
# for i in aci['data']:
#     if (i['type'])==1:
#         if (i['currency'])=='USDT':
#             usdti=float(i['balance'])
# for i in aci['data']:
#     if (i['type'])==1:
#         if (i['currency'])==(symbol.replace('USDT','')):
#             basei=float(i['balance'])
# pp=price_pick(symbol,qty)
# if (random.randint(0,14)) == 5:
#     price=pp[1]
# else:
#     price=pp[0]
# qtyo=pp[2]
# if (bool(random.getrandbits(1))):
#     try:
#         buy_order=buy(api_key,secret_key,price,qtyo,symbol)
#         print(buy_order)
#         buy_id= buy_order["data"]["ordId"]
#     except:
        
#         dtm=str(datetime.datetime.utcnow())
#         urlll = 'http://159.65.12.9:80/trades'
#         myobj = {"trade_id":'Buy_failed',"price":0,"status":"Buy_failed","coins":00,"time":dtm,"volume":00}

#         x = requests.post(urlll, json = myobj)
#         sys.exit("Error ")
#     try:
#         sell_order=sell(api_key,secret_key,price,qtyo,symbol)
#         print(sell_order)
#         sell_id= sell_order["data"]["ordId"]
#     except:
#         try:
#             cancel_order(api_key,secret_key,symbol,buy_id)
#         except:pass
#         try:
#             cancel_order(api_key,secret_key,symbol,sell_id)
#         except:pass
#         dtm=str(datetime.datetime.utcnow())
#         urlll = 'http://159.65.12.9:80/trades'
#         myobj = {"trade_id":'Sell_failed',"price":0,"status":"Sell_failed","coins":00,"time":dtm,"volume":00}

#         x = requests.post(urlll, json = myobj)
#         sys.exit("Error ")

# else:
#     try:
#         sell_order=sell(api_key,secret_key,price,qtyo,symbol)
#         print(sell_order)
#         sell_id= sell_order["data"]["ordId"]
#     except:
        
#         dtm=str(datetime.datetime.utcnow())
#         urlll = 'http://159.65.12.9:80/trades'
#         myobj = {"trade_id":'Buy_failed0',"price":0,"status":"Buy_failed","coins":00,"time":dtm,"volume":00}

#         x = requests.post(urlll, json = myobj)
#         sys.exit("Error ")
#     try:
        
#         buy_order=buy(api_key,secret_key,price,qtyo,symbol)
#         print(buy_order)
#         buy_id= buy_order["data"]["ordId"]
#     except:
    
#         dtm=str(datetime.datetime.utcnow())
#         urlll = 'http://159.65.12.9:80/trades'
#         myobj = {"trade_id":'Sell_failed0',"price":0,"status":"Sell_failed","coins":00,"time":dtm,"volume":00}

#         x = requests.post(urlll, json = myobj)
#         sys.exit("Error ")

# time.sleep(1)
# try:
#     cancel_order(api_key,secret_key,symbol,buy_id)
# except:pass
# try:
#     cancel_order(api_key,secret_key,symbol,sell_id)
# except:pass

# # x=0
# # while x<5:
# #     x=x+1
# #     try:
# #         cb=order_status(api_key,secret_key,buy_id)
# #         cs=order_status(api_key,secret_key,sell_id)
# #         break
# #     except:
# #         time.sleep(1)
# #         pass
# # try:
# #     if cb["data"]["ordState"] == "FILLED" and cs["data"]["ordState"] == "FILLED":
# #         dtm=str(datetime.datetime.utcnow())
# #         vol=(float(qtyo)*2)*float(price)

# #         urlll = 'http://159.65.12.9:80/trades'
# #         myobj = {"price":price,"status":"successful","coins":qtyo,"time":dtm,"volume":vol}

# #         x = requests.post(urlll, json = myobj)
# #     else:
# #         cancel_order(api_key,secret_key,symbol,buy_id)
# #         cancel_order(api_key,secret_key,symbol,sell_id)
# #         urlll = 'http://159.65.12.9:80/trades'
# #         myobj = {"price":price,"status":"failed","coins":qtyo,"time":dtm,"volume":00}

# #         x = requests.post(urlll, json = myobj)
# #         print("order failed,entering rebancing mode")
# #         acf=account_info(api_key,secret_key)
# #         for i in acf['data']:
# #             if (i['type'])==1:
# #                 if (i['currency'])=='USDT':
# #                     usdtf=float(i['balance'])
# #         for i in acf['data']:
# #             if (i['type'])==1:
# #                 if (i['currency'])==(symbol.replace('USDT','')):
# #                     basef=float(i['balance'])
# #         if (usdti-usdtf)>(usdti*0.01):
# #             req_usdt=usdti-usdtf
# #             qq=basef-basei
# #             sell_market(api_key,secret_key,qq,symbol)
# #         if (basei-basef)>(basei*0.01):
# #             qq=basei-basef
# #             buy_market(api_key,secret_key,qq,symbol)
# #         print("Rebanced")
# # except:
# #     try:
# #         cancel_order(api_key,secret_key,symbol,buy_id)
# #         cancel_order(api_key,secret_key,symbol,sell_id)
# #         urlll = 'http://159.65.12.9:80/trades'
# #         myobj = {"price":price,"status":"failed","coins":qtyo,"time":dtm,"volume":00}

# #         x = requests.post(urlll, json = myobj)
# #         print("order failed,entering rebancing mode")
# #         acf=account_info(api_key,secret_key)
# #         for i in acf['data']:
# #             if (i['type'])==1:
# #                 if (i['currency'])=='USDT':
# #                     usdtf=float(i['balance'])
# #         for i in acf['data']:
# #             if (i['type'])==1:
# #                 if (i['currency'])==(symbol.replace('USDT','')):
# #                     basef=float(i['balance'])
# #         if (usdti-usdtf)>(usdti*0.01):
# #             req_usdt=usdti-usdtf
# #             qq=basef-basei
# #             sell_market(api_key,secret_key,qq,symbol)
# #         if (basei-basef)>(basei*0.01):
# #             qq=basei-basef
# #             buy_market(api_key,secret_key,qq,symbol)
# #         print("Rebanced")
# #     except:
# #         pass
# time.sleep(delay)
            