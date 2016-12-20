#!/usr/bin/python  
# -*- coding:utf-8 -*- 

"""
加载数据
"""
import redis
import MySQLdb

from core import config
iredis = redis.Redis(config.max_redis_host, config.max_redis_port, config.max_redis_db, config.max_redis_pwd)

iredis2 = redis.Redis(config.redis_host, config.redis_port)

def load_warrant_to_redis(underlying = ''):
	conn = MySQLdb.connect(config.max_mysql_host, config.max_mysql_user, config.max_mysql_pwd,"doge",charset="utf8")
	cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
	cols = "`code`,`name`,`type`,`underlying`,`issuer`,`issue_size`,`issue_price`,`strike_price`,`call_price`,`lot_size`, `exchange_ratio`,`listing_date`,`maturity_date`,`ft_id`,`state`"
	sql = "select "+cols+" from tb_warrant_base where `state`>= 0"
	if underlying != '':
		sql = sql + " and `underlying`=" + str(underlying)

	cursor.execute(sql)
	for row in cursor.fetchall():
		key = str(row['code'])+'.HK'
		iredis.set(key, row)
		iredis.sadd("wr:"+underlying+'.HK', key)

def update_follow_list(underlying, top = 20):
	get_follow_list_type(underlying, 'call', top)
	get_follow_list_type(underlying, 'put', top)
	get_follow_list_type(underlying, 'bull', top)
	get_follow_list_type(underlying, 'bear', top)

def get_follow_list_type(underlying, type, top = 20):
	date = '20161219'
	conn = MySQLdb.connect(config.max_mysql_host, config.max_mysql_user, config.max_mysql_pwd,"doge",charset="utf8")
	cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
	sql = "SELECT `code`,type, AVG(ask_bid) AS ask_bid  FROM tb_warrant_grade WHERE underlying='"+str(underlying)+"' AND dt="+str(date)+" AND ask>0 AND bid>0 AND price>0.05 AND type = '"+str(type)+"' GROUP BY `code` HAVING ask_bid<2 ORDER BY ask_bid ASC LIMIT "+str(top)
	cursor.execute(sql)
	for row in cursor.fetchall():
		key = "follow:"+str(type)+":"+str(underlying)+'.HK'
		warrant = str(row['code'])+'.HK'
		score = int(row['ask_bid']*1000)
		iredis2.zadd(key, warrant, score)	

def update_trade_list(underlying, top = 5):
	types = ['call', 'put', 'bull', 'bear']
	for type in types:
		key = "follow:"+str(type)+":"+str(underlying)+'.HK'
		symbols = iredis.zrange(key,0, top - 1)
		if len(symbols) >  0:
			for symbol in symbols:
				key2 = "trade:"+str(type)+":"+str(underlying)+'.HK'
				iredis2.zadd(key2, symbol, 1)	


def get_trade_list(underlying, type,top = 5):
	key = "trade:"+str(type)+":"+str(underlying)+'.HK'
	symbols = iredis.zrange(key,0, top - 1)
	print symbols					


underlying = '00700'
#load_warrant_to_redis('00700')

#update_follow_list(underlying, 20)
update_trade_list(underlying, 5)
#get_trade_list(underlying, 'put', 2)

	