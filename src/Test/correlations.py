import pandas as pd


x_field = 'Date'
y_field = 'Close'

final_mstr_string: str = "c:/quant/historicalStockPrices/historical_MSTR.csv"
final_btc_string: str = "c:/quant/historicalStockPrices/historical_BTC-USD.csv"
final_aapl_string: str = "c:/quant/historicalStockPrices/historical_AAPL.csv"
final_amzn_string: str = "c:/quant/historicalStockPrices/historical_AMZN.csv"

df_amzn = pd.read_csv(final_amzn_string)
df_btc = pd.read_csv(final_btc_string)
df_mstr = pd.read_csv(final_mstr_string)
df_aapl = pd.read_csv(final_aapl_string)


def run_with_number(num):
    global aapl_amzn_corr, aapl_btc_corr, aapl_mstr_corr, btc_mstr_corr, btc_amzn_corr
    mstr_values = df_mstr[y_field].iloc[-num:].reset_index(drop=True)
    btc_values = df_btc[y_field].iloc[-num:].reset_index(drop=True)
    amzn_values = df_amzn[y_field].iloc[-num:].reset_index(drop=True)
    aapl_values = df_aapl[y_field].iloc[-num:].reset_index(drop=True)
    aapl_amzn_corr = aapl_values.corr(amzn_values)
    aapl_btc_corr = aapl_values.corr(btc_values)
    aapl_mstr_corr = aapl_values.corr(mstr_values)
    btc_mstr_corr = btc_values.corr(mstr_values)
    btc_amzn_corr = btc_values.corr(amzn_values)

    print(f"{num}| aapl_amzn_corr: ", aapl_amzn_corr)
    print(f"{num}| aapl_btc_corr: ", aapl_btc_corr)
    print(f"{num}| aapl_mstr_corr: ", aapl_mstr_corr)
    print(f"{num}| btc_mstr_corr: ", btc_mstr_corr)
    print(f"{num}| btc_amzn_corr: ", btc_amzn_corr)
    print(f"===========")


run_with_number(14)
run_with_number(50)
run_with_number(200)
run_with_number(500)
run_with_number(1000)



