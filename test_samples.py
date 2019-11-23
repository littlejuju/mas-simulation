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
print(df['a'].tolist())
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
# from keras.models import Sequential
# from keras.layers import Dense, Activation
#
# from keras.optimizers import SGD
#
# x_data = np.linspace(-0.5,0.5,200)
# noise = np.random.normal(0, 0.02, x_data.shape)
# y_data = np.square(x_data) + noise
#
# plt.scatter(x_data, y_data)
# plt.show()
#
# model = Sequential()
#
#
# model.add(Dense(units=10, input_dim=1))
# model.add(Activation('tanh'))
# model.add(Dense(units=1))
# model.add(Activation('tanh'))
#
# # model.add(Dense(units=10, input_dim=1, activation='relu'))
# # model.add(Dense(units=1, activation='relu'))
#
#
# sgd = SGD(lr=0.3)
# # sgd: Stochastic gradient descent
# # mse: Mean Squared Error
# model.compile(optimizer=sgd, loss='mse')
#
# # 进行训练
# for step in range(3001):
#
#     cost = model.train_on_batch(x_data, y_data)
#     # 每500个batch打印一次cost值
#     if step % 500 == 0:
#         print('cost: ', cost)
#
# W, b = model.layers[0].get_weights()
# print('W：', W, ' b: ', b)
# print(len(model.layers))
#
#
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
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# mail_content = '''Hello,
# This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
# Thank You
# '''
# #The mail addresses and password
# sender_address = 'a0195470yrobot@gmail.com'
# sender_pass = 'h+X730630'
# receiver_address = 'a0195470yreceiver@gmail.com'
# #Setup the MIME
# message = MIMEMultipart()
# message['From'] = sender_address
# message['To'] = receiver_address
# message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
# #The body and the attachments for the mail
# message.attach(MIMEText(mail_content, 'plain'))
# #Create SMTP session for sending the mail
# session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
# session.starttls() #enable security
# session.login(sender_address, sender_pass) #login with mail_id and password
# text = message.as_string()
# session.sendmail(sender_address, receiver_address, text)
# session.quit()
# print('Mail Sent')
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
fig.set_tight_layout(True)

#  询问图形在屏幕上的尺寸和DPI（每英寸点数）。
#  注意当我们把图形储存成一个文件时，我们需要再另外提供一个DPI值
print('fig size: {0} DPI, size in inches {1}'.format(
    fig.get_dpi(), fig.get_size_inches()))

# 画出一个维持不变（不会被重画）的散点图和一开始的那条直线。
x = np.arange(0, 20, 0.1)
ax.scatter(x, x + np.random.normal(0, 3.0, len(x)))
line, = ax.plot(x, x - 5, 'r-', linewidth=2)

def update(i):
    label = 'timestep {0}'.format(i)
    print(label)
    # 更新直线和x轴（用一个新的x轴的标签）。
    # 用元组（Tuple）的形式返回在这一帧要被重新绘图的物体
    line.set_ydata(x - 5 + i)
    ax.set_xlabel(label)
    return line, ax
save = True
if __name__ == '__main__':
    # FuncAnimation 会在每一帧都调用“update” 函数。
    # 在这里设置一个10帧的动画，每帧之间间隔200毫秒
    anim = FuncAnimation(fig, update, frames=np.arange(0, 10), interval=200)
    if save:
        anim.save('C:/Users/Xiangqi/Desktop/Singapore Modules Folders/is5006/MAS_v3_git/mas-simulation/line.gif', dpi=80, writer='imagemagick')
    else:
        # plt.show() 会一直循环播放动画
        plt.show()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = np.linspace(0, 10, 100)
y = 1+ np.random.randint(0,10,size=(100,1))*0.1
print(y)

fig, ax = plt.subplots()
line, = ax.plot(x, y, color='k')
line2, = ax.plot(x, y-0.1, color='k')


print(type(line))

def update(num, x, y, line):
    line.set_data(x[:num], y[:num])
    line.axes.axis([0, 10, 0, 2])
    line2.set_data(x[:num], (y-1)[:num])
    line2.axes.axis([0, 10, 0, 2])
    return [line,line2]  # 可以同时画两个或多个线，只要在update函数中返回多个线即可


ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line],
                              interval=25, blit=True)
ani.save('test.gif')
plt.show()

