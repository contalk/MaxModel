#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import socket
import sys
import string

import time
import thread
import threading

import math
import codecs
import traceback

class Futu():

	config = {}
	trade_locked = 1

	PROTO_PRICE = 1001
	PROTO_GEAR = 1002
	PROTO_UNLOCK = 6006

	PROTO_HK_SET_ORDER = 6003
	PROTO_HK_SET_ORDER_STATUS = 6004
	PROTO_HK_UPDATE_ORDER = 6005
	PROTO_HK_ACCOUNT = 6007
	PROTO_HK_ORDER_LIST = 6008
	PROTO_HK_HOLD_LIST = 6009

	PROTO_US_SET_ORDER = 7003
	PROTO_US_SET_ORDER_STATUS = 7004
	PROTO_US_UPDATE_ORDER = 7005
	PROTO_US_ACCOUNT = 7007
	PROTO_US_ORDER_LIST = 7008
	PROTO_US_HOLD_LIST = 7009
	VERSION = '1'

	def __init__(self, config):
		self.config = config
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.config['host'], self.config['port']))
		self.lock = thread.allocate_lock()

	def __del__(self):
		self.s.close()

	def __check_symbol(self, symbol):
		symbol = symbol.strip().upper()
		arr = symbol.split('.')
		if len(arr)==2:
			rs = {}
			rs['Market'] = arr[1]
			rs['StockCode'] = arr[0]
			return rs
		else:
			print('symbol code error')
			return None

	def __get_market_code(self, market):
		market = market.strip().upper()
		marketCode = {
			'HK':'1', 
			'US':'2', 
			'SH':'3', 
			'SZ':'4'
			}
		if marketCode.has_key(market):
			return marketCode[market]
		else:
			print('market code error')
			return None

	def __call(self, command, param):
		self.lock.acquire()
		try:
			req = {
				'Protocol':str(command),
				'ReqParam': param,
				'Version':self.VERSION
				} 		
			mystr = json.dumps(req) + '\n'
			self.s.send(mystr) 
			rsp = ""
			buf = self.s.recv(4096)
			mybuf = buf.split("\r\n")
			for rsp in mybuf:
				if len(rsp) > 2:
					try:
						rsp = rsp.decode('utf-8')
					except Exception, e:
						rsp = rsp.decode('gbk')
					r = json.loads(rsp)

					#if r["Protocol"] == self.PROTO_US_SET_ORDER or r["Protocol"] == self.PROTO_HK_SET_ORDER or r["Protocol"] == self.PROTO_HK_SET_ORDER_STATUS or r["Protocol"] == self.PROTO_HK_UPDATE_ORDER:
					#	if r['ErrCode'] > 0 :
					#		print r['ErrCode'],r['ErrDesc']
					if r['ErrCode'] == '0' :
						self.lock.release()
						return r["RetData"]
					else:
						print r['ErrCode'],r['ErrDesc']   			 			
		except Exception, e:
			exstr = traceback.format_exc()
			print exstr
		self.lock.release()   	
		return None

	def get_account(self, market):
		req = {
			'Cookie':self.config['uid'],
		  	'EnvType':self.config['env'],
		  	}
		if market.upper()=='HK':
			return self.__call(self.PROTO_HK_ACCOUNT, req)
		elif market.upper()=='US':
		  	return self.__call(self.PROTO_US_ACCOUNT, req)
		else:
		  	return None

	def __unlock(self):
		req = {
			'Cookie':str(self.config['uid']),
		  	'Password':str(self.config['pwd']),
		  	}
		return self.__call(self.PROTO_UNLOCK, req)
	  
	def get_price(self, symbol):
		r = self.__check_symbol(symbol)
		if r is not None:
			req = {
				'Market':self.__get_market_code(r['Market']),
			  	'StockCode':r['StockCode'],
				}
			data = self.__call(self.PROTO_PRICE, req)
			if(data is not None):
				for i in ('Cur','High','Low', 'Close', 'Open', 'LastClose', 'Turnover'):
				  	data[i] = round(float(data[i]) / 1000, 3)
				  	data['Vol'] = int(data['Vol'])
				return data
		return None

	def get_gear(self, symbol, num = 1):
		r = self.__check_symbol(symbol)
		if r is not None:
			req = {
				'Market':self.__get_market_code(r['Market']),
			  	'StockCode':r['StockCode'],
			  	'GetGearNum':str(num)
				}
			data = self.__call(self.PROTO_GEAR, req)
			if data is not None:
				for i in data['GearArr']:
			  		i['BuyPrice'] = round(float(i['BuyPrice']) / 1000,3)
			  		i['BuyVol'] = int(i['BuyVol'])
			  		i['SellPrice'] = round(float(i['SellPrice']) / 1000,3)
			  		i['SellVol'] = int(i['SellVol'])
				return data['GearArr']
		return None

	#暂只支持限价 OrderType = 0 
	def buy(self, symbol, price, volume):
		r = self.__check_symbol(symbol)
		if r is not None:
			#解锁
			if self.trade_locked == 0:
				self.__unlock()
				self.trade_locked = 1

			#HK
			OrderType = 0
			Protocol = self.PROTO_HK_SET_ORDER
			if r['Market'] == 'US' :
				OrderType = 2
				Protocol = self.PROTO_US_SET_ORDER

			req = {
				'Cookie': str(self.config['uid']),
				'OrderSide':'0',
				'OrderType':str(OrderType),
				'Price':str(int(math.floor(price * 1000))),
				'Qty': str(int(volume)),
				'StockCode':str(r['StockCode']),
				'EnvType': str(self.config['env'])
				}
			return self.__call(Protocol, req)
		return None

	def sell(self, symbol, price, volume):
		r = self.__check_symbol(symbol)
		if r is not None:
			#解锁
			if self.trade_locked == 0:
				self.__unlock()
				self.trade_locked = 1
			#HK
			OrderType = 0
			Protocol = self.PROTO_HK_SET_ORDER
			if r['Market'] == 'US' :
				OrderType = 2
				Protocol = self.PROTO_US_SET_ORDER

			req = {
				'Cookie':str(self.config['uid']),
				'OrderSide':'1',
				'OrderType':str(OrderType),
				'Price':str(int(math.floor(price * 1000))),
				'Qty': str(volume),
				'StockCode':str(r['StockCode']),
				'EnvType': str(self.config['env'])
				}
			return self.__call(Protocol, req)
		return None

	def cancel(self, market, LocalID):
		Protocol = self.PROTO_HK_SET_ORDER_STATUS
		if market.upper() == 'US':
			Protocol = self.PROTO_US_SET_ORDER_STATUS

		req = {
			'Cookie':str(self.config['uid']),
		  	'LocalID':str(LocalID),
		  	'SetOrderStatus':'0',
		  	'EnvType':str(self.config['env'])
		  	}
		return self.__call(Protocol, req)

	def update(self, market, LocalID, price, amount):
		Protocol = self.PROTO_HK_UPDATE_ORDER
		if market.upper() == 'US':
			Protocol = self.PROTO_US_UPDATE_ORDER

		req = {
			'Cookie':str(self.config['uid']),
		  	'LocalID':str(LocalID),
		  	'Price':int(math.floor(price * 1000)),
		  	'Qty': str(amount),
		  	'EnvType':str(self.config['env'])
		  	}
		print req
		return self.__call(Protocol, req)

	def get_order_list(self, market):
		req = {
			'Cookie':str(self.config['uid']),
		  	'EnvType':str(self.config['env'])
		  	}
		if market.upper() == 'HK':
		  	return self.__call(self.PROTO_HK_ORDER_LIST, req)
		elif market.upper() == 'US':
		  	return self.__call(self.PROTO_US_ORDER_LIST, req)

	def get_hold_list(self, market):
		market = market.upper()
		req = {
			'Cookie':str(self.config['uid']),
		  	'EnvType':str(self.config['env'])
		  	}
		hold_list = {}
		rs = {}
		key = 'HKPositionArr'
		if market == 'HK':
			rs = self.__call(self.PROTO_HK_HOLD_LIST, req) 				
		elif market == 'US':
		  	rs = self.__call(self.PROTO_US_HOLD_LIST, req)
		  	key = 'USPositionArr'
			
		if rs.has_key(key) and len(rs[key]) > 0:		
			for row in rs[key]:
				item = {}
				code = str(row['StockCode'])+'.'+market
				item['Qty'] = row['Qty']
				item['MarketVal'] = round(float(row['MarketVal']) / 1000, 3)
				item['CostPrice'] = round(float(row['CostPrice']) / 1000, 3)
				hold_list[code] = item

		return hold_list


