import pandas as pd
import numpy as np



coins = pd.read_excel('coin.xlsx')
column_list = list(coins.columns)
print(column_list)


View(coins)


coins.dtypes


coins ['date_added'] = pd.to_datetime(coins ['date_added'])

coins ['quote.USD.last_updated'] = pd.to_datetime(coins ['quote.USD.last_updated'])



#Add percentages

coins['quote.USD.volume_change_24h'] = coins['quote.USD.volume_change_24h'] * 1000

coins['quote.USD.percent_change_1h'] = (coins['quote.USD.percent_change_1h'].astype(str) + '%')
coins['quote.USD.percent_change_24h'] = (coins['quote.USD.percent_change_24h'].astype(str) + '%')
coins['quote.USD.percent_change_30d'] = (coins['quote.USD.percent_change_30d'].astype(str) + '%')
coins['quote.USD.percent_change_60d'] = (coins['quote.USD.percent_change_60d'].astype(str) + '%')
coins['quote.USD.percent_change_90d'] = (coins['quote.USD.percent_change_90d'].astype(str) + '%')

coins.to_excel('/Users/angeaduhire/Desktop/crypto2.xlsx', sheet_name='crypto2', startrow=1, index=False)



