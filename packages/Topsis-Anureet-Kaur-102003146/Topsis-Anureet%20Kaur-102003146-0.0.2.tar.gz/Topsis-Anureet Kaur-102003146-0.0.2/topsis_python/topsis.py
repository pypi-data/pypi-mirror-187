
# MANINDER SINGH 101703325

import pandas as pd
import  numpy as np
import sys
import math as m

file=sys.argv[1]
weights = sys.argv[2]
impacts = sys.argv[3]
outfile=sys.argv[4]

weights = list(map(float ,weights.split(',')))
impacts = list(map(str ,impacts.split(',')))


dataset = pd.read_csv(file)


data=dataset.iloc[ :,1:].values.astype(float)

(r,c)=data.shape

s=sum(weights)

for i in range(c):
    weights[i]/=s

a=[0]*(c)


for i in range(0,r):
    for j in range(0,c):
        a[j]=a[j]+(data[i][j]*data[i][j])

for j in range(c):
    a[j]=m.sqrt(a[j])


for i in range(r):
    for j in range(c):
        data[i][j]/=a[j]
        data[i][j]*=weights[j]

print(data)


pos=np.amax(data,axis=0) 
neg=np.amin(data,axis=0) 
for i in range(len(impacts)):
    if(impacts[i]=='-'):         
        temp=pos[i]
        pos[i]=neg[i]
        neg[i]=temp

dpos=list()
dneg=list()

for i in range(r):
    s=0
    for j in range(c):
        s+=pow((data[i][j]-pos[j]), 2)

    dpos.append(float(pow(s,0.5)))


for i in range(r):
    s=0
    for j in range(c):
        s+=pow((data[i][j]-neg[j]), 2)

    dneg.append(float(pow(s,0.5)))


score=dict()

for i in range(r):
    score[i+1]=dneg[i]/(dneg[i]+dpos[i])

a=list(score.values())
b=sorted(list(score.values()) , reverse=True)

rank=dict()

for i in range(len(a)):
    rank[(b.index(a[i]) + 1)] = a[i]
    b[b.index(a[i])] =-b[b.index(a[i])]


row=list(i+1 for i in range(len(b)))
a=list(rank.values())
rr=list(rank.keys())


out={'Row':row,'Performance Score' : a , 'Rank':rr}

output=pd.DataFrame(out)

print(output)

dataset['Topsis Score'] = a
dataset['Rank'] = rr
dataset.to_csv(outfile)