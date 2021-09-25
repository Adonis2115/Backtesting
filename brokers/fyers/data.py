from fyers_api import fyersModel
from fyers_api import accessToken
import json
import pandas as pd
import psycopg2

f = open('./brokers/fyers/credentials.json')
credentials = json.load(f)
appID = credentials['appID']
token = credentials['token']

fyers = fyersModel.FyersModel(client_id=appID, token=token, log_path="C:/Users/Himanshu Pandey/Documents/Project/Code/backtrader/brokers/fyers/logs")
is_async = True

data = {"symbol":"NSE:BANKNIFTY21SEPFUT","resolution":"1","date_format":"1","range_from":"2021-09-01","range_to":"2021-09-25","cont_flag":"1"}

df = pd.DataFrame(fyers.history(data)['candles'])
df[0] = pd.to_datetime(df[0], unit='s')
df[0] = df[0] + pd.Timedelta('05:30:00')
df[6] = [d.date() for d in df[0]]
df[7] = [d.time() for d in df[0]]
del df[0]
clist = list(df.columns)
clist_new = clist[-1:]+clist[:-1]
df = df[clist_new]
clist = list(df.columns)
clist_new = clist[-1:]+clist[:-1]
df = df[clist_new]
df.insert(0, 0, 'BANKNIFTY21SEPFUT')
df.to_csv('./Data/Custom/BANKNIFTY21SEPFUT.csv', index=False, header=False)
print(df)