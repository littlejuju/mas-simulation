import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

import random
from constants import tick_time, ticks
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures


def plot(seller):
    
    for product in seller.product_list:
        plt.figure(figsize=(6, 9))
        plt.subplots_adjust(hspace=0.5)
        plt.subplot(311)
        plt.plot(seller.revenue_history[product], label='Revenue')
        plt.plot(seller.expense_history[product][:-1], label='Expenses')
        plt.plot(seller.profit_history[product], label='Profit')
        plt.xticks(range(len(seller.revenue_history[product])))
        plt.legend()
        plt.title(seller.name.upper() + ' ' + product.name, size=16)
    
        plt.subplot(312)
        plt.plot(np.cumsum(seller.revenue_history[product]), label='Cumulative Revenue')
        plt.plot(np.cumsum(seller.expense_history[product][:-1]), label='Cumulative Expenses')
        plt.plot(np.cumsum(seller.profit_history[product]), label='Cumulative Profit')
        plt.xticks(range(len(seller.revenue_history[product])))
        plt.legend()
    
        plt.subplot(313)
        plt.plot(seller.sentiment_history[product], label='User Sentiment')
        plt.xticks(range(len(seller.revenue_history[product])))
        plt.legend()
    plt.show()

def regression(seller):
    if seller.CEO_type == 'random':
        return
    elif seller.CEO_type == 'poly2':
        for product in seller.product_list:
            plt.figure()
            model = seller.CEO_price_model[product]
            price_series = np.array(seller.price_history[product][1:])
            revenue_series = np.array(seller.revenue_history[product])
            # print(len(price_series))
            # print(len(revenue_series))
            axis_x = model['x']
            predict_y = model['y']
            plt.scatter(price_series, revenue_series, color='orange')
            plt.plot(axis_x, predict_y, color='blue')
            plt.xlabel('Price')
            plt.ylabel('Revenue')
            plt.title(seller.name.upper() + ' ' + product.name +
                      ' Regression: ' + str(seller.poly2_coef[product][0]) + ' + ' +
                      str(seller.poly2_coef[product][1]) + 'x + ' + str(seller.poly2_coef[product][2]) + 'x^2' , size=6)

        plt.show()
    elif 'sgd' in seller.CEO_type:
        for product in seller.product_list:
            plt.figure()
            model = seller.CEO_price_model[product]
            price_series = np.array(seller.price_history[product][1:])
            revenue_series = np.array(seller.revenue_history[product])
            axis_x = model['x']
            predict_y = model['y']
            plt.scatter(price_series, revenue_series, color='orange')
            plt.plot(axis_x, predict_y, color='blue')
            plt.xlabel('Price')
            plt.ylabel('Revenue')
            plt.title(seller.name.upper() + ' ' + product.name +
                      ' Regression: ' + seller.CEO_type, size=6)
        plt.show()

def Save(object, object_type):
    if object_type == 'customer':
        return
    elif object_type == 'seller':
        return
    elif object_type == 'datacenter':
        return

def animate(datacenter):
    # draw price_series
    df_price_series = datacenter.price_series.dropna(axis = 0)
    x = np.linspace(0, ticks, df_price_series.shape[0])
    # y = np.linspace(0, ticks, df_price_series.shape[0])
    fig, ax = plt.subplots()
    line_package = dict()

    for key in df_price_series.columns.tolist():
        # print(key)
        # print(df_price_series[key])
        line_package[key], = ax.plot(x, np.array(df_price_series[key].tolist()), color=random_color(), label = key)
    # line, = ax.plot(x, y, color='k')
    # print(type(line))
    ani = animation.FuncAnimation(fig, update1, len(x), fargs=[x, line_package, df_price_series],
                                  interval=250, blit=True)
    ani.save('C:/Users/Xiangqi/Desktop/Singapore Modules Folders/is5006/MAS_v3_git/mas-simulation/price_series.gif', dpi=80, writer='imagemagick')
    # draw sales rank
    df_sales_rank = datacenter.sales_rank.dropna(axis = 0)
    x = np.linspace(0, ticks, df_sales_rank.shape[0])
    # y = np.linspace(0, ticks, df_sales_rank.shape[0])
    fig, ax = plt.subplots()
    line_package = dict()

    for key in df_sales_rank.columns.tolist():
        # print(key)
        # print(df_sales_rank[key])
        line_package[key], = ax.plot(x, np.array(df_sales_rank[key].tolist()), color=random_color(), label = key)
    # line, = ax.plot(x, y, color='k')
    # print(type(line))
    ani = animation.FuncAnimation(fig, update2, len(x), fargs=[x, line_package, df_sales_rank],
                                  interval=250, blit=True)
    ani.save('C:/Users/Xiangqi/Desktop/Singapore Modules Folders/is5006/MAS_v3_git/mas-simulation/sales_rank.gif', dpi=80, writer='imagemagick')


def random_color():
    color_choice16 = "0123456789ABCDEF"
    defcolor = '#'+ str(random.sample(color_choice16, 6)).replace(',','').replace('[','').replace(']','').replace('\'','').replace(' ','')
    return defcolor
def update1(num, x, line_package, df_price_series):
    line_list = list()
    for key in line_package:
        line_package[key].set_data(x[:num], df_price_series[key].tolist()[:num])
        line_package[key].axes.axis([0, ticks+1, 60, 350])
        line_list.append(line_package[key])
    return line_list  # 可以同时画两个或多个线，只要在update函数中返回多个线即可
def update2(num, x, line_package, df_price_series):
    line_list = list()
    for key in line_package:
        line_package[key].set_data(x[:num], df_price_series[key].tolist()[:num])
        line_package[key].axes.axis([0, ticks+1, 0, 8])
        line_list.append(line_package[key])
    return line_list  # 可以同时画两个或多个线，只要在update函数中返回多个线即可