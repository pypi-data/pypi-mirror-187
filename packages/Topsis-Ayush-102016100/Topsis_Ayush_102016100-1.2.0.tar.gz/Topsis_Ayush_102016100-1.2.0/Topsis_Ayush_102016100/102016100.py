import sys
import math
import pandas as pd
import numpy as np
import logging
from logging import exception
import os

def topsis():
  try:
    length=len(sys.argv)
    if length != 5:
        raise exception
  except:
    print('You must have 4 parameters present that is the name of the csv file to run the process, weights, impacts, output file.\nError Occured because of passing less/more than 4 arguments.')
    sys.exit()
  try:
    file=sys.argv[1]
    data=pd.read_csv(file)
  except:
    print("You either have entered incorrect file name/extension or the file don't exist.")
    sys.exit()
  try:
    if len(data.columns)<3:
        raise exception
  except:
    print('Csv file must have at least 3 columns, column length lower than 3 will result in an error.')
    sys.exit()
  try:
    df=data.iloc[:,1:]
    for i in df.columns:
      pd.to_numeric(df[i],errors='coerce')
      df[i].fillna(df[i].mean(),inplace=True)
  except:
    print('Some cells of Csv file does contain non numeric values, recheck again')
    sys.exit()
  try:
    weights=[float(i) for i in sys.argv[2].split(',')]
    impacts=[str(i) for i in sys.argv[3].split(',')]
  except:
    print('Input Weights or impacts are not seperated by commas')
    sys.exit()
  try:
    if len(df.columns)!=len(weights) or len(df.columns)!=len(impacts):
      raise exception
  except:
    print('Number of columns and length of weights and impacts are not same')
    sys.exit()
  try:
    for i in impacts:
      if not (i=='+' or i=='-'):
        raise exception
  except:
    print('Impacts must have either positive sign or negative sign')
    sys.exit()
  try:
    if ".csv" != (os.path.splitext(sys.argv[4]))[1]:
      raise exception
    result=sys.argv[4]
  except:
    print('Output file given is not csv')
    sys.exit()

  z=0
  ide_best=[]
  ide_worst=[]
  for i in df.columns:
    x=math.sqrt(np.sum(df[i]*df[i]))
    df[i]=(df[i]*weights[z])/x
    if impacts[z]=='+':
      ide_best.append(df[i].max())
      ide_worst.append(df[i].min())
    else:
      ide_best.append(df[i].min())
      ide_worst.append(df[i].max())
    z=z+1

  df['pos']=0
  df['neg']=0
  z=0
  for i in df.columns[:-2]:
    df['pos']+=((df[i]-ide_best[z])**2)
    df['neg']+=((df[i]-ide_worst[z])**2)
    z=z+1
  pos=df['pos'].values
  neg=df['neg'].values
  for i in range(len(pos)):
    pos[i]=math.sqrt(pos[i])
    neg[i]=math.sqrt(neg[i])
  pos, neg
  df['pos']=pos
  df['neg']=neg
  df['total']=df['pos']+df['neg']
  df['score']=df['neg']/df['total']

  data['Topsis Score']=df['score']
  data['Rank'] = data['Topsis Score'].rank(ascending = 0)
  data['Rank']=data['Rank'].astype(np.int32)

  data.to_csv(result,index=None)
