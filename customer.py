import random
import time
from threading import Thread, Lock

import numpy

from constants import tick_time, seed
from google_ads import GoogleAds
from market import Market
from twitter import Twitter

from DataCenter import DataCenter

random.seed(seed)


class Customer(object):
    def __init__(self, name, customer_id, wallet, dataCenter, crisp_sets=(0.3, 0.7), price_tolerance=0.5,
                 quality_tolerance=0.5):
        """

        :type dataCenter: DataCenter
        """
        self.name, self.customer_id, self.wallet = name, customer_id, wallet
        self.price_tolerance, self.quality_tolerance = price_tolerance, quality_tolerance
        self.dataCenter = dataCenter

        # initialize crisp sets for fuzzy logic
        self.crisp_sets = crisp_sets
        # Register the user with google ads
        GoogleAds.register_user(self)
        self.dataCenter.register_data(self, register_type='customer')

        # ad space stores all the adverts consumed by this user
        self.ad_space = set()
        # stores all the bought products
        self.owned_products = set()

        # flag to stop thread
        self.STOP = False

        # regulate synchronisation
        self.lock = Lock()

        # start this user in separate thread
        self.thread = Thread(name=name, target=self.loop)
        self.thread.start()

    # View the advert to this consumer. The advert is appended to the ad_space
    def view_advert(self, product):
        self.lock.acquire()
        self.ad_space.add(product)
        self.lock.release()

    # Consumer decided to buy a 'product'.
    """function 1 : performance_ratio (float in [0,1])
        use fuzzy logic to calculate the performance ratio of a product for this consumer
        based on tolerance degree and product information"""

    def performance_ratio(self, product):
        # ratio to be finished
        tweets = numpy.asarray(Twitter.get_latest_tweets(product, 100))
        user_sentiment = 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()
        correlation = list()
        if len(self.owned_products) > 0:
            for prod in self.owned_products:
                try:
                    correlation.append(Market.correlation_map[(prod.product_id, product.product_id)])
                except KeyError:
                    correlation.append(0.5)
        if len(correlation) > 0:
            cm = sum(correlation)/len(correlation)
        else:
            cm = 1
        if self.wallet < 200:
            self.price_tolerance = 0.3
        else:
            self.price_tolerance = 0.7
        ratio = cm * ((self.quality_tolerance * self.price_tolerance + user_sentiment) / 2)

        # print('\nratio: ', ratio)

        return ratio

    """function 2 : purchase_decision (bool)
        use tolerance degree and product value to decide whether to buy product"""

    def purchase_decision(self, product):

        ratio = self.performance_ratio(product)
        if 0 < ratio < self.crisp_sets[0]:
            if random.random() < 0.01:
                return True
        if self.crisp_sets[0] < ratio < self.crisp_sets[1]:
            if random.random() < 0.05:
                return True
        if self.crisp_sets[1] < ratio:
            if random.random() < 0.15:
                return True
        else:
            return False

    def consider(self, product):
        # if not enough money in wallet, don't proceed
        if self.wallet < product.price:
            print('Out of money ' + self.name)
            return

        decision = self.purchase_decision(product)
        if not decision:
            return
            # purchase the product from market

        seller = Market.buy(self, product)
        if seller != 0:
            self.dataCenter.data_ranking(obj_data=[self, product, seller], data_type='customer')
            self.owned_products.add(product)


        # add product to the owned products list

    # money is deducted from user's wallet when purchase is completed
    def deduct(self, money):
        self.wallet -= money

    # User expresses his sentiment about the product on twitter
    def tweet(self, product, sentiment):
        Twitter.post(self, product, sentiment)

    # Loop function to keep the simulation going
    def loop(self):
        while not self.STOP:
            self.tick()
            time.sleep(tick_time)

    # one timestep in the simulation world
    def tick(self):


        # user looks at all the adverts in his ad_space
        for product in self.ad_space:
            self.lock.acquire()
            self.consider(product)
            self.lock.release()

        self.lock.acquire()
        # remove the adverts from ad_space
        self.ad_space = set()

        # with some chance, the user may tweet about the product
        if random.random() < 0.5 and len(self.owned_products) > 0:
            # he may choose any random product
            product = random.choice(list(self.owned_products))

            # sentiment in positive if the quality is higher than the tolerance
            sentiment = 'POSITIVE' if self.quality_tolerance < product.quality else 'NEGATIVE'

            # tweet sent
            self.tweet(product, sentiment)

        self.lock.release()

    # set the flag to True and wait for thread to join
    def kill(self):
        self.STOP = True
        self.thread.join(timeout=0)

    def __str__(self):
        return self.name
