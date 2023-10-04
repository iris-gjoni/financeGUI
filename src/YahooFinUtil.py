import csv
import datetime
import yahoo_fin.stock_info as si
import DateFormattingHelper
import pandas as pd


def refresh_data(ticker, start_date, end_date):
    start_date_holder = DateFormattingHelper.parse_date(start_date) + datetime.timedelta(days=1)
    end_date_holder = DateFormattingHelper.parse_date(end_date)
    today = DateFormattingHelper.parse_date(str(datetime.date.today()))
    if start_date_holder < today:
        data = si.get_data(ticker,
                           start_date=start_date_holder,
                           end_date=end_date_holder,
                           interval='1d',
                           index_as_date=False)
        # print("data from yahoo :", data)
        return data
    else:
        print("data for today exists!")
    return None


def read_most_recent_entry_in_csv(filepath):
    df = pd.read_csv(filepath)
    columns = df.columns.tolist()
    # print("columns:", columns)

    if columns.__contains__('date'):
        df = df.sort_values(by='date', ascending=False)
        most_recent_row = df.iloc[0]
        # print("row: ", most_recent_row)
        return most_recent_row, 2
    elif columns.__contains__('Date'):
        df = df.sort_values(by='Date', ascending=False)
        most_recent_row = df.iloc[0]
        # print("row: ", most_recent_row)
        return most_recent_row, 1
    else:
        most_recent_row = df.iloc[0]
        # print(most_recent_row)
        return most_recent_row, 0


def append_new_data_to_file(new_data_df, filepath):
    # headers = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    check_for_new_line(file_path=filepath)

    new_data_df.set_index('date')
    new_data_df.drop('ticker', axis=1, inplace=True)
    new_data_df = new_data_df.round(6)
    new_data_df['date'] = pd.to_datetime(new_data_df['date']).dt.strftime('%Y-%m-%d')
    with open(filepath, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=new_data_df.columns)
        for index, row in new_data_df.iterrows():
            row_dict = row.to_dict()
            # row_dict['date'] = index
            writer.writerow(row_dict)
            print("Data appended to the CSV file ", row_dict)


def check_for_new_line(file_path):
    with open(file_path, 'rb') as file:
        # Go to the last byte of the file
        file.seek(-1, 2)  # 2 means "from the end of the file"

        # Read the last byte
        last_char = file.read().decode()

        # Check if the last character is a newline
        needs_newline = last_char != '\n'
    # If the file does not end with a newline, append one
    if needs_newline:
        with open(file_path, 'a', newline='') as file:
            file.write('\n')


def append_new_data(ticker_name, filepath_for_test):
    recent_entry_df, contains_date = read_most_recent_entry_in_csv(filepath_for_test)
    if contains_date == 0:
        print("no date")
    elif contains_date == 1:
        data_from_server = refresh_data(ticker_name, recent_entry_df['Date'], datetime.date.today().strftime("%d-%m-%Y"))
        if data_from_server is not None:
            append_new_data_to_file(data_from_server, filepath_for_test)
        else:
            print("emtpy data: ", data_from_server)
    elif contains_date == 2:
        data_from_server = refresh_data(ticker_name, recent_entry_df['date'], datetime.date.today().strftime("%d-%m-%Y"))
        if data_from_server is not None:
            append_new_data_to_file(data_from_server, filepath_for_test)
        else:
            print("emtpy data: ", data_from_server)

# ===== testing ===========


def test_read_recent_row():
    read_most_recent_entry_in_csv(
        "c:/quant/historicalStockPrices/historical_AAPL.csv"
    )


def test_refresh_data():
    refresh_data("AAPL",
                 "25-09-2023",
                 datetime.date.today().strftime("%d-$m-%Y"))


if __name__ == "__main__":
    # test_read_recent_row()
    # test_refresh_data()
    ticker = "AAPL"
    filepath = "c:/quant/historicalStockPrices/historical_AAPL.csv"
    append_new_data(ticker, filepath)
