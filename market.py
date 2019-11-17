from threading import Lock

from google_ads import GoogleAds


class Market(object):
    
    catalogue = {}
    lock = Lock()
    correlation_map = dict()

    # initialise the seller catalogue
    @staticmethod
    def register_seller(seller, product_list):
        Market.lock.acquire()
        for product in product_list:
            if product not in Market.catalogue:
                Market.catalogue[product] = list()
            Market.catalogue[product].append(seller)
            
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
        # get the seller for product from catalogue
        seller_list = Market.catalogue[product]

        # call seller's sold function
        if len(seller_list) == 1:
            seller = seller_list[0]
            seller.sold(product)
    
            # deduct price from user's balance
            buyer.deduct(seller.price_history[product][-1])
    
            # track user
            GoogleAds.track_user_purchase(buyer, product)
