from market import Market
class Product(object):
    def __init__(self, name, product_id, price, quality, category = 'electronic', prob_map = dict()):
        assert quality <= 1

        self.name = name
        self.product_id = product_id
        self.price = price
        self.quality = quality
        self.category = category
        self.prob_map = prob_map
        self.seller = list()
        Market.register_correlation_matrix(self)
    """function1: add_seller
        add product seller to seller list"""    
    def add_seller(self, seller):
        self.seller.append(seller)
        
