#import libraries
from requests import Request, Session
import json
import pprint
import pandas as pd
import yaml
import numpy as np
import openpyxl
from openpyxl import load_workbook


#get data from coinmarketcap - latest quotes
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

#create a dictionary with the name of the latest 100 crytos converted in USD
  parameters_USD = {
  'start':'1',
  'limit':'100',
  'convert':'USD'
}

#create a dictionary with the name of the latest 100 crytos converted in EUR
  parameters_EUR = {
  'start':'1',
  'limit':'100',
  'convert':'EUR'
}

#load the API key from my local file
path = r'/Users//Users/angeaduhire/Desktop/Programming/PWC_WebScrapping/CoinMarket_Project/CoinMarket.yml'
with open(path) as file:
    apikey = yaml.load(file, Loader=yaml.FullLoader)['api_key']

#create a dictionary to pass the API key
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': apikey,
}

#create the session
session = Session()
session.headers.update(headers)

#get the response urls 
response_latest_USD = session.get(url, params = parameters_USD)
response_latest_EUR = session.get(url, params = parameters_EUR)

#Data wrangling - load data in json format 
json_data_latest_USD = json.loads(response_latest_USD.text)
json_data_latest_EUR = json.loads(response_latest_EUR.text)

#Data wrangling - transform the json data into a dataframe
##for USD
data_latest_USD = pprint.pprint(json_data_latest_USD)
data_latest_USD = pd.json_normalize(json_data_latest_USD, record_path =['data'])
View(data_latest_USD)

##for EUR
data_latest_EUR = pprint.pprint(json_data_latest_EUR)
data_latest_EUR = pd.json_normalize(json_data_latest_EUR, record_path =['data'])
View(data_latest_EUR)

#Data wrangling - 
#remove NaN from the dataframes
data_latest_USD = data_latest_USD.fillna("")
data_latest_EUR = data_latest_EUR.fillna("")
#remove all the blank rows
data_latest_USD = data_latest_USD.dropna(how='all')
data_latest_EUR = data_latest_EUR.dropna(how='all')
#remove all the blank columns
data_latest_USD = data_latest_USD.loc[:, (data_latest_USD != "").any(axis=0)]
data_latest_EUR = data_latest_EUR.loc[:, (data_latest_EUR != "").any(axis=0)]

#format numbers 
##to a friendlier reading format: separate by comas, 3 decimals 
dataUSD = data_latest_USD.applymap(lambda x: f'{x:,.3f}' if isinstance(x, float) else x)
dataEUR = data_latest_EUR.applymap(lambda x: f'{x:,.3f}' if isinstance(x, float) else x)

##colouring negative values in red, and positive values in black
def highlight_val(cell):
    if type(cell) != str and cell < 0 :
        return 'color: red'
    else:
        return 'color: black'
  
dataUSD.style.applymap(highlight_val)
dataEUR.style.applymap(highlight_val)

#review data
View(dataUSD)
dataUSD.info()
View(dataEUR)
dataEUR.info()


#Write DataFrame to Excel file, Sheet Name: USD"
path='/Users/angelinadavies/behaviouralTool/Desktop/Alexandre Ball/Coins.xlsx'
writer = pd.ExcelWriter(path, engine = 'openpyxl')

with pd.ExcelWriter(path) as writer:
    dataUSD.to_excel(writer, index=False, sheet_name='dataUSD')
    dataEUR.to_excel(writer, index=False, sheet_name='dataEUR')
