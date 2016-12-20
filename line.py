#!/usr/bin/python  
# -*- coding:utf-8 -*- 

'''
python2.7.12
pip
numpy
pypareing 
dateutil 
pandas 
matplotlib
scipy
'''

import numpy as np
import pandas as pd
import string
import matplotlib.pyplot as plt
import json


def draw_line(b, s):
	l=len(b)
	x=range(l)
	plt.plot(x,b)
	plt.plot(x,s)
	plt.show()

def load_data(file):
	f = open(file, "r")  
	b = []
	s = []
	tmp = 0
	while True:
	    line = f.readline()
	    if line: 
	        rows = json.loads(line)
	        if rows[0]['BuyPrice'] != tmp:# and rows[0]['SellPrice'] < 0.111:  
	        	tmp = rows[0]['BuyPrice']
	        	#print tmp
	        	if rows[0]['SellPrice'] != 0:	#异常报价 0.发行商不挂单[关键点] 1.调低买一，不挂卖单 2.调低买一，调高卖一 3.挂单边单 【另外】尽量选择order > 1，选择有人工挂单的
	        		b.append(rows[0]['BuyPrice'])
	        		s.append(rows[0]['SellPrice'])
		        if abs(rows[0]['SellPrice'] - rows[0]['BuyPrice']) > 0.01:
		        	print rows[0]
	    else:  
	        break
	f.close()
	b = tuple(b)
	draw_line(b, s)


#load_data("data/00700.txt")
load_data("data/66259.txt")

