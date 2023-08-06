import pandas as pd
import math as m
import numpy as np
import sys
import logging


File_name = sys.argv[1]
Weights = sys.argv[2]
Impacts = sys.argv[3]
Output_File = sys.argv[4]
logging.basicConfig(filename="101903244-log.log",level = logging.DEBUG,encoding='utf-8')

if ',' not in Weights:
    logging.error("Array weights should be separated by commas','")
    
weight = Weights.split(',')
try:
    weight = list(map(int,weight))
except ValueError:
    logging.error("Weights has non integral value")

if ',' not in Impacts:
    logging.error("Array impacts should be separated by ','")
impact = Impacts.split(',')
    
# outfile = args[4]
    
for x in impact:
    if x != '+' and x != '-':
        logging.error("Impact must contain only '+' or '-'")

try:
    df = pd.read_csv(File_name)
except FileNotFoundError:
    logging.error("Input file provided not found")

    
df1 = pd.read_csv(File_name)
# print(df)
imp ={}
df.drop(df.columns[[0]], axis=1, inplace=True)
# print(df)
# computing number of rows
rows = df.axes[0]
rows1 = len(df.axes[0])
# computing number of columns
cols = df.axes[1]
cols1 = len(df.axes[1])
k = 0
for t in cols:
    imp[t]=impact[k]
    k=k+1
den = df.apply(np.square).apply(np.sum,axis = 0).apply(np.sqrt)

for i in range(cols1):
    for j in range(rows1):
        df.iat[j, i] = (df.iloc[j, i] / den[i]) * weight[i]

a_pos = {}
a_neg = {}

for i in cols:
    if(imp[i]=='+'):
        a_pos[i]=max(df[i])
        a_neg[i]=min(df[i])
        
    else:
        a_pos[i]=min(df[i])
        a_neg[i]=max(df[i])       
df_a_pos = pd.DataFrame.from_dict(a_pos, orient ='index')
df_a_neg = pd.DataFrame.from_dict(a_neg, orient ='index')

df['Si']= np.nan
df['Sj']=np.nan
for j in range(rows1):
    sum = 0
    sum1 = 0
    for i in range(cols1):
        sum  = sum + ((df.iloc[j,i]-df_a_pos.iloc[i])**2)
        sum1 = sum1 + ((df.iloc[j,i]-df_a_neg.iloc[i])**2)
    df['Si'][j] = sum**0.5
    df['Sj'][j] = sum1**0.5

df['Si+Sj'] = df['Si']+df['Sj']
df["Topsis Score"] = df['Si']/df['Si+Sj']*100
df['Rank'] = df['Topsis Score'].rank().astype('int64')
df2 = df1.iloc[:, 0:6]
df3 = df.iloc[:, 8:11]
result = pd.concat([df2, df3], axis=1)
result.to_csv(Output_File)