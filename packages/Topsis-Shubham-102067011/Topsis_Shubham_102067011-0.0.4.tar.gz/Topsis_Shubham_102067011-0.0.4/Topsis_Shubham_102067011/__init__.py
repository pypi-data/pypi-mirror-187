
def normalize(df):
    import numpy as np
    cols = df.columns[1::]
    for i in cols:
        #CHECKING IF ALL ELEMENTS ARE NUMERIC
        if(all([isinstance(item, float) for item in df[i]])==True):
           normval = np.sqrt(np.sum(np.power(df[i],2)))
           df[i] = df[i]/normval
        else:
            raise Exception("Column must contain only numeric values!!")
    return df




def weightAssignment(df,weights):
    import numpy as np
    id = 0
    cols = df.columns[1::]
    if(len(cols)!=len(weights)):
       raise Exception("Number of columns and number of weights do not match!!","columns",len(cols),"weights size",len(weights))
    for i in cols:
        #CHECKING IF WEIGHTS ARE NUMERIC
        if(str(weights[id]).isdigit() == True):
           df[i] = np.multiply(df[i],int(weights[id]))
           id = id+1
        else:
            raise Exception("Weights should be numeric only!! and seperated by a ',' ")
    return df



def ideal(df,impacts):
    best = []
    worst = []
    id = 0
    cols = df.columns[1::]
    if(len(cols)!=len(impacts)):
        raise Exception("Number of columns and number of impacts do not match!!","columns",len(cols),"weights size",len(impacts))
    for i in cols:
        mx = max(df[i])
        mn = min(df[i])
        if (impacts[id] == '+'):
            best.append(mx)
            worst.append(mn)
        elif(impacts[id]=='-'):
            worst.append(mx)
            best.append(mn)
        else:
            #CHECKING IMPACTS
            raise Exception("Impacts should be either '+' or '-' only!! and seperated by a ',' ")
        id+=1
    return best,worst




def euclideanDist(df,best,worst):
    import numpy as np
    best_dist = []
    worst_dist = []
    df = df.drop(df.columns[[0]],axis=1)
    for i in range(0,len(df)):
        k = df.iloc[i].values
        dist = np.sqrt(np.sum(np.square(k - best)))
        best_dist.append(dist)
        dist = np.sqrt(np.sum(np.square(k - worst)))
        worst_dist.append(dist)
    return best_dist,worst_dist


def performance_score(best_dist,worst_dist):
    import numpy as np
    return np.divide(worst_dist,np.add(best_dist,worst_dist))


def TOPSIS_result(df,performance_score):
    import numpy as np
    a = np.array(performance_score)
    sorted_indices = np.argsort(-a)
    ranks = np.empty_like(sorted_indices)
    ranks[sorted_indices] = np.arange(len(a))
    ranks = list(np.add(ranks,1))
    performance_score =list(performance_score)
    df['Performance score']= performance_score
    df['Rank'] = ranks
    return df