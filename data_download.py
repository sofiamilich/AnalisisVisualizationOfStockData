import yfinance as yf
import os
import pandas as pd


# data_download.py:
# Файл отвечает за загрузку данных об акциях.
# Содержит функции для извлечения данных об акциях из интернета и расчёта скользящего среднего.


def fetch_stock_data(ticker, period=None, start=None, end=None):
    stock = yf.Ticker(ticker)
    if period:
        data = stock.history(period=period)
    else:
        data = stock.history(start=start, end=end)
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
    Экспортирует данные в файл CSV в новую папку Экспорты.

    Параметры:
    data (DataFrame): данные для экспорта
    filename (str): имя файла для сохранения данных
    """
    export_folder = "export"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    export_path = os.path.join(export_folder, filename)
    data.to_csv(export_path, index=False)
    print(f"Данные экспортированы в {export_path}")


def export_data_to_excel(data, filename):
    """
    Экспортирует данные в файл Excel в новую папку Экспорты.

    Параметры:
    data (DataFrame): данные для экспорта
    filename (str): имя файла для сохранения данных
    """
    export_folder = "export"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    export_path = os.path.join(export_folder, filename)
    data.to_excel(export_path, index=False)
    print(f"Данные экспортированы в {export_path}")


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


def export_console_data_to_csv(data, filename):
    """
    Экспортирует данные, которые выводили в консоль в файл CSV.

    Параметры:
    data (DataFrame): данные для экспорта
    filename (str): имя файла для сохранения данных
    """
    data.to_csv(filename, index=False)
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

    export_folder = "export"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    export_path = os.path.join(export_folder, filename)

    # Проверяем, существует ли файл
    if os.path.exists(export_path):
        # Если файл существует, читаем суще��твующие данные и добавляем новые
        existing_data = pd.read_csv(export_path)
        existing_data['Дата выгрузки'] = pd.to_datetime(existing_data['Дата выгрузки'],
                                                        errors='coerce')  # Преобразуем к типу datetime
        df = pd.concat([existing_data, df])
        df['Дата выгрузки'] = pd.to_datetime(df['Дата выгрузки'], errors='coerce')  # Преобразуем к типу datetime
        df = df.sort_values(by='Дата выгрузки')  # Сортируем по дате выгрузки

    df.to_csv(export_path, index=False)
    print(f"Данные экспортированы в {export_path}")

    # Экспортируем в Excel
    excel_filename = filename.replace('.csv', '.xlsx')
    excel_export_path = os.path.join(export_folder, excel_filename)
    df.to_excel(excel_export_path, index=False)
    print(f"Данные экспортированы в {excel_export_path}")


def calculate_rsi(data, window_size=14):
    """
    Рассчитывает относительный индекс силы (RSI) для данных.

    Параметры:
    data (DataFrame): Данные с колонкой 'Close'
    window_size (int): Размер окна для расчета RSI (по умолчанию=14)

    Возвращает:
    DataFrame с колонкой RSI
    """
    delta = data['Close'].diff(1)
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=window_size).mean()
    roll_down = down.rolling(window=window_size).mean().abs()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


def calculate_macd(data, fast_window=12, slow_window=26, signal_window=9):
    """
    Рассчитывает MACD.

    Параметры:
    data (DataFrame): Данные с колонкой 'Close'
    fast_window (int): Размер окна для быстрой скользящей средней (по умолчанию=12)
    slow_window (int): Размер окна для медленной скользящей средней (по умолчанию=26)
    signal_window (int): Размер окна для сигнальной скользящей средней (по умолчанию=9)

    Возвращает:
    DataFrame с колонками MACD и Signal
    """
    data['EMA_Fast'] = data['Close'].ewm(span=fast_window, adjust=False).mean()
    data['EMA_Slow'] = data['Close'].ewm(span=slow_window, adjust=False).mean()
    data['MACD'] = data['EMA_Fast'] - data['EMA_Slow']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data
