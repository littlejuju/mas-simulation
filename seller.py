import time
from threading import Lock, Thread

import numpy

from constants import tick_time
from constants import ad_budget_ration
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
# from auctioneer import DataCenter
import random
import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures


class Seller(object):

    def __init__(self, name, product_dict, wallet, dataCenter, email='zhuxiangqi314@gmail.com'):
        self.count = 0
        self.name = name
        self.product_storage = product_dict
        self.product_list = [product for product in product_dict]
        #        self.product = product_list
        self.wallet = wallet
        self.email = email
        self.dataCenter = dataCenter
        dataframe_index_1 = list()
        dataframe_index_2 = list()
        self.customer_record = dict()

        # register the seller in market
        Market.register_seller(self, self.product_storage)

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
            dataframe_index_1.extend([product.name, product.name])
            dataframe_index_2.extend(['price', 'revenue'])
            self.sales_history[product] = list()
            self.revenue_history[product] = list()
            self.profit_history[product] = list()
            self.expense_history[product] = [0]
            self.sentiment_history[product] = list()
            self.item_sold[product] = 0
            self.price_history[product] = [product.price]
            product.add_seller(self)
            self.dataCenter.register_data(obj_data=[product, self], register_type='seller')
            print(self.dataCenter.price_series)
        self.CEO_price_training = pd.DataFrame(columns=[dataframe_index_1, dataframe_index_2])
        self.CEO_price_validation = pd.DataFrame(columns=[dataframe_index_1, dataframe_index_2])

        # Flag for thread
        self.STOP = False

        self.lock = Lock()

        # start this seller in separate thread
        self.thread = Thread(name=name, target=self.loop)
        self.thread.start()

    def loop(self):

        while not self.STOP:
            self.tick()
            self.count += 1
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
        self.dataCenter.seller_info_update(self.count)
        for product in self.product_list:
            self.lock.acquire()

            # append the sales record to the history
            self.dataCenter.data_ranking(obj_data=[product, self], data_type='seller')
            self.sales_history[product].append(self.item_sold[product])
            self.product_storage[product] -= self.item_sold[product]

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

            # avoid bankrupt
            if self.count > 1 & self.my_revenue(product, True) > 0:
                budget = ad_budget_ration * self.my_revenue(product, True)
            else:
                budget = 0
                # perform the actions and view the expense
            self.expense_history[product].append(GoogleAds.post_advertisement(self, product, advert_type, scale, budget))


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
        """1. record price and revenue into training data set"""
        self.CEO_price_training.loc[self.count, (product.name,'price')] = self.price_history[product][-1]
        self.CEO_price_training.loc[self.count, (product.name,'revenue')] = self.revenue_history[product][-1]
        """2. if count < 30: prepare for training data and return random add_price for trial runs"""
        if self.count < 30:
            add_price = int(10 * (random.random() - 0.5))
            return add_price
        """2. decide whether to buy cheating data sheets"""
        data_cheating = False
        if random.random() > 0.7:
            self.dataCenter.send_data(self)
            data_cheating = True
        """3. if cheating"""
        if data_cheating:
            add_price = 0
            return add_price
        """4. if not cheating"""
        # 4.1 divide training and validation set
        df_training = self.CEO_price_training[product.name].loc[0:self.count-10]
        df_validation = self.CEO_price_training[product.name].loc[self.count-10: self.count+1]



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
        scale = self.wallet // GoogleAds.advert_price[advert_type] // 2  # not spending everything
        return advert_type, scale
