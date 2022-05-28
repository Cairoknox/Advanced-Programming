"""
This is a data processing module for the portfolio.

Store, keep and clean data.

Calling new data requires internet connexion.

For Alpha Vantage (AV), max 5 API requests per minute and 500 requests per day. More info on https://www.alphavantage.co/documentation/.

For ESG Enterprise (ESGE), max 50 API requests per day. More info on https://www.esgenterprise.com/docs/api-reference/.
...
Methods
----------
boot()
    Loads names of supported stocks and cryptos. Tries to use AV and ESGE data in cache. If AV is outdated, makes a backup and loads empty dictionnary.
add(name)
    Add an entry to the portfolio to construct.
remove(name)
    Remove an entry from the portfolio of the user.
data_add(name)
    Try to call new data iif it is not already in storage.
data_store(name, dic)
    Store new data from API call in a dictionnary.
esg_add(name, dic)
    Try to call new ESG data iif it is not already in storage.
esg_store(name, dic)
    Store new ESG data from API call in a dictionnary.
construct_pf()
    Constructs the portfolio. Namely, properly call data_get().
data_get(names, data = pd.DataFrame())
    Construct a portfolio with logarithmic returns for given stock and cryptos, and a given horizon.
api_stock(name)
    Returns a dictionary of daily stock data through an AV API call.
api_crypto(name)
    Returns a dictionary of daily crypto data through an AV API call.
api_esg(name)
    Returns a dictionnary of ESG data for a given company through an ESGE API call.
"""
#Copyright (c) 2022 Raphaël Radzuweit

import os
import json
import requests
from datetime import datetime
import pandas as pd
import numpy as np

def boot(self):
    """
    Loads names of supported stocks and cryptos. Tries to use AV and ESGE data in cache. If AV is outdated, makes a backup and loads empty dictionnary.
    """
    ##Load names##
    with open("stock.json") as f: #Open stock.json
        self.stock = json.load(f) #Load data
        print("Stock tickers loaded") #Giving a sign of life to the terminal
    with open("crypto.json") as f: #Open crypto.json
        self.crypto = json.load(f) #Load data
        print("Crypto tickers loaded") #Giving a sign of life to the terminal
    ##Check AV data in cache##
    try: #Try the following, if there is an impossibility, jumps to the except block
        with open("data.json") as f: #Open data.json
            self.data = json.load(f) #Load data
            print("data loaded") #Giving a sign of life to the terminal
        if not list(self.data[list(self.data.keys())[0]].keys())[0] == self.today: #Is the first date of the loaded data equal to the latest trading day. If not...
            with open("data_backup.json", "w+") as f: #Open data_backup.json in write mode
                json.dump(self.data, f) #Dump data
            os.remove("data.json") #Empty data.json
            self.data = dict() #Unload data
            print("I made a backup of your data, it was outdated") #Giving a sign of life to the terminal
    except: #If something went wrong in the try block, most likely there was no data.json file
        print("I tried to open data.json but doesn't exist") #Giving a sign of life to the terminal
        pass
    ##Check ESGE data in cache##
    try: #Try the following, if there is an impossibility, jumps to the except block
        with open("esg.json") as f: #Open esg.json
            self.esg = json.load(f) #Load data
            print("ESG data loaded") #Giving a sign of life to the terminal
    except: #If something went wrong in the try block, most likely there was no esg.json file
        print("I tried to open esg.json but it doesn't exist") #Giving a sign of life to the terminal
        pass
    return

def add(self, name: str):
    """
    Add an entry to the portfolio of the user.
    ----------
    Parameters
    name : str
        The stock or crypto ticker.
    """
    if self.horizon not in list(self.pf.keys()): #Is there a portfolio for the current horizon (the current version does not handle multiple portfolios for different horizon) ? If yes...
        self.pf[self.horizon] = {"stock":list(), "crypto":list()} #Create a structure that accepts a list of crypto and a list of stock tickers.
    elif name in self.pf[self.horizon]["stock"] or name in self.pf[self.horizon]["crypto"]: #If no... is the crypto or stock ticker already in the portfolio ? If yes...
        print(name + " already added to portfolio") #Giving a sign of life to the terminal
        return 0 #This value is used to prevent the table adding a new line for the not added ticker
    if name in self.stock: #Is the ticker a stock? If yes...
        success = data_add(self, name) #Ask the corresponding data
        if success == 0: #If the API key is not valid, the data could not be fetched
            return 0 #This value is used to prevent the table adding a new line for the not added ticker
        self.pf[self.horizon]["stock"].append(name) #Add the ticker to the portfolio
        print(name + " added to portfolio") #Giving a sign of life to the terminal
        return 1 #This value is used to add a new line to the table
    elif name in self.crypto: #If no... is the ticker a crypto? If yes...
        success = data_add(self, name) #Ask the corresponding data
        if success == 0: #If the API key is not valid, the data could not be fetched
            return 0 #This value is used to prevent the table adding a new line for the not added ticker
        self.pf[self.horizon]["crypto"].append(name) #Add the ticker to the portfolio
        print(name + " added to portfolio") #Giving a sign of life to the terminal
        return 1 #This value is used to add a new line to the table
    return 0 #This value is used to prevent the table adding a new line for the not added ticker

def remove(self, name: str):
    """
    Remove an entry from the portfolio of the user.
    ----------
    Parameters
    name : str
        The stock or crypto ticker.
    """
    if name in self.stock: #Is the ticker a stock? If yes...
        self.pf[self.horizon]["stock"].remove(name) #Remove the ticker from the portfolio
    elif name in self.crypto: #If no... is the ticker a crypto? If yes...
        self.pf[self.horizon]["crypto"].remove(name) #Remove the ticker from the portfolio
    return

def data_add(self, name: str):
    """
    Try to call new data iif it is not already in storage.
    ----------
    Parameters
    name : str
        The stock or crypto ticker.
    """
    if name in self.data: #Is the data of the ticker already loaded? If yes...
        print(name + " already added to data") #Giving a sign of life to the terminal
        return 1 #This value is used to say that the data is there
    if name in self.stock: #Is the ticker a stock? If yes...
        try: #Try the following, if there is an impossibility, jumps to the except block
            data_store(self, name, api_stock(self, name)) #Call and store data
            return 1 #This value is used to say that the data is there
        except: #If something went wrong in the try block, most likely the API key is not right
            print("Wrong API key, check it out!") #Giving a sign of life to the terminal
            return 0 #This value is used to say that the data is not there
    if name in self.crypto: #Is the ticker a crypto? If yes...
        try: #Try the following, if there is an impossibility, jumps to the except block
            data_store(self, name, api_crypto(self, name)) #Call and store data
            return 1 #This value is used to say that the data is there
        except: #If something went wrong in the try block, most likely the API key is not right
            print("Wrong API key, check it out!") #Giving a sign of life to the terminal
            return 0 #This value is used to say that the data is not there
    print("Wrong name or name type.") #If nothing of the previous worked, giving a sign of life to the terminal
    return 0 #This value is used to say that the data is not there

def data_store(self, name: str, dic: dict):
    """
    Store new data from API call in a dictionnary.
    ----------
    Parameters
    name : str
        The index (ETF), crypto, or stock.
    dic : dict
        Contains the daily data.
    """
    self.data[name] = dic #This data most likely comes from the API call
    print(name + " added to data successfuly!") #Giving a sign of life to the terminal
    with open("data.json", "w+") as f: #Open data.json in write mode
        json.dump(self.data, f) #Save dataset with the newly fetched data
        print("Autosave...") #Giving a sign of life to the terminal
    return

def esg_add(self, name: str):
    """
    Try to call new ESG data iif it is not already in storage.
    ----------
    Parameters
    name : str
        The index (ETF) or stock.
    """
    if name in self.esg: #Is the data of the ticker already loaded? If yes...
        print(name + " already added to esg data") #Giving a sign of life to the terminal
        return
    if name in self.stock: #Is the ticker a stock? If yes...
        try: #Try the following, if there is an impossibility, jumps to the except block
            esg_store(self, name, api_esg(self, name)) #Call and store data
            return
        except: #If something went wrong in the try block, most likely the API key is not right
            print("Wrong esg API key, check it out!") #Giving a sign of life to the terminal
            pass
    return

def esg_store(self, name: str, dic: dict):
    """
    Store new ESG data from API call in a dictionnary.
    ----------
    Parameters
    name : str
        The stock or crypto ticker.
    dic : dict
        Contains the daily data.
    """
    self.esg[name] = dic #This data most likely comes from the API call
    print(name + " added to esg data successfuly!") #Giving a sign of life to the terminal
    with open("esg.json", "w+") as f: #Open esg.json in write mode
        json.dump(self.esg, f) #Save dataset with the newly fetched data
        print("Autosave ESG...") #Giving a sign of life to the terminal
    return

def construct_pf(self):
    """
    Constructs the portfolio. Namely, properly call data_get().
    """
    self.horizondyn = list(self.pf.keys())[-1] #Access by default the portfolio of the last horizon (the current version does not handle multiple portfolios for different horizon)
    names = self.pf[self.horizondyn] #Load the names of stock and crypto tickers
    data_get(self, names, self.pfdta) #Call data_get()
    return

def data_get(self, names: dict, data: pd.DataFrame = pd.DataFrame()):
    """
    Construct a portfolio with logarithmic returns for given stock and cryptos, and a given horizon.
    ----------
    Parameters
    names : dict
        Lists for stock and crypto entries.
    data : pd.DataFrame
        (optional) Already transformed data, useful when adding only a few more entry to existing transformed data.
    """
    send = pd.DataFrame() #Initialize a dataframe that will be filled with the processed data
    nameslist = names["stock"]+names["crypto"] #Initialize a full list of stock and cryptos
    ##Check if the horizon is reachable##
    horizon_cache = self.horizondyn #Stock current horizon for reference
    for i in nameslist: #For each ticker
        try: #Try the following, if there is an impossibility, jumps to the except block
            test = self.data[i][self.horizondyn] #Access each ticker at given max horizon
        except: #If something went wrong in the try block, most likely the max horizon is too far
            self.horizondyn = list(self.data[i].keys())[-1] #Diminish the horizon to the max horizon of the ticker
    if not horizon_cache == self.horizondyn: #Has the horizon changed from reference? If yes...
        print("horizon went from " + horizon_cache + " to " + self.horizondyn + " because of selected data") #Giving a sign of life to the terminal
    ##Check the initial dataframe## (the current version does not check if a portfolio was previously processed, the following block never runs)
    if not data.empty: #Is there data in the dataframe? If yes...
        datahorizon = data.index[-1] #Take the horizon of data in dataframe
        if datetime.strptime(datahorizon, '%Y-%m-%d') <= datetime.strptime(self.horizondyn, '%Y-%m-%d'): #Is the horizon longer or equal in dataframe than what is achievable? If yes...
            data = data.drop(data.tail(-list(data.index).index(self.horizondyn)-1).index) #Remove useless rows from dataframe
            coldata = data.columns #Load tickers that are present in dataframe
            data[coldata.intersection(nameslist)] #Remove tickers that are no more in portfolio
            nameslist = [i for i in set(nameslist) if i not in coldata] #Update nameslist to remove already added tickers
            send = data #Fill the already process data in the send DataFrame
    ##Process the remaining data##
    if nameslist: #Is there anything left in nameslist? If yes...
        if len(names["stock"]): #Are there stock tickers? If yes...
            daterestr = list(self.data[names["stock"][0]].keys()) #We get a vector of date (they do not include weekends)
        elif len(names["crypto"]): #If no... are there crypto tickers? If yes...
            daterestr = list(self.data[names["crypto"][0]].keys()) #We get a vector of date (they include weekends)
        for i in nameslist: #For each ticker
            #First, for each entry of the portfolio, remove everything beyond the horizon of time
            #stock and cryptos have other small difference in their data structure...
            if i in self.stock: #Is the ticker a stock? If yes...
                a = "4. close" #Get the closing quote
            elif i in self.crypto: #If no... is the ticker a crypto? If yes...
                a = "4a. close (USD)" #Get the closing quote
            temp = {j:self.data[i][j][a] for j in daterestr if datetime.strptime(j, '%Y-%m-%d') > datetime.strptime(self.horizondyn, '%Y-%m-%d')} #Use of our daterestr to not include weekends if mix of stock and crypto tickers
            temp = pd.DataFrame.from_dict(temp, columns = [i], orient = "index") #Transform the dictionnary into a DataFrame column
            send = pd.concat([send, temp], axis=1) #Append to the send DataFrame
    send = send.apply(pd.to_numeric) #Convert the dataframe items to numeric values
    self.pfdta = np.log(send/send.shift(1)).iloc[1:] #Calculate log returns and save them as pfdta
    return

def api_stock(self, name: str):
    """
    Returns a dictionary of daily stock data through an AV API call.
    ----------
    Parameters
    name : str
        The stock ticker.
    """
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + name + '&outputsize=full&apikey=' + self.key #URL to make the API call
    return requests.get(url).json()["Time Series (Daily)"] #Make the actual request and precise the .json format which translates into a dictionnary

def api_crypto(self, name: str):
    """
    Returns a dictionary of daily crypto data through an AV API call.
    ----------
    Parameters
    name : str
        The crypto ticker.
    """
    url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol='+ name + '&market=USD&apikey=' + self.key #URL to make the API call
    return requests.get(url).json()["Time Series (Digital Currency Daily)"] #Make the actual request and precise the .json format which translates into a dictionnary

def api_esg(self, name: str):
    """
    Returns a dictionnary of ESG data for a given company through an ESGE API call.
    ----------
    Parameters
    name : str
        The stock ticker.
    """
    url = 'https://tf689y3hbj.execute-api.us-east-1.amazonaws.com/prod/authorization/search?q=' + self.stock[name] + '&token=' + self.keyesg #URL to make the API call
    req = requests.get(url).json()[0] #Make the actual request and precise the .json format which translates into a dictionnary
    return {key:req.get(key) for key in ['total_grade', 'total', 'last_processing_date']} #Only keep the data of interest
