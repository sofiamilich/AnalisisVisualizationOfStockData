import data_download as dd
import data_plotting as dplt
import analysis_data_mean as da
# import analysis_data_mean
import pandas as pd

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
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc),"
          " GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: "
          "1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Fetch stock data
    # Загружаем данные об акциях
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    # Добавим скользящую среднюю к данным
    stock_data = dd.add_moving_average(stock_data)

    # Plot the data
    # Построим график
    dplt.create_and_save_plot(stock_data, ticker, period)

    # Вычислим и выведем среднюю цену закрытия акций
    da.display_mean_closing_price(stock_data)

    # Уведомляем о сильных колебаниях
    threshold_options = {
        5: "небольшие колебания цены акций",
        10: "средние колебания цены акций",
        20: "значительные колебания цены акций",
    }

    da.notify_if_strong_fluctuations(stock_data, threshold_options)

    # Экспорт данных в CSV
    dd.export_data_to_csv(stock_data, f"{ticker}_{period}_stock_data.csv")

    # Экспорт данных в Excel
    dd.export_data_to_excel(stock_data, f"{ticker}_{period}_stock_data.xlsx")

    # # Создание таблицы с данными для консоли
    # data_table = dd.collect_console_data_new(stock_data, ticker, period)

    # Создание таблицы с данными для консоли
    filename = "console_data_all.csv"
    dd.collect_console_data_new(stock_data, ticker, period, filename)

    # Экспорт данных в Excel для консоли
    dd.export_console_data_to_excel(pd.read_csv(filename), "console_data_all.xlsx")


if __name__ == "__main__":
    main()
