import sys
import os
import pandas as pd

def Normalize(dataset, nCol, weights):
    for i in range(1, nCol):
        temp = 0
        for j in range(len(dataset)):
            temp = temp + dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(dataset)):
            dataset.iat[j, i] = (dataset.iloc[j, i] / temp)*float(weights[i-1])
    print(dataset)


def Calc_Values(dataset, nCol, impact):
    p_sln = (dataset.max().values)[1:]
    n_sln = (dataset.min().values)[1:]
    for i in range(1, nCol):
        if impact[i-1] == '-':
            p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]
    return p_sln, n_sln


print(sys.argv)
f_name= str(sys.argv[0])
in_name=str(sys.argv[1])
wt=str(sys.argv[2])
im=str(sys.argv[3])
out_name=str(sys.argv[4])

wt = wt.split(",")
im=im.split(",")
temp_dataset=pd.read_csv(os.getcwd()+"/"+in_name)
nCol=len(temp_dataset.columns)

Normalize(temp_dataset,nCol,wt)

p_sln, n_sln = Calc_Values(temp_dataset, nCol, im)

score = []
pp = []
nn = [] 
 
 
for i in range(len(temp_dataset)):
    temp_p, temp_n = 0, 0
    for j in range(1, nCol):
        temp_p = temp_p + (p_sln[j-1] - temp_dataset.iloc[i, j])**2
        temp_n = temp_n + (n_sln[j-1] - temp_dataset.iloc[i, j])**2
    temp_p, temp_n = temp_p**0.5, temp_n**0.5
    score.append(temp_n/(temp_p + temp_n))
    nn.append(temp_n)
    pp.append(temp_p)
    

temp_dataset['Topsis Score'] = score
 
temp_dataset['Rank'] = (temp_dataset['Topsis Score'].rank(method='max', ascending=False))
temp_dataset = temp_dataset.astype({"Rank": int})

temp_dataset.to_csv(out_name,index=False)