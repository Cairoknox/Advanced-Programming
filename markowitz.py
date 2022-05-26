from numba import jit, prange
import numpy as np
from scipy.optimize import minimize

def markowitz_init(self):
    #jit does not like pandas dataframes
    assets = len(self.pfdta.columns)
    mean = np.array(self.pfdta.mean())
    covariance = np.array(self.pfdta.cov())
    self.returns, self.volatility, self.weight, a, b, self.sharpe_ratios = markowitz_speedwagon(assets, mean, covariance)
    self.optim = [a, b]
    self.returns2 = np.linspace(0, self.returns[np.argmax(self.returns)]*(1+assets/100), 100)
    self.volatility2, self.weight2, a, b = markowitz_turtle(assets, mean, covariance, self.returns2)
    self.optim2 = [a, b]

@jit(nopython=True)
def markowitz_speedwagon(assets, mean, covariance):
    business_days = 260
    portfolios = int(9000*np.log(assets))
    returns = np.zeros(portfolios)
    volatility = np.zeros(portfolios)
    sharpe_ratios = np.zeros(portfolios)
    maxsr = 0
    #Generate random portfolios
    for i in prange(portfolios):
        weight = np.random.random(assets)
        weight = weight/np.sum(weight)
        returns[i] = np.sum(business_days*mean*weight)
        volatility[i] = np.sqrt(np.dot(business_days*weight.T, np.dot(covariance, weight)))
        sharpe_ratios[i] = returns[i]/volatility[i]
        if sharpe_ratios[i] > maxsr:
            maxsr = sharpe_ratios[i]
            maxw = weight
            maxr = returns[i]
            maxv = volatility[i]
    return returns, volatility, maxw, maxv, maxr, sharpe_ratios

def markowitz_turtle(assets, mean, covariance, mus):
    def markowitz_objective(weights):
        return np.dot(business_days*weights.T, np.dot(covariance, weights))
    def constraint1(weights):
        return np.sum(weights)-1
    def constraint2(weights):
        return np.sum(business_days*mean*weights)
    def sharpe_objective(weights):
        return np.sum(business_days*mean*weights)/np.dot(business_days*weights.T, np.dot(covariance, weights))
    business_days = 260
    bounds = []
    for i in range(assets):
        bounds.append((0, 1))
    bounds = tuple(bounds)
    volatility = []
    for i in mus:
        weights = np.random.random(assets)
        constraints = ({'type' : 'eq', 'fun' : lambda weights : constraint1(weights)},
        {'type' : 'eq', 'fun' : lambda weights : constraint2(weights) - i})
        volatility.append(np.sqrt(minimize(markowitz_objective, weights, method = 'SLSQP', constraints = constraints, bounds = bounds)['fun']))
    maxw = minimize(sharpe_objective, weights, method = 'SLSQP', bounds = bounds, constraints = constraints).x
    maxr = constraint2(maxw)
    maxv = np.sqrt(markowitz_objective(maxw))
    return volatility, maxw, maxv, maxr


# def get_ret_vol_sr(weights, self):
#     weights = np.array(weights)
#     ret = np.sum((self.pfdta.mean()*weights))*252
#     vol = np.sqrt(np.dot(weights.T, np.dot(self.pfdta.cov()*252, weights)))
#     sr = ret/vol
#     return np.array([ret, vol, sr])

# def neg_sharpe(weights, self):
#     return get_ret_vol_sr(weights, self)[2]*(-1)