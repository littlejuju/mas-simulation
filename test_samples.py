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
print(CEO_price_training[price_str].loc[:,['price', 'revenue']])
print(CEO_price_training[price_str].iloc[-1].tolist())
print(CEO_price_training[price_str].iloc[-1].tolist())

import numpy as np
df_training = CEO_price_training[price_str]
dataset_x = np.array(df_training['price'].values)
print(dataset_x)

# import keras
# import matplotlib.pyplot as plt
# # Sequential按顺序构成的模型
# from keras.models import Sequential
# # Dense全连接层
# from keras.layers import Dense, Activation
# # 优化器：随机梯度下降
# from keras.optimizers import SGD
#
# # 生成非线性数据模型
# x_data = np.linspace(-0.5,0.5,200)
# noise = np.random.normal(0, 0.02, x_data.shape)
# y_data = np.square(x_data) + noise
#
# # 显示随机点
# plt.scatter(x_data, y_data)
# plt.show()
#
# model = Sequential()
#
# # 在模型中添加一个全连接层
# # 神经网络结构：1-10-1，即输入层为1个神经元，隐藏层10个神经元，输出层1个神经元。
#
# # 激活函数加法1
# model.add(Dense(units=10, input_dim=1))
# model.add(Activation('tanh'))
# model.add(Dense(units=1))
# model.add(Activation('tanh'))
#
# # 激活函数加法2
# # model.add(Dense(units=10, input_dim=1, activation='relu'))
# # model.add(Dense(units=1, activation='relu'))
#
# # 定义优化算法
# sgd = SGD(lr=0.3)
# # sgd: Stochastic gradient descent,随机梯度下降法
# # mse: Mean Squared Error, 均方误差
# model.compile(optimizer=sgd, loss='mse')
#
# # 进行训练
# for step in range(3001):
#     # 每次训练一个批次
#     cost = model.train_on_batch(x_data, y_data)
#     # 每500个batch打印一次cost值
#     if step % 500 == 0:
#         print('cost: ', cost)
# # 打印权值和偏置值
# W, b = model.layers[0].get_weights()
# print('W：', W, ' b: ', b)
# print(len(model.layers))
#
# # 把x_data输入网络中，得到预测值y_pred
# y_pred = model.predict(x_data)
#
# # 显示随机点
# plt.scatter(x_data, y_data)
# # 显示预测结果
# plt.plot(x_data, y_pred, 'r-', lw=3)
# plt.show()
# # 打印输出结果：
# # cost:  0.11566254
# # cost:  0.0059284647
# # cost:  0.005420627
# # cost:  0.0039270753
# # cost:  0.0012707997
# # cost:  0.0023045745
# # cost:  0.00043227203
# # W： [[-0.8097365   0.873398    0.46838143  0.16048421  0.23931012  0.37379673
# #    1.6485813   0.02880438  0.05999178  0.2506774 ]]  b:  [-0.3891211  -0.27747348 -0.0352951   0.1672752   0.04472595  0.08710503
# #   0.730751    0.21009925 -0.1056181   0.17212172]
# # 4
# test_list = [0,0,2,2,1,3,5]
# print(test_list.count(4))

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
#
# credentials = ServiceAccountCredentials.from_json_keyfile_name('My First Project-16ced2a4af64.json', scope)
# gc = gspread.authorize(credentials)
# try:
#     sh = gc.open('DataCenter')
#     print('open done')
# except gspread.exceptions.SpreadsheetNotFound:
#     sh = gc.create('DataCenter')
#     print('create done')
# try:
#     worksheet = sh.worksheet("test_sample worksheet")
#     sh.del_worksheet(worksheet)
#     worksheet = sh.add_worksheet(title="test_sample worksheet", rows="100", cols="20")
# except gspread.exceptions.WorksheetNotFound:
#     worksheet = sh.add_worksheet(title="test_sample worksheet", rows="100", cols="20")
#     print('add done')
# worksheet.update_acell('B1', 'Bingo!')

test_dict = {'a':[0,0,1],'b':[0],'c':[0,0,0,2,2,2,2]}
# print(pd.DataFrame(test_dict))
df_list = [pd.DataFrame({key: test_dict[key]}) for key in test_dict]
print(pd.concat(df_list, ignore_index=True, axis=1))

# worksheet = sh.add_worksheet(title="A worksheet", rows="100", cols="20")