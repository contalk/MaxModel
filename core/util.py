#!/usr/bin/python  
# -*- coding:utf-8 -*- 

def get_tick_size(self, price, Market='HK'):
	if  price <= 0.25:
		return 0.001 # 价格[0.05, 0.25] 每单位幅度变化 0.4% - 2%
	if price > 0.25 and price <= 0.5:
		return 0.005 # 2% - 1% 尽量不选该区间
	if price > 0.5 and price <= 10:
		return 0.01	# 2% - 0.1%
	if price > 10 and price <= 20:
		return 0.02 # 2% - 0.1%
	if price > 20 and price <= 100:
		return 0.05 # 0.25% - 0.05%
	if price > 100 and price <= 200:
		return 0.1 # 0.1% - 0.05%
	if price > 200 and price <= 500:
		return 0.2 # 0.1% - 0.04%
	if price > 500 and price <= 1000:
		return 0.5 # 0.1% - 0.05%
	if price >= 1000 and price <= 2000:
		return 1
	if price > 2000:
		return 2	

def file(file, line):
	f = open(file, 'a')
	f.write(line)
	f.close()	
	
def log(self, k, v = ''):
	arr = time.localtime(doge.ts)
	ts =  time.strftime("%Y-%m-%d %H:%M:%S", arr)
	ymd = time.strftime("%Y%m%d", arr)
	file = 'log/'+self.g_market+'_'+str(self.g_stock)+'_'+str(ymd)
	log = str(doge.ts) + '|' + str(k) + '|' + str(v) + '\n'
	f = open(file, 'a')
	f.write(log)
	f.close()
	print log	

def check_trade_time():
	arr = time.localtime(self.ts)
	if self.s.g_market.upper() == 'HK':
		hm = int(time.strftime("%H%M", arr))
		if (hm >= 930 and hm <=1200) or (hm >= 1300 and hm <= 1600):
		 	ts_start = int(time.mktime(time.strptime(self.s.g_start_time, "%Y-%m-%d %H:%M:%S")))
			ts_end  = int(time.mktime(time.strptime(self.s.g_end_time, "%Y-%m-%d %H:%M:%S")))
			print self.ts,ts_end
			if self.ts >= ts_start and self.ts <= ts_end:
				return 1
	return 0	