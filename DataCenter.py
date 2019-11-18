# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:36:57 2019

@author: Xiangqi
"""
import pandas as pd
from threading import Thread, Lock
import time
from constants import tick_time
import matplotlib.pyplot as plt


"""not sure if this is right but I really want to alter this class to a dynamic thread"""
class Statistics(object):
    def __init__(self, name = 'xianyu'):
        self.lock = Lock()
        self.STOP = False
        self.name = name
        """1. price_series: record price for each product seller in each tick
        name = [format('product-seller')]
        cols = price/tick"""
        self.price_series = pd.DataFrame()
        
        """2. sold_series: record sold product seller each tick
        list of lists [format('product-seller')]"""
        self.sold_series = list()
        
        """3. customer_history: record customer purchasing record
        key: customer_name
        value: list of tuples: (purchased format('product-seller'), wallet)"""
        self.customer_history = dict()
        self.thread = Thread(name = self.name, target=self.loop)
        self.thread.start()
    
    
    """loop function for displaying video"""
    def loop(self):
        # plt.figure(figsize=(6, 9))
        # plt.ion()
        # plt.subplots_adjust(hspace=0.5)
        """ draw 2/3 pictures:
            1. """
        
        while not self.STOP:
            self.tick()
            time.sleep(tick_time)
            
    """tick function for showing figures in each tick"""
    def tick(self):
        self.lock.acquire()
#        for key in self.customer_history:
#            plt.plot(self.customer_history[key], label = key)
#        plt.show()
        self.lock.release()
    
    """function1 register_data (void)
    initialize names and keys of statistics data"""
#    @staticmethod
    def register_data(self, obj_data, register_type):
        self.lock.acquire()
        if register_type == 'seller':
            key = str(obj_data[0].product_id) +'-'+ obj_data[1].name
            # initialize price_series and sold_series
        if register_type == 'customer':
            key = obj_data.name
            self.customer_history[key] = list()
            # customer_history keys
        self.lock.release()
    
    """function2 data_ranking (void)
    record data in each tick in statistics"""
#    @staticmethod
    def data_ranking(self, obj_data, data_type):
        #obj_data = list((customer),product,seller)
        self.lock.acquire()
        if data_type == 'seller':
            # update price_series and sold_series
            key = str(obj_data[0].product_id) +'-'+ obj_data[1].name   
        if data_type == 'customer':
            key = obj_data[0].name
            tup = (str(obj_data[1].product_id) +'-'+ obj_data[2].name, obj_data[0].wallet)
            self.customer_history[key].append(tup)
        self.lock.release()
        
    """function3 send_data (void)
    1. record data in google sheet
    2. send data in gmail"""
#    @staticmethod
    def send_data(self, seller):
        self.lock.acquire()
        # record all data to google sheet
        # generate an email including all data and send it.
        self.lock.release()
        
    """statictics has to be dead"""
    def kill(self):
        self.STOP = True
        self.thread.join(timeout=0)