import sys
import os
import json
import csv
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from qt_core import *

    #1. Ask for API key
    #2. Charge list of possible stocks and cryptos
    #3. Create portfolio object with the two previous imputs
    #4. Propose list of stocks and cryptos
    #5. Create get_data object from portfolio object
    #6. Create api_call object from get_data object
    #7. Link charge button to the get_data.add() function
    #8. Directly call a plot function to display the charged data if option is checked (make a box to tick ?)
    #9. Link add to portfolio button to the portfolio.add() function
    #10. Link remove from portfolio button to the portfolio.remove() function
    #11. Link construct portfolio button to the portfolio.construct_pf() function
    #12. Link free up space button to the get_data.remove() function

#AV : S5D9F26JVZ9GHH29

class portfolio:
    """
    The ultimate parent class. Create your own portfolio. It is the main instance that runs and rules everything else.
    ...
    Attributes
    ----------
    keys : list
        Contains the IEX and the Alphavantage keys as strings for API calls.
    stock : dict
        Stores all the API callable stocks with their ticker and full name.
    crypto : dict
        Stores all the API callable cryptos with their ticker and full name.
    data : dict
        Stores the full data that has been called through API calls in a nested dictionnary.
    pfdta : DataFrame
        Stores the cleaned and trimmed data of the portfolio, ready to be optimised.
    pf : dict
        Stores the name and horizon
    
    Methods
    ----------
    add(name, horizon)
        Add an entry to the portfolio to construct.
    remove(name)
        Remove an entry from the portfolio to construct.
    construct_pf()
        Constructs the portfolio calling its get_data child.
    
    Child
    ----------
    get_data
        Stores, keep and clean data. Constructs portfolios. It calls its api_call child to find further data for the user.
    
    Grand-child
    ----------
    api_call
        Calls new data. Requires internet connexion.
    """
    def __init__(self, key, ot):
        self.key = key
        self.stock = dict()
        self.crypto = dict()
        self.data = dict()
        self.pfdta = pd.DataFrame()
        self.pf = dict()
        try:
            with open("data.json") as f:
                self.data = json.load(f)
        except:
            pass

    def add(self, name, horizon):
        if name in self.pf & self.pf[name] == horizon:
            return
        self.pf = self.pf[name]
        get_data.add(name)
        return
    
    def remove(self, name):
        self.pf = self.pf.pop(name)
        return
    
    def construct_pf(self):
        horizon = list(self.pf.keys())[0]
        names = self.pf['horizon']
        self.pfdta = get_data.get(names, horizon, self.pfdta)
        return

class get_data(portfolio):
    """
    Stores, keep and clean data. Constructs portfolios. It calls the api_call child to find further data for the user.
    ...
    Attributes
    ----------
    See parent class portfolio.
    
    Methods
    ----------
    store(name, dic)
        Stores new data from api_call in a dictionnary.
    add(name)
        Tries to call new data iif it is not already in storage.
    remove(name)
        Tries to remove a stock or a crypto from the storage to free up space.
    get(names, horizon, data = pd.DataFrame())
        Construct a portfolio for given stock and cryptos, and a given horizon.
    
    Child
    ----------
    api_call
        Calls new data. Requires internet connexion.
    """
    def store(self, name: str, dic: dict):
        """
        Stores new data from api_call in a dictionnary.
        ----------
        Parameters
        name : str
            The index (ETF), crypto, or stock.
        dic : dict
            Contains the daily data.
        """
        self.data[name] = dic
        #autosave
        with open("data.json", "w+") as f:
            json.dump(self.data, f)
        return
    
    def add(self, name: str):
        """
        Tries to call new data iif it is not already in storage.
        ----------
        Parameters
        name : str
            The index (ETF), crypto, or stock.
        """
        if name in self.data:
            return
        if name in self.stock:
            try:
                self.store(name, api_call.stock(self, name))
            except:
                print("Wrong API key, check it out!")
            return
        if name in self.crypto:
            try:
                self.store(name, api_call.crypto(self, name))
            except:
                print("Wrong API key, check it out!")
            return
        raise Exception("Wrong name or name type.")
        return
    
    def remove(self, name: str):
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
    
    def get(self, names: dict, horizon: str, data: pd.DataFrame = pd.DataFrame()):
        """
        Construct a portfolio for given stock and cryptos, and a given horizon.
        ----------
        Parameters
        names : dict
            Contains lists for stock and crypto entries.
        horizon : str
            Starting date of sample.
        data : pd.DataFrame
            (optional) Already transformed data, useful when adding only a few more entry to existing transformed data
        """
        #The output to send to portfolio class
        send = pd.DataFrame()
        nameslist = names["stock"]+names["crypto"]
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
            daterestr = list(self.stock[list(self.stock.keys())[0]].keys())
        elif len(names["crypto"]):
            daterestr = list(self.crypto[list(self.crypto.keys())[0]].keys())
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
            send[i] = pd.concat([temp, self.data[i]], axis=1)
        return send
    
    def plot(self, name): ### Mettre dans portfolio évt.
        df = self.data[str(name)]
        col = df.columns
        df.plot(x = col, y = self.data[str(name)])
        plt.show()
        return

class api_call(get_data):
    """
    This class calls new data. Requires internet connexion. Max 5 API requests per minute and 500 requests per day. More info on https://www.alphavantage.co/documentation/.
    ...
    Attributes
    ----------
    See grand-parent class portfolio.
    
    Methods
    ----------
    stock(name)
        Used for stock and index (ETF). Returns a dictionary of daily data.
    crypto(name)
        Used for cryptos. Returns a dictionary of daily data.
    """
    
    def stock(self, name: str):
        """
        Used for stock and index (ETF). Returns a dictionary of daily data.
        ----------
        Parameters
        name : str
            The stock or index.
        """
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + name + '&outputsize=full&apikey=' + self.key
        return requests.get(url).json()["Time Series (Daily)"]
    
    def crypto(self, name: str):
        """
        Used for cryptos. Returns a dictionary of daily data.
        ----------
        Parameters
        name : str
            The crypto.
        """
        url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol='+ name + '&market=USD&apikey=' + self.key
        return requests.get(url).json()["Time Series (Digital Currency Daily)"]

class plot(portfolio):
    def watch_and_store(self):#plot a serie that just got called by the API
        return
    