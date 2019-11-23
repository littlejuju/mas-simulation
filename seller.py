import time
from threading import Lock, Thread

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from constants import tick_time
from constants import ad_budget_ration
from constants import relevance_to_recommend
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
# from auctioneer import DataCenter
import random
import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from keras.models import Sequential
# Dense full connect layer
from keras.layers import Dense, Activation
# optimizer: Stochastic gradient descent
from keras.optimizers import SGD



class Seller(object):

    def __init__(self, name, product_dict, wallet, dataCenter, email='zhuxiangqi314@gmail.com', CEO_type = 'poly2'):
        self.count = 0
        self.name = name
        self.CEO_type = CEO_type
        self.product_storage = product_dict
        self.product_list = [product for product in product_dict]
        #        self.product = product_list
        self.wallet = wallet
        self.email = email
        self.dataCenter = dataCenter
        dataframe_index_1 = list()
        dataframe_index_2 = list()
        self.customer_record = dict()
        self.poly2_coef = dict()
        self.data_cheating = False
        self.cheating_package = dict()

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
        self.CEO_price_model = dict()

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
            self.poly2_coef[product] = [0, 0, 0]
            self.CEO_price_model[product] = {'x':[],'y':[]}
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
        """ decide whether to buy cheating data sheets in each tick count > 20 """
        self.data_cheating = False
        if self.count > 20 and random.random() > 0.7:
            self.data_cheating = True
            """obtain cheating data sheet """
            self.dataCenter.send_data(self)
            # the price of a cheating package is related to package size
            self.wallet -= 20*self.count
            self.cheating_package = self.dataCenter.send_data(self)

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
            self.wallet += self.profit_history[product][-1]
            self.sentiment_history[product].append(self.user_sentiment(product))
            self.price_history[product].append(self.price_history[product][-1] + self.CEO_price(product))

            # add the profit to seller's wallet
            self.wallet += self.my_profit(product, True)
            self.lock.release()

            # choose what to do for next timestep

            advert_type, user_list, scale = self.CEO_advertisement(product)

            # ANSWER a. print data to show progress
            print('\nProduct in previous quarter: ' + product.name)
            print('Revenue in previous quarter:', self.my_revenue(product, True))
            print('Expenses in previous quarter:', self.my_expenses(product, True))
            print('Profit in previous quarter:', self.my_profit(product, True))
            print('\nStrategy for next quarter \nAdvert Type: {}, scale: {}\n\n'.format(advert_type, scale))
            print('\n',self.count)

            # avoid bankrupt
            if self.count > 0 and self.revenue_history[product][-1] > 0:
                budget = ad_budget_ration * self.revenue_history[product][-1]
            elif self.count == 0:
                budget = ad_budget_ration * self.wallet / len(self.product_list)
                # perform the actions and view the expense
            else:
                budget = 0
            if self.product_storage[product] > 0:
                self.expense_history[product].append(
                    GoogleAds.post_advertisement(self, product, advert_type, user_list, scale, budget))
            else:
                self.expense_history[product].append(0)
        print(self.name + ' wallet: ' + str(self.wallet))

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_revenue(self, product, latest_only=False):
        revenue = self.revenue_history[product][-1] if latest_only else np.sum(self.revenue_history[product])
        return revenue

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_expenses(self, product, latest_only=False):
        bill = self.expense_history[product][-1] if latest_only else np.sum(self.expense_history[product])
        return bill

    # calculates the total revenue. Gives the revenue in last tick if latest_only = True
    def my_profit(self, product, latest_only=False):
        profit = self.profit_history[product][-1] if latest_only else np.sum(self.profit_history[product])
        return profit

    # calculates the user sentiment from tweets.
    def user_sentiment(self, product):
        tweets = np.asarray(Twitter.get_latest_tweets(product, 100))
        return 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()

    # to stop the seller thread
    def kill(self):
        self.STOP = True
        self.thread.join()

    def __str__(self):
        return self.name

    """function01 customer analysis
    Using customer purchasing history to analyze correlation between product
    if there is product_x 
     if customer purchase it, they have high prob to buy this product and this product sales rank go lower
      then add_price -= 1
     else:
      add_price += 1"""

    def CEO_customer_analysis(self, product, sales_rank, customer_history):
        also_buy = dict()
        key_list = sales_rank.columns.tolist()
        for key in key_list:
            also_buy[key] = 0
        this_product = str(product.product_id) + '-' + self.name
        for key in customer_history:
            if this_product in customer_history[key]:
                for key1 in key_list:
                    if key1 in customer_history[key]:
                        also_buy[key1] += 1
        correlation = 0
        highest_prob = this_product
        for key in also_buy:
            if also_buy[key] > correlation:
                highest_prob = key
                correlation = also_buy[key]
        add_add_price = 0
        if sales_rank[highest_prob].iloc[-1] < sales_rank[highest_prob].iloc[-2]:
            add_add_price += 1
        else:
            add_add_price -= 1

        return add_add_price

    """function02 price comparison
    compare price and sales rank of this product in different sellers
    if product sales rank is the highest, add_add_price = 1
    else: if other seller has higher sales rank and lower price, add_add_price = -1"""
    def CEO_price_comparison(self, product, sales_rank, price_history):
        add_add_price = 0
        seller_list = [str(product.product_id) + '-' + seller.name for seller in product.seller]
        df_sales = sales_rank.loc[:, seller_list]
        df_price = price_history.loc[:, seller_list]
        this_seller_product = str(product.product_id)+'-'+self.name
        rank_list = df_sales.iloc[-1].tolist()
        price_list = df_price.iloc[-1].tolist()
        if df_sales[this_seller_product].iloc[-1] == min(rank_list):
            add_add_price += 1
        elif price_list[rank_list.index(min(rank_list))] == min(price_list):
            add_add_price -= 1
        return add_add_price

    """function1 price decision
    return price addition (can be negative)"""

    def CEO_price(self, product):
        """1. record price and revenue into training data set"""
        self.CEO_price_training.loc[self.count, (product.name, 'price')] = self.price_history[product][-1]
        self.CEO_price_training.loc[self.count, (product.name, 'revenue')] = self.revenue_history[product][-1]
        """2. if count < 30: prepare for training data and return random add_price for trial runs"""
        if self.count < 20:
            add_price = int(10 * (random.random() - 0.5))
            return add_price

        """3. if cheating
           add_add_price will be added on add_price (derive by price optimization)"""
        add_add_price = 0
        if self.data_cheating:
            """ the aim of cheating from data center is to analyze factors of revenue and """
            """3.1 price comparison (if product has more than one seller)"""

            df_sales_rank = self.cheating_package['sold']
            df_product_price = self.cheating_package['price']
            if len(product.seller) > 0:
                add_add_price += self.CEO_price_comparison(product, df_sales_rank, df_product_price)

            """3.2 customer analysis"""
            dict_customer = self.cheating_package['customer']
            add_add_price += self.CEO_customer_analysis(product, df_sales_rank, dict_customer)

            # return add_price
        """4. if not cheating"""
        # 4.1 divide training and validation set
        if self.CEO_type == 'random':
            add_price = int(10 * (random.random() - 0.5))
        elif self.CEO_type == 'poly2':
            df_training = self.CEO_price_training[product.name].loc[0:self.count - 10]
            df_validation = self.CEO_price_training[product.name].loc[self.count - 10: self.count + 1]
            # 4.2 2 degree polynomial regression
            poly_reg = PolynomialFeatures(degree=2)
            X_poly = poly_reg.fit_transform(np.array(df_training['price'].values).reshape(-1, 1))
            lin_reg_2 = linear_model.LinearRegression()
            lin_reg_2.fit(X_poly, np.array(df_training['revenue'].values).reshape(-1, 1))
            coef = lin_reg_2.coef_
            # calculate mse
            score = np.mean((lin_reg_2.predict(X_poly) - np.array(df_training['revenue'].values)) ** 2)
            # calculate R square
            SSR = sum([(f_i - np.mean(np.array(df_training['revenue'].values))) ** 2 for f_i in lin_reg_2.predict(X_poly)])
            SST = sum([(y_i - np.mean(np.array(df_training['revenue'].values))) ** 2 for y_i in df_training['revenue'].values.tolist()])
            R_square = SSR / SST
            #lin_reg_2.score(np.array(df_validation['price'].values), np.array(df_validation['revenue'].values).reshape(-1, 1))
            print('\nRegression Coefficient ' + product.name + ' :' + str(coef))
            print('\nRegression MSE Score ' + product.name + ' :' + str(score))
            print('\nRegression R Square ' + product.name + ' :' + str(R_square))
            if coef[0][2] < 0 and coef[0][1] > 0:
                new_price = -coef[0][1] / (2 * coef[0][2])
                add_price = new_price - self.price_history[product][-1]
                self.poly2_coef[product] = coef[0]
                self.poly2_coef[product][0] = lin_reg_2.intercept_
                price_series = np.array(self.price_history[product][1:])
                price_model = dict()
                axis_x = np.arange(int(min(price_series)),int(max(price_series))+1).reshape([-1,1])
                X_poly2 = poly_reg.fit_transform(axis_x)
                price_model['x'] = axis_x
                price_model['y'] = [y - lin_reg_2.intercept_ for y in list(lin_reg_2.predict(X_poly2))]
                self.CEO_price_model[product] = price_model
            else:
                add_price = 0
        elif 'sgd' in self.CEO_type:
            df_training = self.CEO_price_training[product.name].loc[0:self.count + 1]
            x_data = np.array(df_training['price'].values)
            y_data = np.array(df_training['revenue'].values)
            model = Sequential()
            # activate function: tanh
            if self.CEO_type == 'sgd_tanh':
                model.add(Dense(units=10, input_dim=1))
                model.add(Activation('tanh'))
                model.add(Dense(units=1))
                model.add(Activation('tanh'))
            elif self.CEO_type == 'sgd_relu':
                model.add(Dense(units=10, input_dim=1))
                model.add(Activation('relu'))
                model.add(Dense(units=1))
                model.add(Activation('relu'))
            sgd = SGD(lr=0.3)
            model.compile(optimizer=sgd, loss='mse')
            step_cost = list()
            for step in range(20):
                # one batch each step
                cost = model.train_on_batch(x_data, y_data)
                step_cost.append(cost)
            # weight, b = model.layers[0].get_weights()
            # print('W：', weight, ' b: ', b)
            print(len(model.layers))
            self.CEO_price_model[product] = model
            trial_x = np.linspace(min(x_data),0.1,max(x_data))
            y_pred = list(model.predict(trial_x))
            price_series = np.array(self.price_history[product][1:])
            price_model = dict()
            axis_x = np.arange(int(min(price_series)),int(max(price_series))+1).reshape([-1,1])
            price_model['x'] = axis_x
            price_model['y'] = model.predict(axis_x)
            self.CEO_price_model[product] = price_model
            new_price = trial_x[y_pred.index(max(y_pred))]
            add_price = new_price - self.price_history[product][-1]
        return add_price + add_add_price

    """ Cognition system that make decisions about advertisement."""

    def CEO_advertisement(self, product):
        """
        WRITE YOUR INTELLIGENT CODE HERE
        Recommendation algorithm based on relationship between two products:
        if users bought a product which has strong connection with other product,
        these users will be targeted for the other product.
        """
        most_relevance = 0
        most_relevant_user_list = GoogleAds.purchase_history[product]
        for other_product in self.product_list:
            if product.name != other_product.name:
                if len(GoogleAds.purchase_history[other_product]) > 0:
                    relevance = len(list(set(GoogleAds.purchase_history[product]) & set(
                        GoogleAds.purchase_history[other_product]))) / len(GoogleAds.purchase_history[other_product])
                    if relevance > most_relevance:
                        most_relevance = relevance
                        most_relevant_user_list = GoogleAds.purchase_history[other_product]
        if most_relevance > relevance_to_recommend:
            advert_type = GoogleAds.ADVERT_TARGETED
            scale = len(most_relevant_user_list)
        else:
            advert_type = GoogleAds.ADVERT_BASIC
            scale = self.wallet // GoogleAds.advert_price[advert_type]
        return advert_type, most_relevant_user_list, scale
