# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import os


# data_plotting.py:
# Отвечает за визуализацию данных.
# Содержит функции для создания и сохранения графиков цен закрытия
# и скользящих средних.


# Создаём график, отображающий цены закрытия и скользящие средние.
# Предоставляет возможность сохранения графика в файл. Параметр filename -
# если он не указан, имя файла генерируется автоматически.
def create_and_save_plot(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
            if 'RSI' in data.columns:
                plt.plot(dates, data['RSI'].values, label='RSI')
            if 'MACD' in data.columns and 'Signal' in data.columns:
                plt.plot(dates, data['MACD'].values, label='MACD')
                plt.plot(dates, data['Signal'].values, label='Signal')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        if 'RSI' in data.columns:
            plt.plot(data['Date'], data['RSI'], label='RSI')
        if 'MACD' in data.columns and 'Signal' in data.columns:
            plt.plot(data['Date'], data['MACD'], label='MACD')
            plt.plot(data['Date'], data['Signal'], label='Signal')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    export_folder = "export/chart"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    export_path = os.path.join(export_folder, filename)
    plt.savefig(export_path)
    print(f"График сохранен как {export_path}")
