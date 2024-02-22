import ccxt

bybit=ccxt.bybit({})
base='BTCUSDT'
quote=''
ticker=bybit.create_market_order('BTCUSDT','buy','10')
price=(ticker['close'])
