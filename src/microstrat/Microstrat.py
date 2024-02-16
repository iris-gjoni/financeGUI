import pandas as pd
from src import DateFormattingHelper

x_field = 'Date'
y_field = 'Close'
btc_held = 189150
mstr_outstanding_shares = 13670000
mstr_diluted_outstanding_shares = 16720000

final_string: str = "c:/quant/historicalStockPrices/historical_MSTR.csv"
final_btc_string: str = "c:/quant/historicalStockPrices/historical_BTC-USD.csv"

df = pd.read_csv(final_string)
y_values: float = df[y_field]

df2 = pd.read_csv(final_btc_string)
# btc_price = df2[y_field].iloc[-1]
btc_price = 43000
# mstr_price = df[y_field].iloc[-1]
mstr_price = 505
mstr_bus_value = 1_500_000_000

print("======")
print("#btc price: ", round(btc_price, 2))
print("======")
print("#mstr price: ",mstr_price)
print("======")
btc_cap = btc_price * btc_held
print("mstr btc market cap: ", round(btc_cap, 2))
print("======")
m_cap = mstr_price * mstr_outstanding_shares
# print("mstr market cap: ", round(m_cap,2))
# print("premium: ", round(m_cap / btc_cap * 100,2))
# print("======")
m_d_cap = mstr_price * mstr_diluted_outstanding_shares
print("mstr market cap diluted: ", round(m_d_cap,2))
print("premium: ", round(m_d_cap / btc_cap * 100, 2))
print("======")
cap_inc_biz = btc_cap + mstr_bus_value
print("mstr market cap diluted incl biz: ", round(cap_inc_biz,2))
print("premium: ", round(m_d_cap / cap_inc_biz * 100, 2))
print("======")
btc_share = btc_held / mstr_diluted_outstanding_shares
my_btc_share = btc_share * 21.5
print("btc per share: ", round(btc_share,5))
print("my mstr btc : ", round(my_btc_share,5))

