import pandas as pd
import  numpy as np
import sys
import math as m

if len(sys.argv) < 4:
    print('NOT ENOUGH ARG')
    sys.exit()
# store the inputs given in the command promt in order datafile,weight,impact resultfile
datafile=sys.argv[1]
weight = sys.argv[2]
impacts = sys.argv[3]
resultfile= sys.argv[4]


#map Returns a list of the results after applying the given function  to each item of a given iterable. 
#We convert weights to float and impact to string.
weight = list(map(float ,weight.split(',')))
impacts = list(map(str ,impacts.split(',')))
try:
    dataset = pd.read_csv(datafile)
except FileNotFoundError as e:
    print(f"FileNotFoundError successfully handled\n"f"{e}")
    sys.exit()

#dataset includes row numbers. therefore exclude row column 
data=dataset.iloc[ :,1:].values.astype(float)

#record rows and columns
(r,c)=data.shape

s=sum(weight)
if(r<2):
    print("Insufficient columns")
    sys.exit()
if len(impacts) != c:
    print("Insufficient impacts")
    sys.exit()
for i in range(c):
    if((impacts[i]!= '+') and (impacts[i]!='-')):
        print("Impacts should only be + or -")
        sys.exit()

if len(weight) != c:
    print("Insufficient weights")
    sys.exit()

#normalization of weights
for i in range(c):
    weight[i]/=s


SsumofC=[0]*(c)
#calculate sum of squares of all columns
for i in range(0,r):
    for j in range(0,c):
        SsumofC[j]=SsumofC[j]+(data[i][j]*data[i][j])

#calculate root of sum of squares of all columns

for j in range(c):
    SsumofC[j]=m.sqrt(SsumofC[j])

#Vector normalization and multiplication by column weight
for i in range(r):
    for j in range(c):
        data[i][j]/=SsumofC[j]
        data[i][j]*=weight[j]

## this becomes WEIGHTED NORMALIZED MATRIX

#we find ideak best and worst values. 
#first we assume that all columns will have best values as the max value 
#but then for columns with impact -ve we swap the values of ideal best and worst

ideal_best=np.amax(data,axis=0) # MAX IN VERTICAL COL
ideal_worst=np.amin(data,axis=0) # MIN IN EACH COL
for i in range(len(impacts)):
    if(impacts[i]=='-'):         # SWAPPING TO STORE REQUIRED IN ideal_best
        temp=ideal_best[i]
        ideal_best[i]=ideal_worst[i]
        ideal_worst[i]=temp
#find euclidean distance with both best and worst ideal values
best_dist=list()
worst_dist=list()

for i in range(r):
    s=0
    for j in range(c):
        s+=pow((data[i][j]-ideal_best[j]), 2)

    best_dist.append(float(pow(s,0.5)))


for i in range(r):
    s=0
    for j in range(c):
        s+=pow((data[i][j]-ideal_worst[j]), 2)

    worst_dist.append(float(pow(s,0.5)))


score=dict()
#performance score is mapped in a dict .values are stored in a 
for i in range(r):
    score[i+1]=worst_dist[i]/(worst_dist[i]+best_dist[i])

a=list(score.values())
b=sorted(list(score.values()) , reverse=True)

rank=dict()
#rank starts from 1 so index+1
#we take element of a. find its index in sorted list b. and that index+1 is final rank
for i in range(len(a)):
    rank[(b.index(a[i]) + 1)] = a[i]
    b[b.index(a[i])] =-b[b.index(a[i])]


a=list(rank.values())
rr=list(rank.keys())

#forming the output file 
out={'score' : a , 'Rank':rr}
output=pd.DataFrame(out)
resultfile=(pd.concat([dataset, output], axis=1))

#saving to the result file.
pd.DataFrame(resultfile).to_csv('102017078-result.csv')
print('Done.Result stored in output file in working directory')