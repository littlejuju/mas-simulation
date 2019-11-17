# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:36:57 2019

@author: Xiangqi
"""
import pandas as pd
from threading import Lock

class Statistics(object):
    lock = Lock()
    
    """1. price_series: record price for each product seller in each tick
    name = [format('product-seller')]
    cols = price/tick"""
    price_series = pd.DataFrame()
    
    """2. sold_series: record sold product seller each tick
    list of lists [format('product-seller')]"""
    sold_series = list()
    
    """3. customer_history: record customer purchasing record
    key: customer_name
    value: list of tuples: (purchased format('product-seller'), price)"""
    customer_history = dict()
    
    
    """function1 register_data (void)
    initialize names and keys of statistics data"""
    @staticmethod
    def register_data(obj_data, register_type):
        Statistics.lock.acquire()
        if register_type == 'seller':
            key = str(obj_data[0].product_id) +'-'+ obj_data[1].name
            # initialize price_series and sold_series
        if register_type == 'customer':
            key = obj_data.name
            Statistics.customer_history[key] = list()
            # customer_history keys
        Statistics.lock.release()
    
    """function2 data_ranking (void)
    record data in each tick in statistics"""
    @staticmethod
    def data_ranking(obj_data, data_type):
        #obj_data = list((customer),product,seller)
        Statistics.lock.acquire()
        if data_type == 'seller':
            # update price_series and sold_series
            key = str(obj_data[0].product_id) +'-'+ obj_data[1].name   
        if data_type == 'customer':
            key = obj_data[0].name
            tup = (str(obj_data[1].product_id) +'-'+ obj_data[2].name, obj_data[2].price_history[-1])
            Statistics.customer_history[key].append(tup)
        Statistics.lock.release()
        
    """function3 send_data (void)
    1. record data in google sheet
    2. send data in gmail"""
    @staticmethod
    def send_data(seller):
        Statistics.lock.acquire()
        # record all data to google sheet
        # generate an email including all data and send it.
        Statistics.lock.release()