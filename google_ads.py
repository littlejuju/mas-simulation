import random
from collections import defaultdict
from threading import Lock

from constants import seed

random.seed(seed)


class GoogleAds(object):
    # Define the types of adverts available
    ADVERT_BASIC = 'BASIC'
    ADVERT_TARGETED = 'TARGETED'

    # Define advert's price
    advert_price = {
        ADVERT_BASIC: 5,
        ADVERT_TARGETED: 10
    }

    # Google's internal database
    users = []
    expenses = defaultdict(list)
    purchase_history = defaultdict(list)

    lock = Lock()

    # post an advert about the product
    @staticmethod
    def post_advertisement(seller, product, advert_type, scale):
        # scale of adverts should not be more than number of users
        scale = min(scale, len(GoogleAds.users))
        GoogleAds.lock.acquire()

        # if advert_type is basic, choose any set of customers
        if advert_type == GoogleAds.ADVERT_BASIC:
            users = random.choices(GoogleAds.users, k=scale)

        # if advert_type is targeted, choose user's who were not shown the same advert in previous tick
        elif advert_type == GoogleAds.ADVERT_TARGETED:
            new_users = list(set(GoogleAds.users) - set(GoogleAds.purchase_history[product]))
            users = random.choices(new_users, k=scale)

        else:
            print('Not a valid Advert type')
            return

        # publish the advert to selected user
        scale = len(users)
        for user in users:
            user.view_advert(product)

        # update the bill into seller's account
        bill = scale * GoogleAds.advert_price[advert_type]
        GoogleAds.expenses[seller].append(bill)

        GoogleAds.lock.release()

        # return the bill amount to the seller
        return bill

    @staticmethod
    def register_user(user):
        GoogleAds.lock.acquire()
        GoogleAds.users.append(user)
        GoogleAds.lock.release()

    @staticmethod
    def track_user_purchase(user, product):
        GoogleAds.lock.acquire()
        GoogleAds.purchase_history[product].append(user)
        GoogleAds.lock.release()

    @staticmethod
    def user_coverage(product):
        return len(set(GoogleAds.purchase_history[product])) / len(GoogleAds.users)
