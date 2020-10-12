import requests
import numpy as np
import pandas as pd

def precio_btc(ticket, interval, limit):
    url = "https://api.binance.com/api/v3/klines"
    querystring = {"symbol":ticket,"interval":interval,"limit":limit}
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "*"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    nparray = np.array(response.json())
    print(nparray)
    return pd.DataFrame(nparray.reshape(-1,12),dtype=float, columns = ('Open Time',
                                                                    'Open',
                                                                    'High',
                                                                    'Low',
                                                                    'Close',
                                                                    'Volume',
                                                                    'Close time',
                                                                    'Quote asset volume',
                                                                    'Number of trades',
                                                                    'Taker buy base asset volume',
                                                                    'Taker buy quote asset volume',
                                                                    'Ignore'))


