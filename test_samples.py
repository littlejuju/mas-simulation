# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:25:05 2019

@author: Xiangqi
"""

test_dict = {'a': 2, 'b': [1, 2]}
print('a' in test_dict)
print('c' in test_dict)

test_tup = {'iphone': [(0, 0.2)]}
for key in test_tup:
    for tup in test_tup[key]:
        print(tup[0])

test_tup = ['a', 1]

import pandas as pd

count = 0
df = pd.DataFrame()
print(df)
df['a'] = None
print(df)
df['b'] = None
print(df)
while count < 10:
    df.loc[count] = 3
    df.loc[count, 'a'] = 1
    count += 1
print(df)

l = [list() for i in range(20)]
print(len(l))

print(int(0.5))
CEO_price_training = pd.DataFrame(
    columns=[['product1', 'product1', 'product2', 'product2'], ['price', 'revenue', 'price', 'revenue']])

price_str = 'product1'
print(CEO_price_training[price_str])
CEO_price_training.loc[0] = None
CEO_price_training.loc[0,(price_str,'price')] = 1
CEO_price_training.loc[1] = None
CEO_price_training.loc[1,(price_str,'price')] = 1
print(CEO_price_training[price_str])
print(CEO_price_training[price_str].loc[0:2, 'price'])

import numpy as np
df_training = CEO_price_training[price_str]
dataset_x = np.array(df_training['price'].values)
print(dataset_x)
