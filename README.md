# MAS Documentation
## 1. customer.py
### 1.1 Parameters
* *name* (str): consumer id
* *wallet* (float): consumer possession
* *❌tolerance*
* ***price_tolerance*** (float [0,1]): higher -> consumer tends to buy higher-price products
* ***quality_tolerance*** (float [0,1]): higher -> consumer tends to buy higher-quality products

### 1.2 Functions
* ***performance_ratio(self, product)*** (float in [0,1])
      use fuzzy logic to calculate the performance ratio of a product for this consumer
      based on tolerance degree and product information
* ***purchase_decision(self, product)*** (bool)
      use tolerance degree and product value to decide whether to buy product

## 2. product.py
### 2.1 Parameters
* *name* (str): product name
* *price* (float): product original price (can be different from price in sellers)
* *quality* (float [0,1]): product quality
* ***product_id*** (int): product id
* ***category*** (str): product category
* ***prob_map*** (dict):
      key: product_name
      value: (product_id, correlation) where correlation is the probability of consumer also buy key product when purchasing self product
* ***seller*** (list): list of sellers who sell this product

### 2.2 Functions
* ***add_seller(seller)*** (void)
      add product seller to seller list

## 3. seller.py
### 3.1 Parameters
* *name* (str): seller name
* *❌product*
* ***product_list*** (list): list of products this seller sells
* ***product_storage*** (dict): record of product storage
* ***email*** (str): email account of this seller (for receiving cheating data sheet)
* ***sales_history & profit_history & expense_history & sentiment_history & item_sold*** (dict):
      all original variables have to be altered to dict
      key: product
      value: original list/int
* ***price_history*** (dict)
      record sellers price decision for each product in each tick
      key: product
      value: price at this tick


### 3.2 Functions
      in each tick, each product will be considered iteratively
      while in CEO decsion function, all products will be considered in each decsion
* ***sold & my_revenue & my_expenses & my_profit & user_sentiment***: add parameter *product*
* *❌CEO()*: original CEO function only used for advertisement decision. And it has to be located in product loop. So it has been altered to *CEO_advertisement(product)*
* ***CEO_advertisement(product)***: Cognition system that make decisions about advertisement.
* ***CEO_price(product)***:
      1. decide whether to buy cheating data from autioneer
      2. analyze data to decide add_price (can be negative)
      3. history return price addition

## 4. market.py
### 4.1 Variables
* ***catalogue***(dict):
      dict of product and sellers
      key: product
      value: seller list
* ***correlation_map(product)*** (dict):
      dict of correlation between products
      key: (product_id1, product_id2)
      value: the probability of consumer also buy key product2 when purchasing product1 P(buy_p2|buy_p1)

### 4.2 Functions
* ***register_correlation_matrix(product)*** (void)
      used in product.py
      generete correlation_map iteratively

## 5. ***auctioneer.py***
### 5.1 Variables
* ***price_series*** (pd.DataFrame)
      record price for each product seller in each tick
      name = [format('product-seller')]
      cols = price/tick
* ***sold_series*** (list)
      record sold product seller each tick
      list of lists [format('product-seller')]
* ***customer_history*** (dict)
      record customer purchasing record
      key: customer_name
      value: list of tuples: (purchased format('product-seller'), price)

### 5.2 Functions
* ***register_data(obj_data, register_type)*** (void)
      initialize names and keys of statistics data
* ***data_ranking(obj_data, data_type)*** (void)
      record data in each tick in statistics
* ***send_data(seller)*** (void)
      1. record data in google sheet
      2. send data in gmail