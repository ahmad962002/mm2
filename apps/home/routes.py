# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps import db
from apps.home import blueprint
from flask import render_template, request,redirect, jsonify
from apps.home.forms import ApiForm,SetForm
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask_login import (
    current_user
)
from apps.home.models import Binance,Set,Data,Trades
from apps.authentication.models import Users
import datetime,socket,math,time,json
from threading import Thread
import hashlib
import hmac
import json
import math
import time
import requests
from pyxt.spot import Spot
state=0

@blueprint.route('/index')
@login_required
def index():
    user = current_user.get_id()
    trades=Trades.find_all()
    # print(Trades.find_all())
    
    return render_template('home/index.html',trades=trades, segment='index',user=user)

@blueprint.route('/trades', methods=['POST'])
def tradess():
    trade = (request.json)
    trade=Trades(price=trade['price'],status=trade['status'],coins=trade['coins'],time=trade['time'],volume=trade['volume'])
    # print(request.form["api"],user)
    db.session.add(trade)
    db.session.commit()
    return('ok')
@blueprint.route('/tps', methods=['GET', 'POST'])
@login_required
def tps():
    set_form = SetForm(request.form)
    segment = get_segment(request)
    user = current_user.get_id()
    set=Set.find_by_userid(user)



    if 'connect' in request.form:
        pair = (request.form["pair"])
        qt=float(request.form["qt"])
        delay=float(request.form["delay"])
        


        try:
            Set.query.filter_by(user_id =user).delete()
            db.session.commit()
        except:
            pass
        
        settings=Set(user_id=user,pair=pair,qt=qt,delay=delay)
        # print(request.form["api"],user)
        db.session.add(settings)
        db.session.commit()
        return redirect('/tps')
    else:
        try:
            return render_template( 'home/tps.html',
                                    form=set_form,segment=segment,pair=set.pair,qt=set.qt,delay=set.delay)
        except:
            return render_template( 'home/tps.html',
                                form=set_form,segment=segment,pair="XRPUSDT",qt=1,delay=120)


@blueprint.route('/ex', methods=['GET', 'POST'])
@login_required
def binance():
    segment = get_segment(request)
    user = current_user.get_id()
    user_check = Binance.query.filter_by(user_id =user).first()
    if user_check:
        try:
            api=Binance.find_by_userid(user)
            appi=api.api
            secc=api.secret
            xt = Spot(host="https://sapi.xt.com", access_key=appi, secret_key=secc)
            usdt=(xt.balance("usdt"))
            
            return render_template( 'home/binance_dash.html',segment=segment,user=user,usdt=usdt)
        except:
            Binance.query.filter_by(user_id =user).delete()
            db.session.commit()
            return redirect('/ex')
            
    else:
        api_form = ApiForm(request.form)
        if 'connect' in request.form:
            appi=str(request.form["api"])
            secc=str(request.form["secret"])
            
            try:
                api_key=appi
                secret_key=secc
                
                xt = Spot(host="https://sapi.xt.com", access_key=api_key, secret_key=secret_key)
                (xt.balance("usdt"))
            except:
                return render_template( 'home/binance.html',
                                    form=api_form,segment=segment,msg="Api or Secret is Wrong. Also Check Apikey Permissions")
            
            
            api=Binance(user_id=user,api=request.form["api"],secret=request.form["secret"])
            # print(request.form["api"],user)
            db.session.add(api)
            db.session.commit()
            return redirect('/ex')
        else:
            return render_template( 'home/binance.html',
                                    form=api_form,segment=segment,user=user)

@blueprint.route('/ex/disconnect/<user>')
@login_required
def del_binance(user):
    Binance.query.filter_by(user_id =user).delete()
    db.session.commit()
    return redirect("/ex", code=302)

        
# @blueprint.route('/gainers', methods=['POST'])
# def gainers():
#     msg=request.json
#     gainers=(msg)
#     gainer=json.dumps(msg)
#     data=Data.find()
#     data.gainers=gainer
#     db.session.commit()
#     bb=Binance.find_all()
#     for b in bb:
#         g4=dict(sorted(gainers.items(), key=lambda x: x[1], reverse=True)[:4])
#         set=Set.find_by_userid(b.user_id)
#         binance=ccxt.binanceusdm({'apiKey': b.api,'secret': b.secret,})
#         binance.load_markets
#         bal = (binance.fetch_balance())
#         balance=''
#         for i in bal:
#             if i=='USDT':
#                 balance= (bal[i])
#         usdt=(set.qt/100)*(float(balance['total']))
#         if usdt<50:
#             continue
#         usdt= usdt/4
#         uu=float(balance['free'])
#         if uu<usdt:
#             usdt=uu-(uu*0.02)
#         x=0
#         bb = (binance.fetch_positions())
#         alreadyp=[]
#         for i in bb:
#             if float(i['info']['positionAmt'])!=0:
#                 alreadyp.append(i['info']['symbol'])
#                 x=x+1
#         if x>3:
#             continue
#         if x<4:
#             for g in g4:
#                 if g in alreadyp:
#                     continue
#                 if x>3:
#                     break
#                 pair=(g)
#                 sideb='sell'
#                 sides='buy'
#                 ticker=binance.fetch_ticker(pair)
#                 price=float(ticker['close'])
#                 qty=float(binance.amount_to_precision(pair,(usdt*int(set.lev)/price)))
#                 stp=price+(((float(set.stp)/int(set.lev))/100)*price)
#                 stp=float(binance.price_to_precision(pair,stp))
#                 tp=price-(((float(set.tp)/int(set.lev))/100)*price)
#                 tp=float(binance.price_to_precision(pair,tp))
#                 try:
#                     binance.set_leverage(int(set.lev),pair)
#                 except:
#                     pass
#                 try:
                    
#                     binance.set_margin_mode(set.mode,pair)
#                 except:
#                     pass
#                 try:
#                     binance.cancel_all_orders(pair)
#                 except:
#                     pass
#                 try:
#                     binance.create_order(pair,'MARKET',sideb,qty)
#                     x = x+1
#                 except:
#                     continue
#                 binance.create_order(pair,'STOP_MARKET',sides,amount='',price='',params={'closePosition':'true','stopPrice':stp})
#                 binance.create_order(pair,'TAKE_PROFIT_MARKET',sides,amount='',price='',params={'closePosition':'true','stopPrice':tp})
                
#     return('done')    
                
                
            
            
#     #     b = (binance.fetch_balance())
#     #     balance=''
#     #     for i in b:
#     #         if i=='USDT':
#     #             balance= (b[i])
#     #     for new_s, new_val in gainers.items():
#     #         pair=(new_s)
#     #         bb = (binance.fetch_positions())
#     #         for i in bb:
#     #             if float(i['info']['positionAmt'])!=0:
#     #                 continue
#     #         break
#     #     print(pair)
#     #     usdt=(set.qt/100)*(float(balance['free']))/4
#     #     ticker=binance.fetch_ticker(pair)
#     #     price=float(ticker['close'])
#     #     qty=float(binance.amount_to_precision(pair,(usdt*int(set.lev)/price)))
#     #     sideb='sell'
#     #     sides='buy'
#     #     stp=price+(((float(set.stp)/int(set.lev))/100)*price)
#     #     stp=float(binance.price_to_precision(pair,stp))
#     #     tp=price-(((float(set.tp)/int(set.lev))/100)*price)
#     #     tp=float(binance.price_to_precision(pair,tp))
#     #     try:
#     #         binance.cancel_all_orders(pair)
#     #     except:
#     #         pass
#     #     try:
#     #         binance.set_leverage(int(set.lev),pair)
#     #     except:
#     #         pass
            
#     #     main=binance.create_market_order(pair,sideb,qty)
#     #     stp=(binance.create_order(
#     #                 symbol=pair,
#     #                 type='STOP_MARKET',
#     #                 side=sides,
#     #                 amount=qty,
#     #                 params={
#     #                     'stopPrice': stp,   
#     #                 }
#     #             ))
#     #     tp=(binance.create_order(
#     #                 symbol=pair,
#     #                 type='TAKE_PROFIT_MARKET',
#     #                 side=sides,
#     #                 amount=qty,
#     #                 params={
#     #                     'stopPrice':tp,
#     #                 }
#     #             ))

          

#     # return('done')



# @blueprint.route('/bot_start', methods=['POST'])
# def signal():
#     if state==1:
#         return('already running')
#     if request.method == 'POST':
#         while True:
#             state==1
#             try:
#                 try:
#                     set=Set.find_by_userid(1)
#                     symbol=set.pair
#                     qty=set.qt
#                     delay=set.delay
#                     api=Binance.find_by_userid(1)
#                     appi=api.api
#                     secc=api.secret
#                     api_key=appi.encode('utf-8')
#                     secret_key=secc.encode('utf-8')

                    
                
#                 except:
#                     time.sleep(60)
#                     continue
#                 url = f"https://api.coinstore.com/api//v2/public/config/spot/symbols"
#                 expires = int(time.time() * 1000)
#                 expires_key = str(math.floor(expires / 30000))
#                 expires_key = expires_key.encode("utf-8")
#                 key = hmac.new(secret_key, expires_key, hashlib.sha256).hexdigest()
#                 key = key.encode("utf-8")
#                 payload = json.dumps({"symbolCodes":[symbol] })
#                 payload = payload.encode("utf-8")
#                 signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
#                 headers = {
#                     'X-CS-APIKEY': api_key,
#                 'X-CS-SIGN': signature,
#                 'X-CS-EXPIRES': str(expires),
#                 'exch-language': 'en_US',
#                 'Content-Type': 'application/json',
#                 'Accept': '*/*',
#                 # 'Host': 'https://api.coinstore.com',
#                 'Connection': 'keep-alive'
#                 }
#                 response = requests.request("POST", url, headers=headers, data=payload)
#                 info=json.loads(response.text)
#                 pricen=int(info['data'][0]['tickSz'])
#                 qtyn=int(info['data'][0]['lotSz'])
#                 if qtyn==0:
#                     qty=str(int(qty))
#                 if qtyn==1:
#                     qty=qty*10
#                     qty=(int(qty))
#                     qty=str(qty/10)
#                 if qtyn==2:
#                     qty=qty*100
#                     qty=(int(qty))
#                     qty=str(qty/100)
#                 if qtyn==3:
#                     qty=qty*1000
#                     qty=(int(qty))
#                     qty=str(qty/1000)
#                 if qtyn==4:
#                     qty=qty*10000
#                     qty=(int(qty))
#                     qty=str(qty/10000)
#                 if qtyn==5:
#                     qty=qty*100000
#                     qty=(int(qty))
#                     qty=str(qty/100000)
#                 if qtyn==6:
#                     qty=qty*1000000
#                     qty=(int(qty))
#                     qty=strCompu943377#(qty/1000000)
#                 if qtyn==7:
#                     qty=qty*10000000
#                     qty=(int(qty))
#                     qty=str(qty/10000000)
#                 if qtyn==8:
#                     qty=qty*100000000
#                     qty=(int(qty))
#                     qty=str(qty/100000000)
#                 else:
#                     pass
#                 try:
#                     url = f"https://api.coinstore.com/api/v1/market/depth/{symbol}"
#                     expires = int(time.time() * 1000)
#                     expires_key = str(math.floor(expires / 30000))
#                     expires_key = expires_key.encode("utf-8")
#                     key = hmac.new(secret_key, expires_key, hashlib.sha256).hexdigest()
#                     key = key.encode("utf-8")
#                     payload = json.dumps({"symbol":symbol,
#                                         "depth": 1 })
#                     payload = payload.encode("utf-8")
#                     signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
#                     headers = {
#                         'X-CS-APIKEY': api_key,
#                     'X-CS-SIGN': signature,
#                     'X-CS-EXPIRES': str(expires),
#                     'exch-language': 'en_US',
#                     'Content-Type': 'application/json',
#                     'Accept': '*/*',
#                     # 'Host': 'https://api.coinstore.com',
#                     'Connection': 'keep-alive'
#                     }
#                     response = requests.request("GET", url, headers=headers, data=payload)
                    
#                     r=(json.loads(str(response.text)))
#                     a=float(r['data']['a'][0][0])
#                     b=(float(r['data']['b'][0][0]))
#                     p = (a+b)/2
#                     p= str(round(p,pricen))
#                     url = "https://api.coinstore.com/api/trade/order/place"

#                     expires = int(time.time() * 1000)
#                     expires_key = str(math.floor(expires / 30000))
#                     expires_key = expires_key.encode("utf-8")
#                     key = hmac.new(secret_key, expires_key, hashlib.sha256).hexdigest()
#                     key = key.encode("utf-8")

#                     payload = json.dumps({
#                         "ordPrice": p ,
#                     "ordQty": qty,
#                     # "clOrdId": "8vdpfHC0LmhojVIffOlkBc9bV9992",
#                     "symbol": symbol,
#                     "side": "BUY",
#                     "ordType": "LIMIT"
#                     })
#                     payload1 = json.dumps({
#                         "ordPrice": p ,
#                     "ordQty": qty,
#                     # "clOrdId": "8vdpfHC0LmhojVIffOlkBc9bV9992",
#                     "symbol": symbol,
#                     "side": "SELL",
#                     "ordType": "LIMIT"
#                     })
#                     payload = payload.encode("utf-8")
#                     payload1 = payload1.encode("utf-8")
#                     signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
#                     signature1 = hmac.new(key, payload1, hashlib.sha256).hexdigest()
#                     headers = {
#                         'X-CS-APIKEY': api_key,
#                     'X-CS-SIGN': signature,
#                     'X-CS-EXPIRES': str(expires),
#                     'exch-language': 'en_US',
#                     'Content-Type': 'application/json',
#                     'Accept': '*/*',
#                     # 'Host': 'https://api.coinstore.com',
#                     'Connection': 'keep-alive'
#                     }
#                     headers1 = {
#                         'X-CS-APIKEY': api_key,
#                     'X-CS-SIGN': signature1,
#                     'X-CS-EXPIRES': str(expires),
#                     'exch-language': 'en_US',
#                     'Content-Type': 'application/json',
#                     'Accept': '*/*',
#                     # 'Host': 'https://api.coinstore.com',
#                     'Connection': 'keep-alive'
#                     }
#                     response = requests.request("POST", url, headers=headers, data=payload)
#                     response1 = requests.request("POST", url, headers=headers1, data=payload1)
#                     print(response.text)
#                     print(response1.text)
#                     time.sleep(delay)
#                 except:
#                     url = "https://api.coinstore.com/api/spot/accountList"
#                     expires = int(time.time() * 1000)
#                     expires_key = str(math.floor(expires / 30000))
#                     expires_key = expires_key.encode("utf-8")
#                     key = hmac.new(secret_key, expires_key, hashlib.sha256).hexdigest()
#                     key = key.encode("utf-8")
#                     payload = json.dumps({})
#                     payload = payload.encode("utf-8")
#                     signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
#                     headers = {
#                         'X-CS-APIKEY': api_key,
#                     'X-CS-SIGN': signature,
#                     'X-CS-EXPIRES': str(expires),
#                     'exch-language': 'en_US',
#                     'Content-Type': 'application/json',
#                     'Accept': '*/*',
#                     #  'Host': 'https://api.coinstore.com',
#                     'Connection': 'keep-alive'
#                     }
#                     response = requests.request("POST", url, headers=headers, data=payload)
#                     ac=json.loads(response.text)
#                     for i in ac['data']:
#                         if (i['type'])==1:
#                             if (i['currency'])==(symbol.replace('USDT','')):
#                                 amt=float(i['balance'])
#                     if amt:   
#                         amt=str(round(amt,qtyn))
#                         url = "https://api.coinstore.com/api/trade/order/place"
#                         expires = int(time.time() * 1000)
#                         expires_key = str(math.floor(expires / 30000))
#                         expires_key = expires_key.encode("utf-8")
#                         key = hmac.new(secret_key, expires_key, hashlib.sha256).hexdigest()
#                         key = key.encode("utf-8")
#                         payload = json.dumps({
#                         "ordQty": amt,
#                         # "clOrdId": "8vdpfHC0LmhojVIffOlkBc9bV9992",
#                         "symbol": symbol,
#                         "side": "SELL",
#                         "ordType": "MARKET"
#                         })
#                         payload = payload.encode("utf-8")
#                         signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
#                         headers = {
#                             'X-CS-APIKEY': api_key,
#                         'X-CS-SIGN': signature,
#                         'X-CS-EXPIRES': str(expires),
#                         'exch-language': 'en_US',
#                         'Content-Type': 'application/json',
#                         'Accept': '*/*',
#                         # 'Host': 'https://api.coinstore.com',
#                         'Connection': 'keep-alive'
#                         }
#                         response = requests.request("POST", url, headers=headers, data=payload)
#                         print(response.text)
#                     else:
#                         pass

#                     continue
#             except:
#                 time.sleep(3)
                            
                        
                        
#         return('done')        
#         # user = current_user.get_id()
#         # api=Bybit.find_by_userid(user)
#         # bybit=ccxt.bybit({'apiKey': api.api,'secret': api.secret,})


    



# @blueprint.route('/bybit/disconnect/<user>')
# @login_required
# def del_bibit(user):
#     Bybit.query.filter_by(user_id =user).delete()
#     db.session.commit()
#     return redirect("/bybit", code=302)
# @blueprint.route('/<template>')
# @login_required
# def route_template(template):

#     try:

#         if not template.endswith('.html'):
#             template += '.html'

#         # Detect the current page
#         segment = get_segment(request)

#         # Serve the file (if exists) from app/templates/home/FILE.html
#         return render_template("home/" + template, segment=segment)

#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404

#     except:
#         return render_template('home/page-500.html'), 500


# # Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment
    except:
        return None

