import data_download as dd
import analysis_data_mean as da
import os
import data_plotting as dplt
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    # Выводим доступные стили
    print("Доступные стили для графика:", plt.style.available)
    # Устанавливаем стиль seaborn
    sns.set()
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), "
          "GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.")
    print("Вы также можете ввести пользовательские даты в формате YYYY-MM-DD.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца или"
                   " 'YYYY-MM-DD' - дату начала периода, который хотите увидеть): ")

    # Проверяем, являются ли введенные данные датами или периодом
    if len(period) == 10 and period[4] == '-' and period[7] == '-':
        start_date = period
        end_date = input("Введите дату окончания (в формате YYYY-MM-DD): ")
        stock_data = dd.fetch_stock_data(ticker, start=start_date, end=end_date)
    else:
        stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Let's add RSI
    stock_data = dd.calculate_rsi(stock_data)

    # Adding a function call
    stock_data = dd.calculate_macd(stock_data)

    # User selects the style of the plot
    style = input("Выберите стиль графика (например, 'Solarize_Light2', '_classic_test_patch', '_mpl-gallery',"
                  " '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', "
                  "'grayscale', 'seaborn-v0_8'): ")

    # Plot the data dplt.create_and_save_plot(stock_data, ticker, period)
    dplt.create_and_save_plot(stock_data, ticker, period, style)

    # Calculate and display mean closing price
    da.display_mean_closing_price(stock_data)

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
