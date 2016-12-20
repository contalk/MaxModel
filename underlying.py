#!/usr/bin/python  
# -*- coding:utf-8 -*- 
'''
	跟踪正股
'''
import time
from core import config
from core import timer
from core import futu
from core import util

import redis
import json
import sys 

class Underlying():

	underlying = ''	
	price_sn = []
	sn_max = 0
	sn_min = 0
	sn = 60
	diff_limit = 0.5
	ts = 0

	def __init__(self, underlying):
		self.ft = futu.Futu(config.futu)
		self.re = redis.Redis(config.redis_host, config.redis_port)
		self.underlying = underlying


	def handle(self, arg):
		self.ts = int(time.time())
		r = self.ft.get_price(self.underlying)
		self.handle_price(r)

		line = json.dumps(r) + '\n'
		util.file('data/'+self.underlying, line)
		t1 = timer.CountDownExec(1, _underlying.handle, 'hello')
		t1.start()

	def handle_price(self, data):
		
		#if cur_price > 0:
		#	key = 'price_list:'+self.underlying
		#	self.re.zadd(key, cur_price, ts)
		#	top = self.re.zrevrange(key, 0, -1, withscores=True)  
		
		cur_price = data['Cur']
		self.price_sn.insert(0, cur_price)
		if len(self.price_sn) > self.sn:
			self.price_sn.pop()

			self.sn_max = max(self.price_sn)
			self.sn_min = min(self.price_sn)
			self.sn_avg = sum(self.price_sn) / self.sn
		
			msg = 'wait'
			diff = round(self.sn_max - self.sn_min, 3)
			if diff >= self.diff_limit:
				if cur_price >= self.sn_max:
					msg = 'up'
				elif cur_price <= self.sn_min:
					msg = 'down'

			channel = 'sign:'+self.underlying
			msg = msg + '|' + str(diff)
			print msg
			self.re.publish(channel, msg) 


if __name__ == '__main__':

	underlying = sys.argv[1]
	_underlying = Underlying(underlying)
	
	t1 = timer.CountDownExec(1, _underlying.handle, 'hello')
	t1.start()
