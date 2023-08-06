import pandas as pd
import math as m
import numpy as np
import sys
import logging


File_name = sys.argv[1]
w = sys.argv[2]
im = sys.argv[3]
Output_File = sys.argv[4]
logging.basicConfig(filename="101903244-log.log",level = logging.DEBUG,encoding='utf-8')

if ',' not in w:
    logging.error("Array weights should be separated by ','")
    
weight = w.split(',')
try:
    weight = list(map(int,weight))
except ValueError:
    logging.error("Weights has non integral value")

if ',' not in im:
    logging.error("Array impacts should be separated by ','")
impact = im.split(',')
    
# outfile = args[4]
    
for x in impact:
    if x != '+' and x != '-':
        logging.error("Impact must contain only '+' or '-'")

try:
    df = pd.read_csv(File_name)
except FileNotFoundError:
    logging.error("Input file provided not found")

    
df1 = pd.read_csv(File_name)
# print(df1)

    # weight = (1,1,1,1,1)
    # impact = ('+', '-', '+', '+', '-')
imp ={}
for col in df.columns:
    if 'Fund Name' in col:
        del df[col]
#df.drop(df.columns[[0]], axis=1, inplace=True)
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
def Normalize(df, nCol,weight):
    for i in range(0, nCol):
        temp = 0
            # Calculating Root of Sum of squares of a particular column
        for j in range(len(df)):
            temp = temp + df.iloc[j, i]**2
        temp = (temp**0.5)*weight[i]
        
        for j in range(len(df)):
            df.iat[j, i] = (df.iloc[j, i] / temp)
            
Normalize(df,cols1,weight)
# print(df)
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
    #         sum = sum + ((df.iloc[0,i]-df_a_pos.iloc[i])**2)
    #     df.Si[j] = sum
    # print(df)
df['Si+Sj'] = df['Si']+df['Sj']
df["Topsis Score"] = df['Si']/df['Si+Sj']*100
df['Rank'] = df['Topsis Score'].rank().astype('int64')
    # print(df1)
df2 = df1.iloc[:, 0:6]
    # print(df2)
df3 = df.iloc[:, 8:11]
    # print(df3)
result = pd.concat([df2, df3], axis=1)
result.to_csv(Output_File)