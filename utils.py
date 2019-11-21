import matplotlib.pyplot as plt
import numpy as np
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