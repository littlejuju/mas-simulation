import matplotlib.pyplot as plt
import numpy


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
        plt.plot(numpy.cumsum(seller.revenue_history[product]), label='Cumulative Revenue')
        plt.plot(numpy.cumsum(seller.expense_history[product][:-1]), label='Cumulative Expenses')
        plt.plot(numpy.cumsum(seller.profit_history[product]), label='Cumulative Profit')
        plt.xticks(range(len(seller.revenue_history[product])))
        plt.legend()
    
        plt.subplot(313)
        plt.plot(seller.sentiment_history[product], label='User Sentiment')
        plt.xticks(range(len(seller.revenue_history[product])))
        plt.legend()
    plt.show()
