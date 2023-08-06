import pandas as pd
import math as m
import logging
def topsis(path, weight, impact, out_name):
    
    try:
        data = pd.read_csv(path)
    except FileNotFoundError:
        logging.error("Invalid file or path")
        return
    
    rows = len(data.axes[0])
    cols = len(data.axes[1])

    if(sum(data.isnull().sum())!=0):
        logging.error("There are NULL values in dataset")
        return

    if(cols<3):
        logging.error("Must be 3 or more columns")
        return
    try:
        weights = [int(e) for e in weight.split(',')]
    except:
        loggin.error("Input weights in the format 'w1,w2....,wn'")
        return 
    if(len(weights)!=cols-1):
        logging.error("Weights are not equal to number of instances")
        return 
    try:    
        impacts = impact.split(',')
    except:
        logging.error("Impacts are not in proper format")
        return
    if(len(impacts)!=cols-1):
        logging.error("Impacts are not equal to number of instances")
        return
    for i in impacts:
        if i!='+' and i!='-':
            logging.error("Incompatible imapct values entered")
    
    df = pd.DataFrame.copy(data, deep=True)
    

    for i in range(1,cols):
        df.iloc[:,i] *= weights[i-1]

    best = []
    worst = []
    for i in range(1,cols):
        if impacts[i-1]=='+':
            best.append(max(df.iloc[:,i]))
            worst.append(min(df.iloc[:,i]))
        if impacts[i-1]=='-':
            best.append(min(df.iloc[:,i]))
            worst.append(max(df.iloc[:,i]))

    d_best=[]
    d_worst=[]
    for i in range(rows):
        d_best.append(m.dist(df.iloc[i,1:],best))
        d_worst.append(m.dist(df.iloc[i,1:],worst))
    
    topsis = []
    for i in range(rows):
        topsis.append((d_worst[i])/(d_best[i]+d_worst[i]))

    data["Topsis Score"] = topsis
    data['Rank'] = (data['Topsis Score'].rank(method='max', ascending=False))
    data = data.astype({"Rank": int})
    for i in range(1,rows):
        data.iloc[:,i] = round(data.iloc[:,i],3) 
    data.to_csv(r'%s' %out_name, index=False, header=True)