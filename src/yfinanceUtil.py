import yfinance as yf


def get_income(ticker):
    ins = yf.Ticker(ticker)
    incomestmt = ins.incomestmt
    print(incomestmt)


def get_balance_sheet(ticker):
    ins = yf.Ticker(ticker)
    balance = ins.balance_sheet
    print(balance)


def get_cash_flow(ticker):
    ins = yf.Ticker(ticker)
    cash = ins.cash_flow
    print(cash)


def get_news(ticker):
    ins = yf.Ticker(ticker)
    news = ins.news
    print(news)


if __name__ == "__main__":
    # get_income("AAPL")
    # get_balance_sheet("AAPL")
    # get_cash_flow("AAPL")
    # get_news("AAPL")
    ins = yf.Ticker("AAPL")
    actions = ins.actions
    print(actions)
    earn_dates = ins.earnings_dates
    print(earn_dates)
