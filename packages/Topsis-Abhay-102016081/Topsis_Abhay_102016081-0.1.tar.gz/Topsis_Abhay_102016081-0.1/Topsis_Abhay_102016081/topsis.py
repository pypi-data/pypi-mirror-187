import numpy as np
import pandas as pd
import math

data=pd.read_excel('data.xlsx')
data.drop(columns=data.columns[0], axis=1,  inplace=True)
data



w=input( "enter the weights:" )
i=input( "enter the impacts:")

w1= pd.to_numeric(w.split(","))
i1= i.split(",")
w1



  


rows=len(data)
columns=len(data.columns)

temp = 0
list=[]
for j in range(columns):
  temp = 0
  for i in range(rows):
    temp= temp + data.iloc[i,j]**2
  list.append(j)
  list[j]=temp


for i in range(columns):
  list[j]=math.sqrt(list[j])

for j in range(columns):
  for i in range(rows):
    data.iloc[i,j]= data.iloc[i,j]/list[j]

for j in range(columns):
  for i in range(rows):
    data.iloc[i,j]*float(w1[j])


v_pstv=[0]*columns
v_ngtv=[0]*columns
for j in range(columns):
  for i in range(rows):
    if i1[j]=='+':
      v_pstv[j]=max(data.iloc[:,j])
      v_ngtv[j]=min(data.iloc[:,j])
    elif i1[j]=='-':
      v_pstv[j]=min(data.iloc[:,j])
      v_ngtv[j]=max(data.iloc[:,j])

v_pstv
v_ngtv

s_pstv=[0]*rows
s_ngtv=[0]*rows

for i in range(rows):
  for j in range(columns):
    s_pstv[i]=np.linalg.norm(data.iloc[i,j]-v_pstv[j])
    s_ngtv[i]=np.linalg.norm(data.iloc[i,j]-v_ngtv[j])

p_score=[0]*rows
for i in range(rows):
  p_score[i]=s_ngtv/(s_ngtv[i]+s_pstv[i])



# data['rank']=p_score[0].rank(ascending=False)
data['topsis score']=p_score[0]
data['rank'] = data['topsis score'].rank(ascending=False)
data.to_csv("out.csv")