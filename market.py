from threading import Lock

from google_ads import GoogleAds
import random

class Market(object):
    
    catalogue = {}
    lock = Lock()
    correlation_map = dict()

    # initialise the seller catalogue
    @staticmethod
    def register_seller(seller, product_storage):
        Market.lock.acquire()
        for product in product_storage:
            if product not in Market.catalogue:
                Market.catalogue[product] = dict()
            Market.catalogue[product][seller] =  product_storage[product]
            
        Market.lock.release()
        
    """function 1 register correlation map
        used in product.py
        generete correlation_map iteratively"""
    @staticmethod
    def register_correlation_matrix(product):
        Market.lock.acquire()
        key1 = product.product_id
        for key in product.prob_map:
            for tup in product.prob_map[key]:
                key2 = tup[0]
                value = tup[1]
                Market.correlation_map[(key1, key2)] = value
                
        Market.lock.release()

    # when a user buys a product, increment the seller's sales
    @staticmethod
    def buy(buyer, product):
        Market.lock.acquire()
        # get the seller for product from catalogue
        storage_dict = Market.catalogue[product]
        seller_list = [seller for seller in storage_dict if storage_dict[seller] > 0]

        # call seller's sold function
        if len(seller_list) > 0:
            seller_index = int(len(seller_list)* random.random())
            seller = seller_list[seller_index]
            seller.sold(product)
            Market.catalogue[product][seller] -= 1
            # deduct price from user's balance
            buyer.deduct(seller.price_history[product][-1])

                # track user
            GoogleAds.track_user_purchase(buyer, product)
            Market.lock.release()
            return seller
        else:
            Market.lock.release()
            return 0
