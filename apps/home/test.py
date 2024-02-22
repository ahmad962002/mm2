from pyxt.spot import Spot
api_key = "8ae3c013-29e2-4f5b-b6a8-ae3ae8cb9e0c"
secret_key = "aeecfbe7fe4e634be376ad5a82be3eb7b371d0f4"
xt = Spot(host="https://sapi.xt.com", access_key=api_key, secret_key=secret_key)
tt=xt.get_depth('ramsena_usdt',2)
p_pre=(xt.get_symbol_config(symbol='ramsena_usdt')[0]['pricePrecision'])
q_pre=(xt.get_symbol_config(symbol='ramsena_usdt')[0]['quantityPrecision'])
high=float(tt['asks'][0][0])
low=float(tt['bids'][0][0])
pp=((high+low)/2)
pp=round(pp,p_pre)
# res = xt.order(symbol='ramsena_usdt', price=pp, quantity=10, side='SELL', type='LIMIT')
# print(res)
res = xt.cancel_order(order_id=330923951932860288)
print(res)
