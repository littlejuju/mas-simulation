from threading import Lock


class Auctioneer(object):
    lock = Lock()
    storage_dict = dict()
    auctioneer_dict = dict()

    @staticmethod
    def bid_buy(buyer, product, storage, seller_list, price):
        Auctioneer.lock.acquire()
        deal = False
        seller = None
        bidder = None
        Auctioneer.storage_dict[product] = storage
        price = buyer.bid(product, price)
        if product not in Auctioneer.auctioneer_dict:
            Auctioneer.auctioneer_dict[product] = [(buyer, price)]
        elif len(Auctioneer.auctioneer_dict[product]) < 3:
            tup = (buyer, price)
            Auctioneer.auctioneer_dict[product].append(tup)
        if len(Auctioneer.auctioneer_dict[product]) == 3:
            """ if there are more than 3 customer bidding price, 
            customer with the highest bid price get the product, 
            seller with the min price will sell the product"""
            buyer_list = [tup[1] for tup in Auctioneer.auctioneer_dict[product]]
            price_list = [tup[1] for tup in Auctioneer.auctioneer_dict[product]]
            price = max(price_list)
            bidder = buyer_list[price_list.index(price)]
            # seller_index = min([seller.price_history[product][-1] for seller in seller_list])
            seller_index = 0
            min_price = seller_list[0].price_history[product][-1]
            for seller in seller_list:
                index = 0
                if seller.price_history[product][-1] < min_price:
                    seller_index = index
                index += 1
            seller = seller_list[seller_index]
            # change price in seller
            seller.price_history[product][-1] = price
            seller.sold(product)
            # deduct price from user's balance
            bidder.deduct(seller.price_history[product][-1])
            print('Auctioneer Deal: ' + seller.name + ' ' + bidder.name + ' ' + str(price))
            deal = True


        Auctioneer.lock.release()
        return deal, seller, bidder
