import sys
import math
import pandas as pd
import numpy as np
import logging
from logging import exception
import os
def topsis(inputFile,weight,impact,outputFile):
    try:
        data=pd.read_csv(inputFile)
    except:
        logging.error("File Not Found")
        sys.exit()
    try:
        if(len(data.columns))<3:
            raise exception
    except:
        logging.error("Constraint that there should be minimum 3 columns not fulfilled")
        sys.exit()
    try:
        df=data.iloc[:,1:]
        for i in df.columns:
            pd.to_numeric(df[i],errors='coerce')
            df[i].fillna(df[i].mean(),inplace=True)
    except:
        logging.error('Some cells of Csv file does contain non numeric values, recheck again')
        sys.exit()
    try:
        weights=[float(i) for i in weight.split(',')]  
        impacts=[str(i) for i in impact.split(',')]     
    except:
        logging.error("Values should be separated by a ,")
        sys.exit()
    try:
        if len(df.columns)!=len(weights):
            raise exception
    except:
        logging.error("The number of entries in weights are not equal to the data provided")
        sys.exit()
    try :
        if len(df.columns)!=len(impacts):
            raise exception
    except:
        logging.error("The number of entries in impacts are not equal to the data provided")
        sys.exit()
    try: 
        for i in impacts:
            if not (i=='+' or i=='-'):
                raise exception
    except:
        logging.error("The entries in impact should be either + or -")
        sys.exit()
    try:
        if ".csv" != (os.path.splitext(outputFile))[1]:
            raise exception
    except:
        logging.error('Output file given is not csv')
        sys.exit()   


    z=0
    ideal_best=[]
    ideal_worst=[]
    for i in df.columns:
        x=math.sqrt(np.sum(df[i]*df[i]))
        df[i]=(df[i]*weights[z])/x
        if impacts[z]=='+':
            ideal_best.append(df[i].max())
            ideal_worst.append(df[i].min())
        else:
            ideal_best.append(df[i].min())
            ideal_worst.append(df[i].max())
        z=z+1

    df['positive']=0
    df['negative']=0
    z=0
    for i in df.columns[:-2]:
        df['positive']+=((df[i]-ideal_best[z])**2)
        df['negative']+=((df[i]-ideal_worst[z])**2)
        z=z+1
    pos=df['positive'].values
    neg=df['negative'].values
    for i in range(len(pos)):
        pos[i]=math.sqrt(pos[i])
        neg[i]=math.sqrt(neg[i])
    pos, neg
    df['positive']=pos
    df['negative']=neg
    df['total']=df['positive']+df['negative']
    df['score']=df['negative']/df['total']

    data['Topsis Score']=df['score']
    data['Rank'] = data['Topsis Score'].rank(ascending = 0)
    data['Rank']=data['Rank'].astype(np.int32)

    data.to_csv(outputFile,index=None)
topsis('102016099-data.csv','1,2,1,2,1','+,-,+,+,-','102016099-result.csv')    