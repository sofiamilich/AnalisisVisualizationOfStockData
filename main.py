import data_download as dd
import data_plotting as dplt
import analysis_data_mean as da
# import pandas as pd
import os

"""
main.py:
Файл является точкой входа в программу.
Запрашивает у пользователя тикер акции и временной период, загружает данные, обрабатывает
их и выводит результаты в виде графика.

Основная функция, управляющая процессом загрузки, обработки данных и их визуализации.
Запрашивает у пользователя ввод данных, вызывает функции загрузки и обработки
данных, а затем передаёт результаты на визуализацию.
"""


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc),"" "
          "GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: ""1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала "
          "года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Let's add RSI
    stock_data = dd.calculate_rsi(stock_data)

    # Adding a function call
    stock_data = dd.calculate_macd(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)

    # Calculate and display mean closing price
    da.display_mean_closing_price(stock_data)

    # da.plot_rsi(stock_data)

    # Notify if strong fluctuations
    threshold_options = {
        5: "Небольшие колебания цены акций",
        10: "Средние колебания цены акций",
        20: "Значительные колебания цены акций",
    }
    da.notify_if_strong_fluctuations(stock_data, threshold_options)

    # Export data to CSV
    export_folder = "export"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    filename = f"{ticker}_{period}_stock_data.csv"
    export_path = os.path.join(export_folder, filename)
    dd.export_data_to_csv(stock_data, export_path)

    # Export data to Excel
    filename = f"{ticker}_{period}_stock_data.xlsx"
    export_path = os.path.join(export_folder, filename)
    dd.export_data_to_excel(stock_data, export_path)

    # Create table with data for console
    filename = "console_data_all.csv"
    export_path = os.path.join(export_folder, filename)
    dd.collect_console_data_new(stock_data, ticker, period, export_path)


if __name__ == "__main__":
    main()
