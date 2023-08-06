import numpy as np
import pandas as pd
import sys
# import csv

narg=len(sys.argv)
if narg<5:
    print("Please pass 5 number of arguments")
    exit()

if (sys.argv[1] == '-'):
    f = sys.stdin.read().splitlines()
else:
    try:
        filename = sys.argv[1]
        f = open(filename, 'r')
    except:
        print("Error, File Not found")
        exit()
# csv = csv.reader(f)
# raw_data = list(csv)
csv=pd.read_csv(sys.argv[1])
raw_data = list(csv)
df=pd.DataFrame(data=raw_data)

csvfile=pd.read_csv(sys.argv[1])
dataset=pd.DataFrame(data=csvfile)


nrows=len(df.axes[0])
ncols=len(df.axes[1])
if ncols<3:
    print("Error, The number of columns are less than 3")
    exit()
df=df.drop([0],axis=1)
df=df.drop([0])

for i in range(1,ncols):
    try:
        df[i] = df[i].astype('float')
    except:
        print("alpha-numeric row can't be typecasted to numeric")
        exit()

im=sys.argv[3]
impacts = im.split(",")
if len(impacts) == 1:
    print("Invalid input.")
    exit()
for j in range(0,ncols-1):
    if impacts[j]!='+' and impacts[j]!='-':
        print("impacts must be positive or negative")
        exit()
w=sys.argv[2]
we = w.split(",")
if len(we) == 1:
    print("Invalid input.")
    exit()
weight=[float(x) for x in we]

#Vector Normalization
sqrt_sum=[]
for i in range(1,ncols):
    sum=0
    for j in range(1,nrows):
        sum=sum+(df[i][j])**2
    sqrt_sum.append(sum**0.5)


for i in range(1,nrows):
    for j in range(1,ncols):
        df[j][i]=df[j][i]/sqrt_sum[j-1]




for i in range(1,nrows):
    for j in range(1,ncols):
        df[j][i]=df[j][i]*weight[j-1]
df




ideal_best=np.zeros(ncols-1)
ideal_worst=np.zeros(ncols-1)
for i in range(1,ncols):
    max_val=df[i].max()
    min_val=df[i].min()
    if impacts[i-1]=='+':
        ideal_best[i-1]=max_val
        ideal_worst[i-1]=min_val
    else:
        ideal_best[i-1]=min_val
        ideal_worst[i-1]=max_val



sp=[]
sn=[]
for i in range(1,nrows):
    sump=0
    sumn=0
    for j in range(1,ncols):
        sump=sump+(df[j][i]-ideal_best[j-1])**2
        sumn=sumn+(df[j][i]-ideal_worst[j-1])**2
    sp.append(sump**0.5)
    sn.append(sumn**0.5)



performance_score=[]
for i in range(1,nrows):
    score=sn[i-1]/(sp[i-1]+sn[i-1])
    performance_score.append(score)




df[ncols]=np.array(performance_score)
dataset['Score']=np.array(performance_score)



df[ncols+1]=(df[ncols].rank(method='max',ascending=False))
dataset['Rank']=(dataset['Score'].rank(method='max',ascending=False))




df=df.astype({ncols+1:int})
dataset=dataset.astype({'Rank':int})


dataset.to_csv(sys.argv[4])
