import json
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from kraken.futures import User, Trade

from .models import Order

##########################
# Config
##########################
key = os.environ.get('KEY')
secret = os.environ.get('SECRET') 

# Create your views here.
def ping(request):
    data = {"ping": "pong"}
    return JsonResponse(data)

@csrf_exempt
def trade(request):
    trade = Trade(key=key, secret=secret, sandbox=True)
    user = User(key=key, secret=secret, sandbox=True)

    size = '0.0006'
    
    if request.method == 'POST' :
        data = json.loads(request.body)
        print(data)
        action = data['action']

        ##########################
        # LONG
        ##########################
        if action == "long_entry" :
            long_order = trade.create_order(
                orderType='mkt',
                symbol='PF_XBTUSD',
                side='buy',
                size=size
            )
            #order = Order.objects.create(order_id=long_order['clientOrderId'], order_direction="long", order_amount_open=long_order['origQty'], order_amount=long_order['origQty'])
            #order.save()
            print(long_order)
            return JsonResponse(long_order)

        if action == "short_entry" :
            short_order = trade.create_order(
                orderType='mkt',
                symbol='PF_XBTUSD',
                side='sell',
                size=size
            )
            #order = Order.objects.create(order_id=short_order['clientOrderId'], order_direction="short", order_amount_open=short_order['origQty'], order_amount=short_order['origQty'])
            #order.save()
            print(short_order)
            return JsonResponse(short_order)


        ##########################
        # CLOSE
        ##########################
        if action == "close_position" :
            res = user.get_open_positions()
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
        ##########################
        # GET POSITIONS
        ##########################
        res = user.get_open_positions()
        print(res)
        return JsonResponse(res)

@csrf_exempt
def account(request):
    user = User(key=key, secret=secret, sandbox=True)
           
    ##########################
    # GET ACCOUNT INFO
    ##########################
    res = user.get_wallets()
    print(res)
    return JsonResponse(res['accounts']['flex']['balanceValue'], safe=False)
