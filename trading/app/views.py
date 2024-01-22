import json
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from kraken.futures import Trade, User
from kraken.spot import User as Suser, Trade as Strade

from .models import Order

##########################
# Config
##########################
key = os.environ.get('KEY')
secret = os.environ.get('SECRET')
spot_key = os.environ.get('SPOT_KEY')
spot_secret = os.environ.get('SPOT_SECRET') 

# Create your views here.
def ping(request):
    data = {"ping": "pong"}
    return JsonResponse(data)

@csrf_exempt
def trade(request):
    trade = Trade(key=key, secret=secret, sandbox=True)
    user = User(key=key, secret=secret, sandbox=True)
    strade = Strade(key=spot_key, secret=spot_secret)
    suser = Suser(key=spot_key, secret=spot_secret)

    size = '0.0003'
    
    if request.method == 'POST' :
        data = json.loads(request.body)
        print(data)
        action = data['action']
        type = data['type']

        # FUTURES
        futures_long = {
            'orderType':'mkt',
            'symbol':'PF_XBTUSD',
            'side':'buy',
            'size': size
        }
        futures_short = {
            'orderType':'mkt',
            'symbol':'PF_XBTUSD',
            'side':'sell',
            'size': size
        }

        # TRADE

        # futures
        if type== "futures" :
            if action == "long_entry" :
                long_order = trade.create_order(**dict(futures_long))
                #order = Order.objects.create(order_id=long_order['clientOrderId'], order_direction="long", order_amount_open=long_order['origQty'], order_amount=long_order['origQty'])
                #order.save()
                print(long_order)
                return JsonResponse(long_order)

            if action == "short_entry" :
                short_order = trade.create_order(**dict(futures_short))
                #order = Order.objects.create(order_id=long_order['clientOrderId'], order_direction="long", order_amount_open=long_order['origQty'], order_amount=long_order['origQty'])
                #order.save()
                print(short_order)
                return JsonResponse(short_order)

            # close futures
            if action == "close_position" :
                res = user.get_open_positions()
                if res['openPositions'] : 
                    direction = res['openPositions'][0]['side']
                    if direction == 'long' :
                        side = 'sell'
                    elif direction == 'short' :
                        side = 'buy'
                    else :
                        return 
                    
                    close_position = trade.create_order(
                                    orderType='mkt',
                                    symbol='PF_XBTUSD',
                                    side=side,
                                    size=size
                                )
                    print(close_position)
                    return JsonResponse(close_position)
                else :
                    data = {"Result": "No open futures positions"}
                    return JsonResponse(data)

            else :
                data = {"Result": "Unknown action"}
                return JsonResponse(data)



        # spot
        if type== "spot" :
            if action == "long_entry" :
                long_order = strade.create_order(ordertype='market',pair='BTCUSD', side='buy',volume=size, leverage='3')
                #order = Order.objects.create(order_id=long_order['clientOrderId'], order_direction="long", order_amount_open=long_order['origQty'], order_amount=long_order['origQty'])
                #order.save()
                print(long_order)
                return JsonResponse(long_order)

            if action == "short_entry" :
                short_order = strade.create_order(ordertype='market',pair='BTCUSD', side='sell',volume=size, leverage='3')
                #order = Order.objects.create(order_id=long_order['clientOrderId'], order_direction="long", order_amount_open=long_order['origQty'], order_amount=long_order['origQty'])
                #order.save()
                print(short_order)
                return JsonResponse(short_order)
            
            if action == "close_position" :
                res = suser.get_open_positions()
                if res:
                    direction = res[0]['type']
                    if direction == 'buy' :
                        side = 'sell'
                    elif direction == 'sell' :
                        side = 'buy'
                    else :
                        return 
                    
                    close_position = strade.create_order(ordertype='market',pair='BTCUSD', side=side,volume=size, leverage='3')
                    print(close_position)
                    return JsonResponse(close_position)
                else :
                    data = {"Result": "No open positions"}
                    return JsonResponse(data)

                    
    else :
        # GET POSITIONS
        res = user.get_open_positions()
        print(res)
        return JsonResponse(res)

@csrf_exempt
def account(request):
    user = User(key=key, secret=secret, sandbox=True)
           
    # GET ACCOUNT INFO
    res = user.get_wallets()
    print(res)
    return JsonResponse(res['accounts']['flex']['balanceValue'], safe=False)
