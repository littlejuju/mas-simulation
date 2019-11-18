import random
import time

from constants import seed
from customer import Customer
from product import Product
from seller import Seller
from utils import plot
from DataCenter import Statistics

random.seed(seed)

# create auctioneer 'xianyu'
xianyu = Statistics('xianyu')
# Create some Consumers
customers = [Customer(name='consumer_' + str(i), wallet=500, statistics = xianyu, price_tolerance=0.5 + 0.4 * random.random()) for i in range(500)]

# Create a product
iphone = Product(name='iphone', product_id = 0, price=300, quality=0.9, prob_map = {'galaxy':[(1,0.1)]})
galaxy = Product(name='galaxy', product_id = 1, price=200, quality=0.8, prob_map = {'iphone':[(0,0.2)]})

# Create a Seller with some budget
seller_apple = Seller(name='apple', product_dict={iphone:100}, wallet=1000, statistics = xianyu, email = 'a0195470yreceiver@gmail.com')
seller_samsung = Seller(name='samsung', product_dict={galaxy:110}, wallet=500, statistics = xianyu, email = 'a0159419u.receiver@gmail.com')

# Wait till the simulation ends
try:
    time.sleep(10)
except KeyboardInterrupt:
    pass

# kill seller thread
seller_apple.kill()
seller_samsung.kill()

# Plot the sales and expenditure trends
plot(seller_apple)
plot(seller_samsung)

for product in seller_apple.product_list:
    print('Total Profit Apple ' + product.name +': ', seller_apple.my_profit(product))
for product in seller_samsung.product_list:
    print('Total Profit Samsung ' + product.name +': ', seller_samsung.my_profit(product))

# Kill consumer threads
for consumer in customers:
    consumer.kill()

xianyu.kill()

#from market import Market
#correlation_map = Market.correlation_map