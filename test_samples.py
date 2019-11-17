# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:25:05 2019

@author: Xiangqi
"""

test_dict = {'a':2,'b':[1,2]}
print('a' in test_dict)
print('c' in test_dict)

test_tup = {'iphone':[(0,0.2)]}
for key in test_tup:
    for tup in test_tup[key]:
        print(tup[0])
        
test_tup = ['a',1]