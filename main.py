import random
import time

from constants import seed
from customer import Customer
from product import Product
from seller import Seller
from utils import plot
from DataCenter import DataCenter
from constants import ticks

random.seed(seed)

# create auctioneer 'dataCenter'
dataCenter = DataCenter('dataCenter')
# Create some Consumers
customers = [Customer(name='consumer_' + str(i), customer_id=i, wallet=7000, dataCenter=dataCenter,
                      crisp_sets=(0.3 + 0.2 * (random.random() - 0.5), 0.7 + 0.2 * (random.random() - 0.5)),
                      price_tolerance=0.5 + 0.4 * random.random(), quality_tolerance=0.5 + 0.4 * random.random()) for i
             in range(700)]

# Create a product
iphone7 = Product(name='iphone7', product_id=0, price=300, quality=0.9, prob_map={'galaxy': [(1, 0.6)]})
galaxy = Product(name='galaxy', product_id=1, price=200, quality=0.7, prob_map={'iphone7': [(0, 0.6)]})
iphone5 = Product(name='iphone5', product_id=2, price=220, quality=0.85,
                  prob_map={'iphone7': [(0, 0.7)], 'galaxy': [(1, 0.8)]})
note = Product(name='note', product_id=3, price=240, quality=0.88,
               prob_map={'iphone7': [(0, 0.7)], 'iphone5': [(2, 0.5)], 'galaxy': [(1, 0.6)]})
#

# Create a Seller with some budget
seller_apple = Seller(name='apple', product_dict={iphone5: 1470, iphone7: 1450}, wallet=1000, dataCenter=dataCenter,
                      email='a0195470yreceiver@gmail.com')
seller_samsung = Seller(name='samsung', product_dict={galaxy: 1510, note: 1200}, wallet=500, dataCenter=dataCenter,
                        email='a0159419u.receiver@gmail.com')

# Wait till the simulation ends
try:
    time.sleep(ticks)
except KeyboardInterrupt:
    pass

# kill seller thread
seller_apple.kill()
seller_samsung.kill()

# Plot the sales and expenditure trends
plot(seller_apple)
plot(seller_samsung)

for product in seller_apple.product_list:
    print('Total Profit Apple ' + product.name + ': ', seller_apple.my_profit(product))
for product in seller_samsung.product_list:
    print('Total Profit Samsung ' + product.name + ': ', seller_samsung.my_profit(product))

# Kill consumer threads
for consumer in customers:
    consumer.kill()

dataCenter.kill()
price_series = dataCenter.price_series
sold_series = dataCenter.sold_series
customer_history = dataCenter.customer_history
print(price_series)
print(sold_series)
print(len(sold_series))
print(customer_history)
print(len(customer_history))
iphone_dict = {'price': seller_samsung.price_history[note], 'sold': seller_samsung.sales_history[note],
               'revenue': seller_samsung.revenue_history[note]}
print(iphone_dict)
# from market import Market
# correlation_map = Market.correlation_map
