"""
This is an optimization module. Simply calling the init method with at least two columns of data in a self.pfdta dataframe in log returns will satisfy the autopilot.
...
Methods
----------
markowitz_init()
    Creates a few variable based on the self.pfdta dataframe. This is a necessary preliminary step because markowitz_speedwagon does not understand dataframes. It directly runs markowitz_speedwagon() and markowitz_turtle().
markowitz_speedwagon(assets, mean, covariance)
    Runs a simple Monte-Carlo simulation and also extracts the highest Sharpe ratio out of it. It tries to be fast!
markowitz_turtle(assets, mean, covariance, mus)
    Runs a first non-linear optimization to estimate the efficient frontier, and a second one to estimate the best portfolio according to the Sharpe ratio measure. The name of the function is a bit misleading, it is not that slow.
"""
#Copyright (c) 2022 Raphaël Radzuweit

import numpy as np #Necessary for the whole module

import pandas #Necessary to handle the dataframe in markowitz_init(). However, it is never called explicitly
from numba import jit, prange #Necessary for markowitz_speedwagon()
from scipy.optimize import minimize #Necessary for markowitz_turtle()

def markowitz_init(self):
    """
    Creates a few variable based on the self.pfdta dataframe. This is a necessary preliminary step because markowitz_speedwagon does not understand dataframes. It directly runs markowitz_speedwagon() and markowitz_turtle().
    """
    assets = len(self.pfdta.columns) #Number of assets
    mean = np.array(self.pfdta.mean()) #Mean return of each asset
    covariance = np.array(self.pfdta.cov()) #Variance-covariance matrix between assets
    ##Monte-Carlo##
    self.returns, self.volatility, self.weight, a, b, self.sharpe_ratios = markowitz_speedwagon(assets, mean, covariance) #Run and save output of markowitz_speedwagon
    self.optim = [a, b] #Saving the volatility and return of the efficient portfolio
    ##Non-linear optimization##
    self.returns2 = np.linspace(0, self.returns[np.argmax(self.returns)]*(1+assets/100), 100) #Creates a vector of target returns from 0 to a bit over the max return found by Monte-Carlo
    self.volatility2, self.weight2, a, b = markowitz_turtle(assets, mean, covariance, self.returns2) #Run and save output of markowitz_turtle
    self.optim2 = [a, b] #Saving the volatility and return of the efficient portfolio
    return

@jit(nopython=True)
def markowitz_speedwagon(assets: int, mean: np.ndarray, covariance: np.ndarray):
    """
    Runs a simple Monte-Carlo simulation and also extracts the highest Sharpe ratio out of it. It tries to be fast!
    ----------
    Parameters
    assets : int
        The total number of assets.
    mean : np.ndarray
        A 1-d np.array containing the returns of each asset.
    covariance : np.ndarray
        A 2-d np.array containg the variance of each asset on the main diagonal, and the covariance between assets on the upper and lower parts.
    """
    business_days = 260 #For annualizing the returns
    portfolios = int(9000*np.log(assets)) #Number of simulations
    returns = np.zeros(portfolios) # Empty vector of zeros
    volatility = np.zeros(portfolios) # Empty vector of zeros
    sharpe_ratios = np.zeros(portfolios) # Empty vector of zeros
    maxsr = 0 # Initialize the maximum Sharpe ratio
    ##Start of the simulation##
    for i in prange(portfolios): #For each portfolio
        weight = np.random.random(assets) #Generate random weight vector
        weight = weight/np.sum(weight) #Normalize the weights to 1
        returns[i] = np.sum(business_days*mean*weight) #Calculate the return of the portfolio with such weights
        volatility[i] = np.sqrt(np.dot(business_days*weight.T, np.dot(covariance, weight))) #Calculate the volatility of the portfolio with such weights
        sharpe_ratios[i] = returns[i]/volatility[i] #Calculate the Sharpe ratio
        if sharpe_ratios[i] > maxsr: #Is the Sharpe ratio of this portfolio greater than previous portfolios ? If it is the case...
            maxsr = sharpe_ratios[i] #Save the new max Sharpe ratio
            maxw = weight #Save the weight vector to display it in the app
            maxr = returns[i] #Save the return for plotting
            maxv = volatility[i] #Save the volatility for plotting
    ##End of the simulation##
    return returns, volatility, maxw, maxv, maxr, sharpe_ratios

def markowitz_turtle(assets: int, mean: np.ndarray, covariance: np.ndarray, mus: np.ndarray):
    """
    Runs a first non-linear optimization to estimate the efficient frontier, and a second one to estimate the best portfolio according to the Sharpe ratio measure. The name of the function is a bit misleading, it is not that slow.
    ----------
    Parameters
    assets : int
        The total number of assets.
    mean : np.ndarray
        A 1-d np.ndarray containing the returns of each asset.
    covariance : np.ndarray
        A 2-d np.ndarray containg the variance of each asset on the main diagonal, and the covariance between assets on the upper and lower parts.
    mus : np.ndarray
        A 1-d np.ndarray with objective returns for the efficient frontier estimation.
    """
    business_days = 260 #For annualizing the returns
    ##Objective functions##
    def markowitz_objective(weights): #The objective for the efficient frontier estimation
        return np.dot(business_days*weights.T, np.dot(covariance, weights)) #Covariance matrix
    def sharpe_objective(weights): #The objective for the efficient portfolio estimation
        return -np.sum(business_days*mean*weights)/np.dot(business_days*weights.T, np.dot(covariance, weights)) #Negative Sharpe ratio
    ##Constraints##
    def constraint1(weights): #The first constraint for both optimizations
        return np.sum(weights)-1 #The sum of weights must be 1
    def constraint2(weights): #The second constraint for the efficient frontier estimation
        return np.sum(business_days*mean*weights) #The return of the portfolio must be non-negative
    ##Bounds##
    bounds = [] #Initialize a list of bounds
    for i in range(assets): #For the number of assets
        bounds.append((0, 1)) #Generate a tuple of min and max bounds for the weights. They cannot be something else than 1
    bounds = tuple(bounds) #Now, transform the list of tuple to a tuple of tuple
    ##Start of efficent frontier optimization##
    volatility = [] #Initialize a list of volatility
    for i in mus: #For each target return
        weights = np.random.random(assets) #Initial weight for optimization. They do not really matter, they are just a starting point for the SLSQP method
        constraints = ({'type' : 'eq', 'fun' : lambda weights : constraint1(weights)},
        {'type' : 'eq', 'fun' : lambda weights : constraint2(weights) - i}) #The set of constraints as explicited before
        volatility.append(np.sqrt(minimize(markowitz_objective, weights, method = 'SLSQP', constraints = constraints, bounds = bounds)['fun'])) #Add the optimal volatility reached to the volatility list
    ##End of efficent frontier optimization##
    ##Start of efficient portfolio optimization##
    constraints = ({'type' : 'eq', 'fun' : lambda weights : constraint1(weights)}) #The constraint as explicited before
    maxw = minimize(sharpe_objective, weights, method = 'SLSQP', bounds = bounds, constraints = constraints).x #Save the weighting of the maximal Sharpe ratio achieved
    maxr = constraint2(maxw) #With the weight we get the return
    maxv = np.sqrt(markowitz_objective(maxw)) #With the weight we get the volatility
    ##End of efficient portfolio optimization##
    return volatility, maxw, maxv, maxr
