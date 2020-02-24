import quandl
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import numpy as np

myurl = 'https://money.cnn.com/data/dow30/'
uClient = uReq(myurl)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("a", {"class":"wsod_symbol"})
symbols = [symbol.text for symbol in containers]


quandl.ApiConfig.api_key = 'jCoKHySC6kb3HRjxYFyp'
df = pd.DataFrame(quandl.get_table('WIKI/PRICES', ticker = symbols, 
                                   date = { 'gte': '2015-01-01', 'lte': '2019-12-31' },
                                   paginate = True))
rf_rate = quandl.get("USTREASURY/BILLRATES", 
                     authtoken="jCoKHySC6kb3HRjxYFyp")['52 Wk Bank Discount Rate']
rf_rate = (rf_rate.sort_index().tail(1)[0])
rf_rate_val = rf_rate / 252

df2 = df[['ticker', 'date', 'adj_open', 'adj_close']]
df2 = df2.set_index('date')
df2['daily_ret'] = df2['adj_close'] - df2['adj_open']
df2['daily_ret_perc'] = df2['daily_ret'] / df2['adj_open']
avg_return = df2['daily_ret_perc'].mean()
cov = np.cov(df2['daily_ret_perc'])
num_portfolios = 100000

df2['adj_close'].pct_change().mean()