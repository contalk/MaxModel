#!/usr/bin/python  
# -*- coding:utf-8 -*- 

import redis
from core import futu
from core import config


class Warrant():

	_hold_list = {}
	underlying = ''
	def __init__(self, underlying):
		self.underlying = underlying
		self.redis = redis.Redis(config.redis_host, config.redis_port)
		self.futu = futu.Futu(config.futu)

		self.init_trade_list(self.underlying)

	def handle(self, msg):
		self.update_hold_list('HK')
		print msg, self._hold_list

	def listen_sign(self):
		ps = self.redis.pubsub()  
		ps.subscribe('sign:00700.HK')
		for msg in ps.listen():
			r = str(msg['data']).split('|')
			if len(r)==2 and (r[0] == 'up' or r[0]=='down'):
				self.trade_change(r[0], r[1])

	def trade_change(trend, diff):
		holds = self.futu.get_hold_list(market)
		op = 'call'
		if trend == 'down':
			op = 'put'

		key =  "trade:"+str(op)+":"+underlying
		warrants = iredis.zrange(key, 0, 4)
		if len(warrants) > 0:
			for warrant in warrants:
				r = ft.get_gear(warrant)
				print r
			

if __name__ == '__main__':
	underlying = '00700.HK'
	Warrant = Warrant(underlying)
	Warrant.listen_sign()
	
