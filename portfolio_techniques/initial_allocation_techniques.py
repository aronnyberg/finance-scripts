def min_vol_above(data, jumps, leverage, aboveX): #should be names maxLeverage
    import itertools   
    choices = [i for i in np.linspace(0,leverage,jumps)]
    iters = list(itertools.product(choices, repeat=2))
    returns = []
    sharpes = []
    params = []
    stds = []
    mean_returns = []
    for each in iters:
        try:
            params.append(each)
            rets = each*data
            port_rets = rets.sum(axis=1)
            mean_return = port_rets.mean()
            sharpe = mean_return/port_rets.std()
            sharpes.append(sharpe)
            returns.append(rets)
            stds.append(port_rets.std())
            mean_returns.append(mean_return)
        except:
            pass   
    stds_above_min_return = [stds[over] for over in [n for n,i in enumerate(mean_returns) if i>aboveX]]
    return min(stds_above_min_return), params[stds_above_min_return.index(min(stds_above_min_return))]

def target_vol(data, jumps, leverage, vol_target): #should be names maxLeverage
    import itertools
    choices = [i for i in np.linspace(0,leverage,jumps)]
    iters = list(itertools.product(choices, repeat=2))
    returns = []
    sharpes = []
    params = []
    stds = []
    mean_returns = []
    for each in iters:
        try:
            params.append(each)
            rets = each*data
            port_rets = rets.sum(axis=1)
            mean_return = port_rets.mean()
            sharpe = mean_return/port_rets.std()
            sharpes.append(sharpe)
            returns.append(rets)
            stds.append(port_rets.std())
            mean_returns.append(mean_return)
        except:
            pass 
    whichone = sharpes.index(max(sharpes))
    maxSharpe = max(sharpes)
    maxSharpeWeights = params[whichone]
    leverage = vol_target/(((1+stds[whichone])**np.sqrt(12))-1)
    return mean_returns[whichone], params[whichone], leverage
    
def max_sharpe(data, jumps, leverage):
    import itertools   
    choices = [i for i in np.linspace(0,leverage,jumps)]
    iters = list(itertools.product(choices, repeat=2))
    returns = []
    sharpes = []
    params = []
    for each in iters:
        try:
            params.append(each)
            rets = each*data
            port_rets = rets.sum(axis=1)
            sharpe = port_rets.mean()/port_rets.std()
            sharpes.append(sharpe)
            returns.append(rets)
        except:
            pass    
    return max(sharpes), params[sharpes.index(max(sharpes))]
    
#min_vol_above(df2.tail(240), 25, 2, ann7pc)
def moving_allocation(MVOorMSorTV, data, days, ndays, rollingYorN, searchN, leverage, annReturn, vol_target):
    
    X = data
    n_train = days*ndays   
    n_records = len(X)
    weight_list = []
    returns_list = []
    date_list = []
    leverage_list = []
    #Recomputes Markowitz weights based on all data up to that date
    for i in range(n_train, n_records, days):
        date = X.index.values[i]
        if rollingYorN == 'Y':
            train = X[i-n_train:i] #Moving window of train period 
        else:
            train = X[0:i] #Uses all data as training data
        if MVOorMSorTV == 'MVO':
            try:
                monthly_minimum = (annReturn**(1/12))-1
                weight_list.append(min_vol_above(train, searchN, leverage, monthly_minimum)[1])
            except:
                try:
                    weight_list.append(weight_list[-1])
                except:
                    weight_list.append((0.5, 0.5))
        if MVOorMSorTV == 'MS':
            try:
                weight_list.append(max_sharpe(train, searchN, leverage)[1])
            except:
                try:
                    weight_list.append(weight_list[-1])
                except:
                    weight_list.append((0.5, 0.5))
        if MVOorMSorTV == 'TV':
            try:   
                allparams = target_vol(train, searchN, leverage, vol_target)
                weight_list.append((allparams[1][0]*allparams[2], allparams[1][1]*allparams[2])) #weights*leverage
            except:
                try:
                    weight_list.append(weight_list[-1])
                except:
                    weight_list.append((0.5, 0.5))
            
            

        else:
            print('Specify the model, dumbass')            
                
        returns = sum(sum(np.array(X[i:i+days])*weight_list[-1]))
        returns_list.append(returns) 
        date_list.append(date)
    return pd.DataFrame({'Date':date_list, 'Returns':returns_list, 'Weights':weight_list}).set_index('Date')
