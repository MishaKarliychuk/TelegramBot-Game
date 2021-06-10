# import requests
# from liqpay import LiqPay
# import time
# import urllib3
# urllib3.disable_warnings()
# import json
# import asyncio

# public_key = 'i77803829040'
# private_key = 'rZIKxVI3hhmVF4ihWzjyGEQ9fJgPyHluh4jXKMRC'

# async def make_req(summ,phone,random_id):
# 	liqpay = LiqPay(public_key, private_key)
# 	res = liqpay.api("request", {
# 	"action"    : "invoice_bot",
# 	"version"   : "3",
# 	"amount"    : str(summ),
# 	"currency"  : "UAH",
# 	"order_id"  : random_id,
# 	"phone"  : str(phone)
# 	})
# 	#js = json.loads(str(res))
# 	print(f'Full result: {res}')
# 	return res["href"]

# async def get_result(random_id):
# 	liqpay2 = LiqPay(public_key, private_key)
# 	res = liqpay2.api("request", {
# 	"action"        : "status",
# 	"version"       : "3",
# 	"order_id"      : random_id
# 	})
# 	#js = json.loads(str(res))
# 	print(f'Full result: {res}')
# 	return res['status']



# def makes(summ,phone,random_id):
# 	liqpay = LiqPay(public_key, private_key)
# 	res = liqpay.api("request", {
# 	"action"    : "invoice_bot",
# 	"version"   : "3",
# 	"amount"    : str(summ),
# 	"currency"  : "UAH",
# 	"order_id"  : random_id,
# 	"phone"  : str(phone)
# 	})
# 	#js = json.loads(str(res))
# 	print(f'Full result: {res}')
# 	return res["id"]  



from cloudipsp import Api, Checkout
import requests
from cloudipsp import Order


async def create_pay(ID, SUMM):
	api = Api(merchant_id=1473484, secret_key='SfJwnYafQZqWx97WU2sOtp7FM4KY9F5t') 		# заменить данные под свои
	checkout = Checkout(api=api)
	data = {
		'order_id': ID,
	    "amount": SUMM,
	    "order_desc":"registration",
	    "currency": "UAH",
	    "merchant_id": '1473484',
	    "response_url": 'https://t.me/kmn_bmg_bot',
	    "lifetime": 600
	}

	url = checkout.url(data)
	return url['checkout_url']

async def check(ID):
	api = Api(merchant_id=1473484, secret_key='SfJwnYafQZqWx97WU2sOtp7FM4KY9F5t')
	ordd = Order(api=api)
	st = ordd.status({'order_id': ID})
	print(st)	
	return st['order_status']

 
