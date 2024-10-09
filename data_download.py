import yfinance as yf
import pandas as pd
import os

# data_download.py:
# Файл отвечает за загрузку данных об акциях.
# Содержит функции для извлечения данных об акциях из интернета и расчёта скользящего среднего.


def fetch_stock_data(ticker, period='1mo'):
    """
    Получаем исторические данные об акциях для указанного тикера и временного периода.
    Возвращает DataFrame с данными.
    ticker: имя тикера, который ввел пользователь
    period: период, который запросил пользователь
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
    Добавляем в DataFrame колонку со скользящим средним,
    рассчитанным на основе цен закрытия.
    Параметры:
    data (DataFrame): данные
    window_size: размер окна
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def export_data_to_csv(data, filename):
    """
    Экспортирует данные в файл CSV.

    Параметры:
    data (DataFrame): данные для экспорта
    filename (str): имя файла для сохранения данных
    """
    data.to_csv(filename, index=False)
    print(f"Данные экспортированы в {filename}")


def export_data_to_excel(data, filename):
    """
    Экспортирует данные в файл Excel.

    Параметры:
    data (DataFrame): данные для экспорта
    filename (str): имя файла для сохранения данных
    """
    data.to_excel(filename, index=False)
    print(f"Данные экспортированы в {filename}")


def collect_data(stock_data, ticker, period):
    """
    Собирает данные в таблицу.

    Параметры:
    stock_data (DataFrame): Данные об акциях
    ticker (str): Тикер, введенный пользователем
    period (str): Период, введенный пользователем
    """
    data = {
        'Дата выгрузки': [pd.Timestamp.now()],
        'Тикер': [ticker],
        'Период': [period],
        'Средняя цена закрытия': [stock_data['Close'].mean()],
        'Максимальная цена закрытия': [stock_data['Close'].max()],
        'Минимальная цена закрытия': [stock_data['Close'].min()],
        'Колебания цены': [(stock_data['Close'].max() - stock_data['Close'].min()) / stock_data['Close'].mean()]
    }
    df = pd.DataFrame(data)
    return df


# def collect_console_data(stock_data, ticker, period):
#     """
#     Собирает данные в таблицу для консоли.
#
#     Параметры:
#     stock_data (DataFrame): Данные об акциях
#     ticker (str): Тикер, введенный пользователем
#     period (str): Период, введенный пользователем
#     """
#     data = {
#         'Дата выгрузки': [pd.Timestamp.now()],
#         'Тикер': [ticker],
#         'Период': [period],
#         'Средняя цена закрытия': [stock_data['Close'].mean()],
#         'Максимальная цена закрытия': [stock_data['Close'].max()],
#         'Минимальная цена закрытия': [stock_data['Close'].min()],
#         'Колебания цены': [(stock_data['Close'].max() - stock_data['Close'].min()) / stock_data['Close'].mean()]
#     }
#     df = pd.DataFrame(data)
#     return df


def export_console_data_to_csv(data, filename):
    """
    Экспортирует данные, которые выводили в консоль в файл CSV.

    Параметры:
    data (DataFrame): данные для экспорта
    filename (str): имя файла для сохранения данных
    """
    data.to_csv(filename, index=False)
    print(f"Данные экспортированы в {filename}")


def export_console_data_to_excel(data, filename):
    """
    Экспортирует данные из консоли в файл Excel.

    Параметры:
    data (DataFrame): данные для экспорта
    filename (str): имя файла для сохранения данных
    """
    data.to_excel(filename, index=False)
    print(f"Данные экспортированы в {filename}")


def collect_console_data_new(stock_data, ticker, period, filename):
    """
    Собирает данные из консоли в общую таблицу, которая сортируется по дате сбора данных.

    Параметры:
    stock_data (DataFrame): данные об акциях
    ticker (str): тикер, введенный пользователем
    period (str): период, введенный пользователем
    filename (str): имя файла для сохранения данных
    """
    data = {
        'Дата выгрузки': [pd.Timestamp.now()],
        'Тикер': [ticker],
        'Период': [period],
        'Средняя цена закрытия': [stock_data['Close'].mean()],
        'Максимальная цена закрытия': [stock_data['Close'].max()],
        'Минимальная цена закрытия': [stock_data['Close'].min()],
        'Колебания цены': [(stock_data['Close'].max() - stock_data['Close'].min()) / stock_data['Close'].mean()]
    }
    df = pd.DataFrame(data)
    df['Дата выгрузки'] = pd.to_datetime(df['Дата выгрузки'])  # Преобразуем к типу datetime

    # Проверяем, существует ли файл
    if os.path.exists(filename):
        # Если файл существует, читаем существующие данные и добавляем новые
        existing_data = pd.read_csv(filename)
        existing_data['Дата выгрузки'] = pd.to_datetime(existing_data['Дата выгрузки'],
                                                        errors='coerce')  # Преобразуем к типу datetime
        df = pd.concat([existing_data, df])
        df['Дата выгрузки'] = pd.to_datetime(df['Дата выгрузки'], errors='coerce')  # Преобразуем к типу datetime
        df = df.sort_values(by='Дата выгрузки')  # Сортируем по дате выгрузки

    df.to_csv(filename, index=False)
    print(f"Данные экспортированы в {filename}")
