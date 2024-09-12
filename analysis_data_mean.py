import pandas as pd



def mean_closing_price(data):

    # Вычисляет среднюю цену закрытия акций за период
    # data - DataFrame с данными об акциях
    # float - средняя цена закрытия акций за период

    return data['Close'].mean()

def display_mean_closing_price(data):

    # Вычисляем и выводим среднюю цену закрытия акций за период
    mean_price = mean_closing_price(data)
    print(f"Средняя цена закрытия акций за период: {mean_price}")


