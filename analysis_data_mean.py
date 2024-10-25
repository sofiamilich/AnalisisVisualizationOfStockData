from data_download import calculate_standard_deviation


def display_mean_closing_price(data):
    """Вычисляет и выводит среднюю цену закрытия акций за период."""
    mean_price = data['Close'].mean()
    print(f"Средняя цена закрытия акций за период: {mean_price}")


def mean_closing_price(data):
    """Вычисляет среднюю цену закрытия акций за период
    data - DataFrame с данными об акциях
    float - средняя цена закрытия акций за период"""

    return data['Close'].mean()


def notify_if_strong_fluctuations(data, threshold_options):
    """Анализируем данные и уведомляем пользователя, если цена акций колебалась более чем на заданный процент за период
    data - DataFrame с данными об акциях
    threshold - заданный порог в процентах
    fluctuation - % колебания цены
    """

    max_close = data['Close'].max()  # максимальная цена закрытия
    print(f'Максимальная цена закрытия {max_close}')
    min_close = data['Close'].min()  # минимальная цена закрытия
    print(f'Минимальная цена закрытия {min_close}')
    fluctuation = (max_close - min_close) / data['Close'].mean() * 100  # колебание в процентах

    for threshold, description in threshold_options.items():
        if fluctuation > threshold:
            print(f"{description} цены акций за день, на {fluctuation} %")
            break


def plot_rsi():
    """Отображает значения RSI"""
    pass


def display_standard_deviation(data):
    """Вычисляем и выводим стандартное отклонение цен закрытия акций за период."""
    std_dev = calculate_standard_deviation(data)
    print(f"Стандартное отклонение цен закрытия акций за период: {std_dev}")
