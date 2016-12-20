#!/usr/bin/python  
# -*- coding:utf-8 -*- 

import time
import threading


class Timer(threading.Thread):

    def __init__(self, seconds):
        self.runTime = seconds
        threading.Thread.__init__(self)
    def run(self):
        time.sleep(self.runTime)


class CountDownTimer(Timer):

    def run(self):
        counter = self.runTime
        for sec in range(self.runTime):
            time.sleep(1)
            counter -= 1
            
class CountDownExec(CountDownTimer):

    def __init__(self, seconds, action, args=[]):
        self.args = args
        self.action = action
        CountDownTimer.__init__(self, seconds)
    def run(self):
        CountDownTimer.run(self)
        self.action(self.args)