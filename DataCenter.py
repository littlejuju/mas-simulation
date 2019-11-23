# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:36:57 2019

@author: Xiangqi
"""
import pandas as pd
import numpy as np
from threading import Thread, Lock
import time
from constants import tick_time, ticks, email_body, sendmail, path
import gspread
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""not sure if this is right but I really want to alter this class to a dynamic thread"""
class DataCenter(object):
    def __init__(self, name = 'xianyu'):
        self.lock = Lock()
        self.STOP = False
        self.name = name
        """1. price_series: record price for each product seller in each tick
        name = [format('product_id-seller')]
        cols = price/tick"""
        self.price_series = pd.DataFrame()
        
        """2. sold_series: record sold product seller each tick
        list of lists [format('product-seller')]"""
        self.sold_series = [list() for i in range(ticks // tick_time + 2)]
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('My First Project-16ced2a4af64.json', scope)

        self.gc = gspread.authorize(credentials)
        self.pygc = pygsheets.authorize(service_file='My First Project-16ced2a4af64.json')
        # self.sh = self.gc.create('A new spreadsheet')
        try:
            self.sh = self.gc.open('DataCenter')
        except gspread.exceptions.SpreadsheetNotFound:
            self.sh = self.gc.create('DataCenter')
        self.worksheet_namelist = ['Price Series', 'Sold Item Statistics', 'Sales Rank', 'Customer Purchase', 'Customer Wallet']
        # self.worksheet_package = dict()
        for sheet_name in self.worksheet_namelist:
            try:
                worksheet = self.sh.worksheet(sheet_name)
                self.sh.del_worksheet(worksheet)
                self.sh.add_worksheet(title=sheet_name, rows="100", cols="20")
            except gspread.exceptions.WorksheetNotFound:
                self.sh.add_worksheet(title=sheet_name, rows="100", cols="20")

        # """3. sold_series_sublist
        # item in sold_series for each tick"""
        # self.sold_series_sublist = list()
        
        """4. customer_history: record customer purchasing record
        key: customer_name
        value: list of tuples: (purchased format('product-seller'), wallet)"""
        self.customer_history = dict()

        """5. sales_rank
        sales rank in each tick"""
        self.sales_rank = pd.DataFrame()
        self.sender_address = 'a0195470yrobot@gmail.com'
        self.sender_pass = 'h+X730630'
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
            time.sleep(tick_time*5)
            
    """tick function for showing figures in each tick"""
    def tick(self):
        self.lock.acquire()
        """ 1. update worksheets in each tick"""
        # price series
        sh = self.pygc.open('DataCenter')
        worksheet0 = sh.worksheet_by_title(self.worksheet_namelist[0])
        worksheet1 = sh.worksheet_by_title(self.worksheet_namelist[1])
        worksheet2 = sh.worksheet_by_title(self.worksheet_namelist[2])
        worksheet3 = sh.worksheet_by_title(self.worksheet_namelist[3])
        worksheet4 = sh.worksheet_by_title(self.worksheet_namelist[4])
        self.lock.release()
        worksheet0.clear()
        worksheet0.set_dataframe(self.price_series, (1, 1))
        # sold series
        worksheet1.clear()
        df_list = list()
        for index in range(len(self.sold_series)):
            key = 'tick ' + str(index + 1)
            df_list.append(pd.DataFrame({key: self.sold_series[index]}))
        worksheet1.set_dataframe(pd.concat(df_list, ignore_index=True, axis=1), (1, 1), copy_head=True)
        # sales rank

        worksheet2.clear()
        worksheet2.set_dataframe(self.sales_rank, (1, 1))
        # customer purchase and wallet
        worksheet3.clear()
        worksheet4.clear()
        df_list3 = list()
        df_list4 = list()
        for key in self.customer_history:
            purchase_list = [tup[0] for tup in self.customer_history[key]]
            wallet_list = [tup[1] for tup in self.customer_history[key]]
            df_list3.append(pd.DataFrame({key: purchase_list}))
            df_list4.append(pd.DataFrame({key: wallet_list}))
        worksheet3.set_dataframe(pd.concat(df_list3, ignore_index=True, axis=1), (1, 1), copy_head=True)
        worksheet4.set_dataframe(pd.concat(df_list4, ignore_index=True, axis=1), (1, 1), copy_head=True)


        #        for key in self.customer_history:
#            plt.plot(self.customer_history[key], label = key)
#        plt.show()

    
    """function1 register_data (void)
    initialize names and keys of statistics data"""
#    @staticmethod
    def register_data(self, obj_data, register_type):
        self.lock.acquire()
        if register_type == 'seller':
            key = str(obj_data[0].product_id) +'-'+ obj_data[1].name
            # initialize price_series
            self.price_series[key] = None
            self.sales_rank[key] = None
            # sold_series do not need initializing
        if register_type == 'customer':
            key = obj_data.name
            self.customer_history[key] = list()
            # customer_history keys
        self.lock.release()
    

#    @staticmethod
    """function2 seller_info_update (void)
    if row number of price_series < count, update a new row in price_series
    """
    def seller_info_update(self, count):
        self.lock.acquire()
        if self.price_series.shape[0] < count:
            self.price_series.loc[count] = None
        self.lock.release()


    """function3 data_ranking (void)
    record data in each tick in statistics"""
    def data_ranking(self, obj_data, data_type):
        #obj_data = list((customer),product,seller)
        self.lock.acquire()
        if data_type == 'seller':
            # update price_series and sold_series
            key = str(obj_data[0].product_id) +'-'+ obj_data[1].name
            self.price_series.loc[obj_data[1].count, key] =  obj_data[1].price_history[obj_data[0]][-1]
            for item in range(obj_data[1].item_sold[obj_data[0]]):
                self.sold_series[obj_data[1].count].append(key)
        if data_type == 'customer':
            key = obj_data[0].name
            tup = (str(obj_data[1].product_id) +'-'+ obj_data[2].name, obj_data[0].wallet)
            self.customer_history[key].append(tup)
        self.lock.release()

    """function5 send_data (void)
    1. record data in google sheet
    2. send data in gmail"""
#    @staticmethod
    def send_data(self, seller):
        """ 1. share spread sheet to seller"""
        if sendmail:
            self.sh.share(seller.email, perm_type='user', role='reader')
        """ 2. send notification email"""
        if sendmail:
            self.send_email(seller)
        self.lock.acquire()

        sales_rank = self.sales_rank
        df_index = 0
        for sales_index in range(len(self.sold_series) - 1):
            sales_list = self.sold_series[sales_index + 1]
            key_list = sales_rank.columns.tolist()
            sales_count = [sales_list.count(key) for key in key_list]
            sales_sorted = np.argsort(np.array(sales_count))
            rank = len(key_list)
            for item in sales_sorted:
                sales_rank.loc[df_index, key_list[item]] = rank
                rank -= 1
            df_index += 1
        self.sales_rank = sales_rank
        cheating_package = dict()
        cheating_package['price'] = self.price_series
        cheating_package['sold'] = self.sales_rank
        cheating_package['customer'] = self.customer_history
        # record all data to google sheet
        # generate an email including all data and send it.
        self.lock.release()
        return cheating_package
        
    """statictics has to be dead"""
    def kill(self):
        self.STOP = True
        self.price_series.to_csv(path + 'price_series.csv')
        df_list = list()
        for index in range(len(self.sold_series)):
            key = 'tick ' + str(index + 1)
            df_list.append(pd.DataFrame({key: self.sold_series[index]}))
        df_sold_series = pd.concat(df_list, ignore_index=True, axis=1)
        df_sold_series.to_csv(path + 'sold_series.csv')
        self.sales_rank.to_csv(path + 'sales_rank.csv')
        df_list3 = list()
        df_list4 = list()
        for key in self.customer_history:
            purchase_list = [tup[0] for tup in self.customer_history[key]]
            wallet_list = [tup[1] for tup in self.customer_history[key]]
            df_list3.append(pd.DataFrame({key: purchase_list}))
            df_list4.append(pd.DataFrame({key: wallet_list}))
        df_customer_purchase = pd.concat(df_list3, ignore_index=True, axis=1)
        df_customer_wallet = pd.concat(df_list4, ignore_index=True, axis=1)
        df_customer_purchase.to_csv(path + 'customer_purchase.csv')
        df_customer_wallet.to_csv(path + 'customer_wallet.csv')
        self.thread.join(timeout=0)


    """ generate email html body"""
    def send_email(self, seller):
        mail_content = email_body.replace('seller.name', seller.name)
        receiver_address = seller.email
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Hi ' + seller.name + '! Here are data sheets you require :)'   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(self.sender_address, self.sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(self.sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')