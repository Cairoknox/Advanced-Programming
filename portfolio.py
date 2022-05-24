
    #10. Link remove from portfolio button to the portfolio.remove() function
    #12. Link free up space button to the get_data.remove() function

#AV : S5D9F26JVZ9GHH29

import os
import json
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
add(name)
    Add an entry to the portfolio to construct.
remove(name)
    Remove an entry from the portfolio to construct.
construct_pf()
    Constructs the portfolio.
data_store(name, dic)
    Stores new data from API call in a dictionnary.
data_add(name)
    Tries to call new data iif it is not already in storage.
data_show(name)
    Plot data that has been asked or added to the portfolio or data.
data_get(names, data = pd.DataFrame())
    Construct a portfolio for given stock and cryptos.
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
    try:
        with open("data.json") as f:
            self.data = json.load(f)
            print("data loaded")
        if not list(self.data[list(self.data.keys())[0]].keys())[0] == self.today:
            with open("data_backup.json", "w+") as f:
                json.dump(self.data, f)
            os.remove("data.json")
            self.data = dict()
            raise Exception("I made a backup of your data, it is outdated.")
    except:
        print("I tried to open data.json but doesn't exist.")
        pass

def add(self, name):
    """
    Add an entry to the portfolio to construct.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    """
    if self.horizon not in list(self.pf.keys()):
        self.pf[self.horizon] = {"stock":list(), "crypto":list()}
    elif name in self.pf[self.horizon]["stock"] or name in self.pf[self.horizon]["crypto"]:
        print(name + " already added to portfolio")
        return 0
    if name in self.stock:
        success = data_add(self, name)
        if success == 0:
            return 0
        self.pf[self.horizon]["stock"].append(name)
        print(name + " added to portfolio")
        return 1
    elif name in self.crypto:
        success = data_add(self, name)
        if success == 0:
            return 0
        self.pf[self.horizon]["crypto"].append(name)
        print(name + " added to portfolio")
        return 1
    return 0

def remove(self, name):
    """
    Remove an entry from the portfolio to construct.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    """
    if name in self.stock:
        self.pf[self.horizon]["stock"].remove(name)
    elif name in self.crypto:
        self.pf[self.horizon]["crypto"].remove(name)
    return

def construct_pf(self):
    """
    Constructs the portfolio.
    """
    self.horizondyn = list(self.pf.keys())[-1]
    names = self.pf[self.horizondyn]
    data_get(self, names, self.pfdta)
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
        return 1
    if name in self.stock:
        try:
            data_store(self, name, api_stock(self, name))
            return 1
        except:
            print("Wrong API key, check it out!")
            return 0
    if name in self.crypto:
        try:
            data_store(self, name, api_crypto(self, name))
            return 1
        except:
            print("Wrong API key, check it out!")
            return 0
    print("Wrong name or name type.")
    return 0

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

def data_get(self, names: dict, data: pd.DataFrame = pd.DataFrame()):
    """
    Construct a portfolio with logarithmic returns for given stock and cryptos, and a given horizon.
    ----------
    Parameters
    names : dict
        Contains lists for stock and crypto entries.
    data : pd.DataFrame
        (optional) Already transformed data, useful when adding only a few more entry to existing transformed data.
    """
    #The output to send to portfolio class
    send = pd.DataFrame()
    nameslist = names["stock"]+names["crypto"]
    #Check the horizon is feasible for selected data
    horizon_cache = self.horizondyn
    for i in nameslist:
        try:
            test = self.data[i][self.horizondyn]
        except:
            self.horizondyn = list(self.data[i].keys())[-1]
    if not horizon_cache == self.horizondyn:
        print("horizon went from " + horizon_cache + " to " + self.horizondyn + " because of selected data")
    #Check the cached data
    if not data.empty:
        #Take the names, and the horizon of cached data
        datanames = list(data.columns)
        datahorizon = data.index[-1]
        #If longer horizon, remove what's beyond
        if datetime.strptime(datahorizon, '%Y-%m-%d') < datetime.strptime(self.horizondyn, '%Y-%m-%d'):
            data = data.drop(data.tail(-list(data.index).index(self.horizondyn)-1).index)
        #If longer or same horizon, remove useless columns from cache and update nameslist
        #Then, add the reviewed cached data to the send DataFrame
        if datetime.strptime(datahorizon, '%Y-%m-%d') <= datetime.strptime(self.horizondyn, '%Y-%m-%d'):
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
        temp = {j:self.data[i][j][a] for j in daterestr if datetime.strptime(j, '%Y-%m-%d') > datetime.strptime(self.horizondyn, '%Y-%m-%d')}
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
