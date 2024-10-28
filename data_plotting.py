import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from data_download import calculate_standard_deviation
import plotly.graph_objs as go
import plotly.offline as pyo

# Устанавливаем стиль seaborn
sns.set()


# data_plotting.py:
# Отвечает за визуализацию данных.
# Содержит функции для создания и сохранения графиков цен закрытия
# и скользящих средних.


# Создаём график, отображающий цены закрытия и скользящие средние.
# Предоставляет возможность сохранения графика в файл. Параметр filename -
# если он не указан, имя файла генерируется автоматически.
def create_and_save_plot(data, ticker, period, style='classic', filename=None):
    """Создаёт график, отображающий цены закрытия и скользящие средние."""

    plt.style.use(style)  # Применяем выбранный стиль
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
        plt.plot(data['Date'], data['Close'], label='Close Price', color='red')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        if 'RSI' in data.columns:
            plt.plot(data['Date'], data['RSI'], label='RSI')
        if 'MACD' in data.columns and 'Signal' in data.columns:
            plt.plot(data['Date'], data['MACD'], label='MACD')
            plt.plot(data['Date'], data['Signal'], label='Signal')

    # Добавляем стандартное отклонение на график
    std_dev = calculate_standard_deviation(data)
    mean_price = data['Close'].mean()
    plt.axhline(mean_price + std_dev, color='red', linestyle='--', label='Mean + Std Dev')
    plt.axhline(mean_price - std_dev, color='blue', linestyle='--', label='Mean - Std Dev')

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


def create_interactive_plot(data, ticker, period):
    """Создаёт интерактивный график, отображающий цены закрытия и скользящие средние."""

    # Создаем график
    fig = go.Figure()

    # Добавляем цены закрытия
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='red')))

    # Добавляем скользящее среднее
    if 'Moving_Average' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Moving Average',
                                 line=dict(color='blue')))

    # Добавляем RSI, если есть
    if 'RSI' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI', line=dict(color='green')))

    # Добавляем MACD, если есть
    if 'MACD' in data.columns and 'Signal' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD', line=dict(color='orange')))
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Signal'], mode='lines', name='Signal', line=dict(color='purple')))

    # Обновляем макет графика
    fig.update_layout(title=f"{ticker} Цена акций с течением времени",
                      xaxis_title="Дата",
                      yaxis_title="Цена",
                      legend_title="Легенда")

    # Сохраняем график в файл HTML
    export_folder = "export/interactive_chart"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    export_path = os.path.join(export_folder, f"{ticker}_{period}_interactive_chart.html")
    pyo.plot(fig, filename=export_path, auto_open=True)
    print(f"Интерактивный график сохранен как {export_path}")

# Код без интерактивного графика

# import matplotlib.pyplot as plt
# import pandas as pd
# import os
# import seaborn as sns
# from data_download import calculate_standard_deviation
#
# # Устанавливаем стиль seaborn
# sns.set()
#
#
# # data_plotting.py:
# # Отвечает за визуализацию данных.
# # Содержит функции для создания и сохранения графиков цен закрытия
# # и скользящих средних.
#
#
# # Создаём график, отображающий цены закрытия и скользящие средние.
# # Предоставляет возможность сохранения графика в файл. Параметр filename -
# # если он не указан, имя файла генерируется автоматически.
# def create_and_save_plot(data, ticker, period, style='classic', filename=None):
#     """Создаёт график, отображающий цены закрытия и скользящие средние."""
#
#     plt.style.use(style)  # Применяем выбранный стиль
#     plt.figure(figsize=(10, 6))
#
#     if 'Date' not in data:
#         if pd.api.types.is_datetime64_any_dtype(data.index):
#             dates = data.index.to_numpy()
#             plt.plot(dates, data['Close'].values, label='Close Price')
#             plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
#             if 'RSI' in data.columns:
#                 plt.plot(dates, data['RSI'].values, label='RSI')
#             if 'MACD' in data.columns and 'Signal' in data.columns:
#                 plt.plot(dates, data['MACD'].values, label='MACD')
#                 plt.plot(dates, data['Signal'].values, label='Signal')
#         else:
#             print("Информация о дате отсутствует или не имеет распознаваемого формата.")
#             return
#     else:
#         if not pd.api.types.is_datetime64_any_dtype(data['Date']):
#             data['Date'] = pd.to_datetime(data['Date'])
#         plt.plot(data['Date'], data['Close'], label='Close Price', color='red')
#         plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
#         if 'RSI' in data.columns:
#             plt.plot(data['Date'], data['RSI'], label='RSI')
#         if 'MACD' in data.columns and 'Signal' in data.columns:
#             plt.plot(data['Date'], data['MACD'], label='MACD')
#             plt.plot(data['Date'], data['Signal'], label='Signal')
#
#     # Добавляем стандартное отклонение на график
#     std_dev = calculate_standard_deviation(data)
#     mean_price = data['Close'].mean()
#     plt.axhline(mean_price + std_dev, color='red', linestyle='--', label='Mean + Std Dev')
#     plt.axhline(mean_price - std_dev, color='blue', linestyle='--', label='Mean - Std Dev')
#
#     plt.title(f"{ticker} Цена акций с течением времени")
#     plt.xlabel("Дата")
#     plt.ylabel("Цена")
#     plt.legend()
#
#     if filename is None:
#         filename = f"{ticker}_{period}_stock_price_chart.png"
#
#     export_folder = "export/chart"
#     if not os.path.exists(export_folder):
#         os.makedirs(export_folder)
#     export_path = os.path.join(export_folder, filename)
#     plt.savefig(export_path)
#     print(f"График сохранен как {export_path}")
