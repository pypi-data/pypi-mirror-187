# A package to generate topsis score and rank 
# By -: Navreen Waraich

import numpy as np
import pandas as pd

def num(dataset):
    aa = 'int32 int64 float32 float64'.split()
    dtype = dataset.dtypes.tolist()
    ind_num = []
    for ind,i in enumerate(dtype):
        if i in aa:
            ind_num.append(ind)

    col_list = dataset.columns.tolist()
    non_num_col_list = [col_list[i] for i in ind_num]

    return non_num_col_list


def wi(ds_col_len, weights, impacts):
    x = len(weights)
    y = len(impacts)
    z = ds_col_len
    if x != y or y != z or z != x:
        raise Exception("Number of weights, impacts and dataset columns are not same.")

    a_impact = '+ -'.split()
    for i in impacts:
        if i not in a_impact:
            raise Exception("Impact element(s) are not +/-")

def norm(ds,weights):
    for i in range(ds.shape[1]):
        total_sqsum = 0
        
        for j in list(ds.iloc[:,i]):
            total_sqsum += j**2
        denom = total_sqsum**0.5
        
        for ind,z in enumerate(list(ds.iloc[:,i])):
            ds.iloc[ind,i] = z*weights[i]/denom

def ideal(ds,imp):
    best = []
    worst = []
    
    for i in range(ds.shape[1]):
        if imp[i] == '+':
            best.append(ds.max()[i])
            worst.append(ds.min()[i])
        else:
            best.append(ds.min()[i])
            worst.append(ds.max()[i])
            
    return best,worst

def score(ds,ibest,iworst):
    pos = []
    neg = []
    for i in range(ds.shape[0]):
            pos.append(np.linalg.norm(ds.iloc[i,:].values-ibest))
            neg.append(np.linalg.norm(ds.iloc[i,:].values-iworst))

    score = []
    for i in range(len(pos)):
        score.append(neg[i]/(pos[i]+neg[i]))
    
    return score

def add_col(ds,score):
    ds['Topsis Score'] = score
    ds['Rank'] = (ds['Topsis Score'].rank(method='max', ascending=False))
    ds = ds.astype({"Rank": int})

def topsis(dataset, weights, impacts):
    try:
        if(len(dataset) == 0):
            raise Exception("Inadequate dataset")

        non_num_col_list = num(dataset)
        df = dataset.loc[:,dataset.columns.isin(non_num_col_list)].copy()
        if len(df.columns.tolist()) <= 1:
            raise Exception("Column Data incomplete to calculate topsis.")

        wi(len(df.columns.tolist()), weights, impacts)   
        norm(df,weights)
        ideal_best,ideal_worst = ideal(df,impacts)
        score = score(df,ideal_best,ideal_worst)
        add_col(dataset,score)
        return dataset
    
    except Exception as ex:
        print(f"{type(ex).__name__} was raised: {ex}")

if __name__ == "__main__":

    data = pd.read_csv("sample_data.csv")
    weights = [1,1,2,1]
    impacts = ["+","+","-","+"]
    dataset = topsis(data,weights,impacts)
    print(dataset)
