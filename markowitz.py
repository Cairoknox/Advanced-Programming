import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def markowitz(self):
    np.random.seed(42)
    num_ports = 6000
    num_asset = len(self.pfdta.columns)
    all_weights = np.zeros((num_ports, num_asset))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)
    

    for x in range(num_ports):
        weights = np.array(np.random.random(num_asset))
        weights = weights/np.sum(weights)
        all_weights[x,:] = weights

        ret_arr[x] = np.sum((self.pfdta.mean()*weights*252))
        vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(self.pfdta.cov()*252, weights)))

        sharpe_arr[x] = ret_arr[x]/vol_arr[x]

    max_sr_ret = ret_arr[sharpe_arr.argmax()]
    max_sr_vol = vol_arr[sharpe_arr.argmax()]
    
    #constraints = ({'type': 'eq', 'fun':check_sum})
    #bounds = ((0, 1), (0, 1), (0, 1), (0, 1))
    #init_guess = [0.25, 0.25, 0.25, 0.25]

    #opt_results = minimize(neg_sharpe, init_guess, method = 'SLSQP', bounds = bounds, constraints = constraints)
    #print(opt_results)

    #get_ret_vol_sr(opt_results.x)
    #frontier_y = np.linspace(0, 0.3, 200)

    #frontier_x = []

    #for possible_return in frontier_y:
    #    constraints = ({'type':'eq', 'fun':check_sum}, {'type':'eq', 'fun': lambda w: get_ret_vol_sr(w)[0] - possible_return})
    #    
    #    result = minimize(minimize_volatility,init_guess,method='SLSQP', bounds=bounds, constraints=constraints)
    #    frontier_x.append(result['fun'])


    plt.figure(figsize=(12,8))
    plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.scatter(max_sr_vol, max_sr_ret,c='red', s=50)
    #plt.plot(frontier_x, frontier_y, 'r--', linewidth=3)
    plt.show()

def get_ret_vol_sr(weights):
    weights = np.array(weights)
    ret = np.sum(log_ret.mean()*weights)*252
    vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
    sr = ret/vol
    return np.array([ret, vol, sr])

def neg_sharpe(weights):
    return get_ret_vol_sr(weights)[2]*(-1)

def check_sum(weights):
    return np.sum(weights)-1

def minimize_volatility(weights):
    return get_ret_vol_sr(weights)[1]
