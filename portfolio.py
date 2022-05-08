    #1. Ask for API key
    #2. Charge list of possible stocks and cryptos
    #3. Create portfolio object with the two previous imputs
    #4. Propose list of stocks and cryptos
    #7. Link charge button to the get_data.add() function
    #8. Directly call a plot function to display the charged data if option is checked (make a box to tick ?)
    #9. Link add to portfolio button to the portfolio.add() function
    #10. Link remove from portfolio button to the portfolio.remove() function
    #11. Link construct portfolio button to the portfolio.construct_pf() function
    #12. Link free up space button to the get_data.remove() function

#AV : S5D9F26JVZ9GHH29

import sys
import os
import json
import csv
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""
The ultimate module. Create your own portfolio. Here are the main functions that run and rule everything else.

Store, keep and clean data.

Calling new data requires internet connexion. Max 5 API requests per minute and 500 requests per day. More info on https://www.alphavantage.co/documentation/.
...
Methods
----------
boot()
    Tries to use data in cache. If outdated, makes a backup and loads empty dictionnary.
add(name, horizon)
    Add an entry to the portfolio to construct.
remove(name)
    Remove an entry from the portfolio to construct.
construct_pf()
    Constructs the portfolio.
data_store(name, dic)
    Stores new data from API call in a dictionnary.
data_add(name)
    Tries to call new data iif it is not already in storage.
data_remove(name)
    Tries to remove a stock or a crypto from the storage to free up space.
data_show(name)
    Plot data that has been asked or added to the portfolio or data.
data_get(names, horizon, data = pd.DataFrame())
    Construct a portfolio for given stock and cryptos, and a given horizon.
api_stock(name)
    Used for stock and index (ETF). Returns a dictionary of daily data.
api_crypto(name)
    Used for cryptos. Returns a dictionary of daily data.

"""
def boot(self):
    """
    Loads ticker names. Tries to use data in cache. If outdated, makes a backup and loads empty dictionnary.
    """
    with open("stock.json") as f:
        self.stock = json.load(f)
        print("Stock tickers loaded")
    with open("crypto.json") as f:
        self.crypto = json.load(f)
        print("Crypto tickers loaded")
    today = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo").json()["Meta Data"]["3. Last Refreshed"]
    try:
        with open("data.json") as f:
            self.data = json.load(f)
            print("data loaded")
        if not list(self.data[list(self.data.keys())[0]].keys())[0] == today:
            with open("data_backup.json", "w+") as f:
                json.dump(self.data, f)
            os.remove("data.json")
            self.data = dict()
            raise Exception("I made a backup of your data, it is outdated.")
    except:
        print("I tried to open data.json but doesn't exist.")
        pass

def add(self, name, horizon = '2019-05-01'):
    """
    Add an entry to the portfolio to construct.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    horizon : str
        (optional) Indicates the max date of the portfolio. Default is 1st May 2019.
    """
    if horizon not in list(self.pf.keys()):
        self.pf[horizon] = {"stock":list(), "crypto":list()}
    elif name in self.pf[horizon]["stock"] or name in self.pf[horizon]["crypto"]:
        print(name + " already added to portfolio")
        #data_show(self, name)
        return
    if name in self.stock:
        data_add(self, name)
        self.pf[horizon]["stock"].append(name)
        print(name + " added to portfolio")
    elif name in self.crypto:
        data_add(self, name)
        self.pf[horizon]["crypto"].append(name)
        print(name + " added to portfolio")
    return

def remove(self, name):
    """
    Remove an entry from the portfolio to construct.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    """
    self.pf = self.pf.pop(name)
    return

def construct_pf(self):
    """
    Constructs the portfolio.
    """
    horizon = list(self.pf.keys())[-1]
    names = self.pf[horizon]
    data_get(self, names, horizon, self.pfdta)
    return

def data_store(self, name: str, dic: dict):
    """
    Stores new data from API call in a dictionnary.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    dic : dict
        Contains the daily data.
    """
    self.data[name] = dic
    print(name + " added to data successfuly!")
    #autosave
    with open("data.json", "w+") as f:
        json.dump(self.data, f)
        print("Autosave...")
    return

def data_add(self, name: str):
    """
    Tries to call new data iif it is not already in storage.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    """
    if name in self.data:
        print(name + " already added to data")
        #data_show(self, name)
        return
    if name in self.stock:
        try:
            data_store(self, name, api_stock(self, name))
        except:
            print("Wrong API key, check it out!")
        #data_show(self, name)
        return
    if name in self.crypto:
        try:
            data_store(self, name, api_crypto(self, name))
        except:
            print("Wrong API key, check it out!")
        #data_show(self, name)
        return
    print("Wrong name or name type.")
    return

def data_remove(self, name: str):
    """
    Tries to remove a stock or a crypto from the storage to free up space.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    """
    if name not in self.data:
        return
    elif name in self.data:
        self.data.pop(name)
    return

def data_show(self, name: str):
    """
    data_show(name)
        Plot data that has been asked or added to the portfolio or data.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    """
    temp = self.data[name]
    x, y = zip(*temp)
    plt.plot(x, y)
    plt.plot.show()
    return

def data_get(self, names: dict, horizon: str, data: pd.DataFrame = pd.DataFrame()):
    """
    Construct a portfolio with logarithmic returns for given stock and cryptos, and a given horizon.
    ----------
    Parameters
    names : dict
        Contains lists for stock and crypto entries.
    horizon : str
        Starting date of sample.
    data : pd.DataFrame
        (optional) Already transformed data, useful when adding only a few more entry to existing transformed data.
    """
    #The output to send to portfolio class
    send = pd.DataFrame()
    nameslist = names["stock"]+names["crypto"]
    #Check the horizon is feasible for selected data
    horizon_cache = horizon
    for i in nameslist:
        try:
            test = self.data[i][horizon]
        except:
            horizon = list(self.data[i].keys())[-1]
    if not horizon_cache == horizon:
        print("Horizon went from " + horizon_cache + " to " + horizon + " because of selected data")
    #Check the cached data
    if not data.empty:
        #Take the names, and the horizon of cached data
        datanames = list(data.columns)
        datahorizon = data.index[-1]
        #If longer horizon, remove what's beyond
        if datetime.strptime(datahorizon, '%Y-%m-%d') < datetime.strptime(horizon, '%Y-%m-%d'):
            data = data.drop(data.tail(-list(data.index).index(horizon)-1).index)
        #If longer or same horizon, remove useless columns from cache and update nameslist
        #Then, add the reviewed cached data to the send DataFrame
        if datetime.strptime(datahorizon, '%Y-%m-%d') <= datetime.strptime(horizon, '%Y-%m-%d'):
            coldata = data.columns
            data[coldata.intersection(nameslist)]
            nameslist = [i for i in set(nameslist) if i not in coldata]
            send = data
    if not nameslist:
        return send
    #Stock data does not include week-ends, whereas crypto data does
    #Need same dimension if creates a portfolio with both!
    if len(names["stock"]):
        daterestr = list(self.data[names["stock"][0]].keys())
    elif len(names["crypto"]):
        daterestr = list(self.data[names["crypto"][0]].keys())
    #Now, create the DataFrame entry by entry...
    for i in nameslist:
        #First, for each entry of the portfolio, remove everything beyond the horizon of time
        #stock and cryptos have other small difference in their data structure...
        if i in self.stock:
            a = "4. close"
        elif i in self.crypto:
            a = "4a. close (USD)"
        #Here, we make use of our daterestr to not include week-ends when we mix cryptos and stock
        temp = {j:self.data[i][j][a] for j in daterestr if datetime.strptime(j, '%Y-%m-%d') > datetime.strptime(horizon, '%Y-%m-%d')}
        #Now, transform the dictionnary (1 column) into a DataFrame
        temp = pd.DataFrame.from_dict(temp, columns = [i], orient = "index")
        #Append this column to the final DataFrame
        send = pd.concat([send, temp], axis=1)
    send = send.apply(pd.to_numeric)
    self.pfdta = np.log(send/send.shift(1)).iloc[1:]
    return

def api_stock(self, name: str):
    """
    Used for stock and index (ETF). Returns a dictionary of daily data.
    ----------
    Parameters
    name : str
        The stock or index.
    """
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + name + '&outputsize=full&apikey=' + self.key
    return requests.get(url).json()["Time Series (Daily)"]

def api_crypto(self, name: str):
    """
    Used for cryptos. Returns a dictionary of daily data.
    ----------
    Parameters
    name : str
        The crypto.
    """
    url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol='+ name + '&market=USD&apikey=' + self.key
    return requests.get(url).json()["Time Series (Digital Currency Daily)"]
