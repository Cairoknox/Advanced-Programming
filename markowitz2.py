from numba import jit, prange
import numpy as np
import time

def markowitz_init(self):
    #jit does not like pandas dataframes
    assets = len(self.pfdta.columns)
    mean = np.array(self.pfdta.mean())
    covariance = np.array(self.pfdta.cov())
    self.returns, self.volatility, self.sharpe_ratios = markowitz_speedwagon(assets, mean, covariance)

@jit(nopython=True)
def markowitz_speedwagon(assets, mean, covariance):
    business_days = 260
    portfolios = int(9000*np.log(assets))
    returns = np.zeros(portfolios)
    volatility = np.zeros(portfolios)
    sharpe_ratios = np.zeros(portfolios)
    #Generate random portfolios
    for i in prange(portfolios):
        weights = np.random.random(assets)
        weights = weights/np.sum(weights)
        returns[i] = np.sum(business_days*mean*weights)
        volatility[i] = np.sqrt(np.dot(business_days*weights.T, np.dot(covariance, weights)))
        sharpe_ratios[i] = returns[i]/volatility[i]
    return returns, volatility, sharpe_ratios
