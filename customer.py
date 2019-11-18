import random
import time
from threading import Thread, Lock

import numpy

from constants import tick_time, seed
from google_ads import GoogleAds
from market import Market
from twitter import Twitter
#from auctioneer import Statistics

random.seed(seed)


class Customer(object):
    def __init__(self, name, wallet, statistics, price_tolerance = 0.5, quality_tolerance = 0.5):
        self.name, self.wallet  = name, wallet
        self.price_tolerance, self.quality_tolerance = price_tolerance, quality_tolerance
        self.statistics = statistics

        # Register the user with google ads
        GoogleAds.register_user(self)
        self.statistics.register_data(self, register_type = 'customer')

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
        ratio = (self.quality_tolerance / self.price_tolerance + user_sentiment) / 2
        
        return ratio
        
    """function 2 : purchase_decision (bool)
        use tolerance degree and product value to decide whether to buy product"""
            
    def purchase_decision(self, product):
        
        decision = False
        ratio = self.performance_ratio(product)
        tweets = numpy.asarray(Twitter.get_latest_tweets(product, 100))
        user_sentiment = 1 if len(tweets) == 0 else (tweets == 'POSITIVE').mean()
        if user_sentiment >= ratio and ((product not in self.owned_products and random.random() < 0.1) or (product in self.owned_products and random.random() < 0.01)):
            decision = True     
        if self.wallet < product.price:
            decision = False
        elif ratio < 0.8:
            decision = False

        return decision
    
    def consider(self, product):
        # if not enough money in wallet, don't proceed
#        if self.wallet < product.price:
#            return
        
        decision = self.purchase_decision(product)
        if decision == False:
            return

            # purchase the product from market
        Market.buy(self, product)
        
                # add product to the owned products list
        self.owned_products.add(product)

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
        self.lock.acquire()

        # user looks at all the adverts in his ad_space
        for product in self.ad_space:
            self.consider(product)

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
