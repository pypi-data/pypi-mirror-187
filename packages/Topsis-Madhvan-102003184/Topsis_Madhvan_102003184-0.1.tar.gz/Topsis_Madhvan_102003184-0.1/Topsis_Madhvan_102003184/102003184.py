# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 22:19:57 2023

@author: madhv
"""


import sys
import pandas as pd
import math as math
import operator
print (sys.argv)
def main():
    if(len(sys.argv)!=5):
        print("Number of inputs is not correct please try again!!")
        exit(0)
    
    df = pd.read_csv(sys.argv[1])
    w=[float(t) for t in sys.argv[2].split(',')]
    imp=[i for i in sys.argv[3].split(',')]
    
    #checking for number of weights
    
    if(len(w)!=df.shape[1]-1):
        print("No of weights are not correct")
        exit(0)
    
    #checking for the impacts
    
    if(len(imp)!=df.shape[1]-1):
        print("No of impacts are not correct")
        exit(0)
        
    df2 = df.iloc[:,1:].values
    try:
        w=[t/sum(w) for t in w]
    except:
        print("Exception 1 raised")

    for i in range(df2.shape[1]):
        den=math.sqrt(sum(df2[:,i]**2))
        for j in range(df2.shape[0]):
            try:
                df2[j][i] = (df2[j][i])/den
            except:
                print("Exception 2 raised")
    
    for i in range(len(w)):
        df2[:,i]=df2[:,i]*w[i]

    ibv=[]
    iwv=[]
    for i in range(len(imp)):
        if(imp[i]=='+'):
            ibv.append(max(df2[:,i]))
            iwv.append(min(df2[:,i]))
        else:
            ibv.append(min(df2[:,i]))
            iwv.append(max(df2[:,i]))

    ebestd=[]
    eworstd=[]
    for i in range(df2.shape[0]):
        sum1=0
        sum2=0
        for j in range(df2.shape[1]):
            sum1=sum1+(df2[i,j] - ibv[j])**2
            sum1=math.sqrt(sum1)
            sum2=sum2+(df2[i,j] - iwv[j])**2
            sum2=math.sqrt(sum2)
        ebestd.append(sum1)
        eworstd.append(sum2)
    
    ts=[]
    for i in range(len(ebestd)):
        try:
            ts.append(eworstd[i]/(ebestd[i] + eworstd[i]))
        except:
            print("Exception 3 raised")
    
    matrix=[]
    for i in range(len(ts)):
        matrix.append([i+1, df.iloc[i,0],ts[i],0])
    
    matrix.sort(key=operator.itemgetter(2))

    for i in range(len(matrix)):
        matrix[i][3] = len(matrix)-i

    matrix.sort(key=operator.itemgetter(0))

    df['topsis score']=ts

    rank=[]
    for i in range(len(matrix)):
        rank.append(matrix[i][3])

    df['Rank']=rank

    df.to_csv(sys.argv[4])
   # print("Finished")
                
if __name__=="__main__":
    main()
    


