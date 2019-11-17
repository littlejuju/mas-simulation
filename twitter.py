from collections import defaultdict


class Twitter(object):
    # dictionary to store tweets
    feed = defaultdict(list)

    # Called by the user to tweet something
    @staticmethod
    def post(user, product, tweet):
        Twitter.feed[product].append((user, tweet))

    # returns the latest tweet about a product.
    @staticmethod
    def get_latest_tweets(product, n):
        return [tweet for user, tweet in Twitter.feed[product][-n:]]
