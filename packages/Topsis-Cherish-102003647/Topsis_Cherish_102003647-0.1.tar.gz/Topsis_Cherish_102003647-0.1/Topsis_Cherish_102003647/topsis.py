import numpy as np
import pandas as pd
import math
import sys
import os


def topsis(A,weight,imp) :

    df=A.copy()
    df.iloc[0:df.shape[0],1:df.shape[1]]
    a=df.iloc[0:df.shape[0],1:df.shape[1]].shape

    #print(len(sys.argv[2]))

    if a[1]<3 :
        print("ERROR => Number of Columns are less than 3")
        exit(0)

    for i in range(1,(a[1]+1)):  
        s=0 
        for j in range(0,a[0]):
            s=s+df.iloc[j,i]*df.iloc[j,i]
        df.at[a[0],i]=math.sqrt(s)
        df.iloc[a[0],i]=math.sqrt(s)
    df=df.drop(df.iloc[:,(a[1]+1):],axis=1)
    for i in range(1,(a[1]+1)):   
        for j in range(0,a[0]):
            df.iloc[j,i]=df.iloc[j,i]/df.iloc[a[0],i]
    w1=list()
    wt=list()
    length=len(weight)
    str=""
    for i in weight :
        if i!=',' :
            str=str+i
        else :
            w1.append(str)
            str=""
    w1.append(str)
    for i in w1 :
        wt.append(float(i))
    if len(wt)!=a[1]:
        print("Weight count is not correct ")
        exit(0)
    for i in range(1,(a[1]+1)):   
        for j in range(0,a[0]):
            df.iloc[j,i]=df.iloc[j,i]*(wt[i-1])
    impact=list()
    for i in imp:
        if i!=',' :
            impact.append(i)
    if len(impact)!=a[1]:
        print("Impact count is not correct ")
        exit(0)
    for i in range(1,(a[1]+1)):       
        if(impact[i-1]=='+'):
            df.at[a[0],i]=df.iloc[:(a[1]+1),i].max()
            df.iloc[a[0],i]=df.iloc[:(a[1]+1),i].max()
            df.at[(a[0]+1),i]=df.iloc[:(a[1]+1),i].min()
            df.iloc[(a[0]+1),i]=df.iloc[:(a[1]+1),i].min()
        elif(impact[i-1]=='-'):
            df.at[a[0],i]=df.iloc[:(a[1]+1),i].min()
            df.iloc[a[0],i]=df.iloc[:(a[1]+1),i].min()
            df.at[(a[0]+1),i]=df.iloc[:(a[1]+1),i].max()
            df.iloc[(a[0]+1),i]=df.iloc[:(a[1]+1),i].max()
        else:
            print("ERROR => Wrong expression for impact!")
            exit(0)
    df=df.drop(df.iloc[:,(a[1]+1):],axis=1)
    for i in range(0,a[0]):   
        s=0
        t=0
        for j in range(1,a[1]+1):
            s=s+(df.iloc[i,j]-df.iloc[a[0],j])*(df.iloc[i,j]-df.iloc[a[0],j])
            t=t+(df.iloc[i,j]-df.iloc[(a[0]+1),j])*(df.iloc[i,j]-df.iloc[(a[0]+1),j])
        df.at[i,(a[1]+1)]=math.sqrt(s)
        df.iloc[i,(a[1]+1)]=math.sqrt(s)
        df.at[i,(a[1]+2)]=math.sqrt(t)
        df.iloc[i,(a[1]+2)]=math.sqrt(t)
    for i in range(0,a[0]):
        ans=0
        for j in range(1,a[1]+1):
            ans=df.iloc[i,(a[1]+2)]/(df.iloc[i,(a[1]+1)]+df.iloc[i,(a[1]+2)])
        df.at[i,(a[1]+3)]=ans
        df.iloc[i,(a[1]+3)]=ans
    df=df.drop(df.index[-1])
    df=df.drop(df.index[-1])
    ranks=df[a[1]+3].rank()
    for i in range(0,a[0]):
        ranks.iloc[i]=int(a[0]+1-ranks.iloc[i])
    ndf=A.copy()
    ndf['Topsis Score'] =df[a[1]+3]
    ndf['Rank']=ranks 
    print(ndf)
# data=pd.read_csv('dataaaa.csv')
# topsis(data,"0.25,0.25,0.25,0.25,0.25" ,"-,+,+,+,+" )
def cli_output():
    if len(sys.argv) != 5:
        print('Wrong Number of args')
        print('Input should be like - \n '
              'python [package name] [path of csv as string] [list of weights as string] [list of sign as string]')
    else:
        file_path = sys.argv[1]
        try:
            if os.path.exists(file_path):
                print('Path exist')
        except OSError as err:
            print(err.reason)
            exit(1)

        df = pd.read_csv(file_path)
        w = sys.argv[2]
        s= sys.argv[3]
        topsis(df, w, s)

if __name__ == '__main__' :
    cli_output()       
