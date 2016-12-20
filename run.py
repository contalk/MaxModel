#!/usr/bin/python  
# -*- coding:utf-8 -*- 

from core import futu
from core import timer
from core import config
import time
import redis
import json

#futu = futu.Futu(config.futu)
"""
re = redis.Redis(config.redis_host, config.redis_port)
re.set("hello", "world1")
r = re.get("hello")
print r
exit()
"""
maxRedis = redis.Redis(config.max_redis_port, config.max_redis_port)
#maxRedis.set("hello", "world2")
r = maxRedis.get("hello")
print maxRedis
exit()



#r = futu.get_price('jd.us') #done
#r = futu.get_gear('00700.hk') #donemarket
#r = futu.get_hold_list('hk')
#r = futu.buy('00700.hk', 184, 100)


while True:
	hold_list = futu.get_hold_list('hk') #done
	if len(hold_list) > 0:
		for symbol, item in hold_list.items():
			channel = 'hold:'+symbol
			redis.publish(channel, item)

	time.sleep(1)
	exit()
