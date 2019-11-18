import time
from threading import Lock, Thread

import numpy

from constants import tick_time
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
#from auctioneer import Statistics
import random

class Seller(object):

    def __init__(self, name, product_dict, wallet, statistics, email = 'zhuxiangqi314@gmail.com'):
        self.name = name
        self.product_storage = product_dict
        self.product_list = [product for product in product_dict]
#        self.product = product_list
        self.wallet = wallet
        self.email = email
        self.statistics = statistics

        # register the seller in market
        Market.register_seller(self, self.product_list)
        

        # metrics tracker
        """all original variables have to be altered to dict
        key: product
        value: original list/int"""
        self.price_history = dict()
        self.sales_history = dict()
        self.revenue_history = dict()
        self.profit_history = dict()
        self.expense_history = dict()
        self.sentiment_history = dict()
        self.item_sold = dict()
        
        for product in self.product_list:
            self.sales_history[product] = list()
            self.revenue_history[product] = list()
            self.profit_history[product] = list()
            self.expense_history[product] = [0]
            self.sentiment_history[product] = list()
            self.item_sold[product] = 0
            self.price_history[product] = [product.price + self.CEO_price(product)]
            product.add_seller(self)
            statistics.register_data(obj_data = [product, self], register_type = 'seller')

        # Flag for thread
        self.STOP = False

        self.lock = Lock()

        # start this seller in separate thread
        self.thread = Thread(name=name, target=self.loop)
        self.thread.start()

    def loop(self):
        while not self.STOP:
            self.tick()
            time.sleep(tick_time)

    # if an item is sold, add it to the database
    def sold(self, product):
        self.lock.acquire()
        self.item_sold[product] += 1
        self.lock.release()

    # one timestep in the simulation world
    def tick(self):

        """ in each tick, each product will be considered iteratively 
        while in CEO decsion function, all products will be considered in each decsion"""
        for product in self.product_list:
            self.lock.acquire()

            # append the sales record to the history
            self.sales_history[product].append(self.item_sold[product])
    
            # reset the sales counter
            self.item_sold[product] = 0
    

    
            # Calculate the metrics for previous tick and add to tracker
            self.revenue_history[product].append(self.sales_history[product][-1] * self.price_history[product][-1])
            self.profit_history[product].append(self.revenue_history[product][-1] - self.expense_history[product][-1])
            self.sentiment_history[product].append(self.user_sentiment(product))
            self.price_history[product].append(self.price_history[product][-1] + self.CEO_price(product))
    
            # add the profit to seller's wallet
            self.wallet += self.my_profit(product, True)
            self.lock.release()

    
            # choose what to do for next timestep
            advert_type, scale = self.CEO_advertisement(product)
    
            # ANSWER a. print data to show progress
            print('\nProduct in previous quarter: ' + product.name)
            print('Revenue in previous quarter:', self.my_revenue(product, True))
            print('Expenses in previous quarter:', self.my_expenses(product, True))
            print('Profit in previous quarter:', self.my_profit(product, True))
            print('\nStrategy for next quarter \nAdvert Type: {}, scale: {}\n\n'.format(advert_type, scale))
    
            # perform the actions and view the expense
            self.expense_history[product].append(GoogleAds.post_advertisement(self, product, advert_type, scale))



    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_revenue(self, product, latest_only=False):
        revenue = self.revenue_history[product][-1] if latest_only else numpy.sum(self.revenue_history[product])
        return revenue

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_expenses(self, product, latest_only=False):
        bill = self.expense_history[product][-1] if latest_only else numpy.sum(self.expense_history[product])
        return bill

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_profit(self, product, latest_only=False):
        profit = self.profit_history[product][-1] if latest_only else numpy.sum(self.profit_history[product])
        return profit

    # calculates the user sentiment from tweets.
    def user_sentiment(self, product):
        tweets = numpy.asarray(Twitter.get_latest_tweets(product, 100))
        return 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()

    # to stop the seller thread
    def kill(self):
        self.STOP = True
        self.thread.join()

    def __str__(self):
        return self.name
    
    """function1 price decision
    return price addition (can be negative)"""
    def CEO_price(self, product):
        data_cheating = False
        if random.random() > 0.7:
            self.statistics.send_data(self)
            data_cheating = True
        if data_cheating:
            add_price = 0
        add_price = 0
        return add_price

    """ Cognition system that make decisions about advertisement."""
    def CEO_advertisement(self, product):
        # WRITE YOUR INTELLIGENT CODE HERE
        # You can use following functions to make decision
        #   my_revenue
        #   my_expenses
        #   my_profit
        #   user_sentiment
        #
        # You need to return the type of advert you want to publish and at what scale
        # GoogleAds.advert_price[advert_type] gives you the rate of an advert

        advert_type = GoogleAds.ADVERT_BASIC if GoogleAds.user_coverage(product) < 0.5 else GoogleAds.ADVERT_TARGETED
        scale = self.wallet // GoogleAds.advert_price[advert_type] // 2 #not spending everything
        return advert_type, scale
