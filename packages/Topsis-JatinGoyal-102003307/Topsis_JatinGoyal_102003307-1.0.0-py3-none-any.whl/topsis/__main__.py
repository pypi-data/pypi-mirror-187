# Jatin Goyal
# 3COE12
# 102003307

import sys
import pandas as pd
import numpy as np

def main():
    # Total Number of Arguments passed is taken into n
    n = len(sys.argv)
    

    # Exception Handling for case when user inputs incorrect number of Arguments
    if(n!=5):
        raise Exception("The Number of Input Arguments is Wrong")


    #Exception handling for case when the dataset file or the first argument path is
    # encountered with some error
    try:
        df=pd.read_csv(sys.argv[1])
    except FileNotFoundError:
        print("The file you're trying to access does not exist")
        raise
    except:
        print("Dataset file has some Error")
        raise

    

    l=len(df.columns)
    if(l<3):
        raise Exception("Atleast 3 or more columns should be there in the database")


    new_df=df.iloc[:,1:]

    weight=np.array(sys.argv[2].split(","))

    impact=np.array(sys.argv[3].split(","))

    if(np.size(weight)!=np.size(impact)):
        print("Size of weight is not equal to size of impact")
        exit(0)
    elif(np.size(weight)!=l-1):
        print("Size of weight is not equal to size of number of columns  in dataset")
        exit(0)

    resultFileName=sys.argv[4]

    for i in impact:
        if(i!='+' and i!='-'):
            print("Imapact can be either + or - only")
            exit(0)
            
    nrow=len(new_df)
    sumGRE=0
    for i in range(0,l-1):
        sumGRE=0
        dfx=new_df.iloc[:,i].values
        dfx_sq=dfx**2
        sumGRE=sum(dfx_sq)
        dfx=dfx/(sumGRE**(1/2))
        new_df.iloc[:,i]=dfx


    for i in range(0,l-1):
        edit=new_df.iloc[:,i]
        edit=edit*int(weight[i])
        new_df.iloc[:,i]=edit


    for i in range(0,l-1):
        edit=new_df.iloc[:,i].values
        new_df.loc[nrow,new_df.columns[i]]=max(edit)
        new_df.loc[nrow+1,new_df.columns[i]]=min(edit)

    for i in range(0,l-1):
        if(impact[i]=='-'):
            new_df.iloc[nrow,i],new_df.iloc[nrow+1,i]=new_df.iloc[nrow+1,i],new_df.iloc[nrow,i]



    PositiveValue=np.array(0)
    NegativeValue=np.array(0)
    for i in range(0,l-1):
        edit=new_df.iloc[:-2,i].values
        edit1=edit-new_df.iloc[nrow,i]
        edit2=edit-new_df.iloc[nrow+1,i]
        # print(type(edit1))
        edit1=edit1**2
        edit2=edit2**2
        PositiveValue=PositiveValue+edit1
        NegativeValue=NegativeValue+edit2

    PositiveValue=PositiveValue**0.5
    NegativeValue=NegativeValue**0.5


    # print(l)
    P=[0]*len(PositiveValue)
    for i in range(0,nrow):
        P[i]=NegativeValue[i]/(PositiveValue[i]+NegativeValue[i])



    # print(P)
    maxi=0
    maxval=P[0]
    for i in range(1,len(P)):
        if(P[i]>maxval):
            maxi=i
            maxval=P[i]

    P=pd.DataFrame(P)

  
    rank=pd.DataFrame(np.array(range(1,nrow+1)))
  
    df.loc[:,"PerformanceScore"]=P
    df=df.sort_values(by=['PerformanceScore'],ascending=False)
    rank=[]
    for i in range(0,nrow):
        rank.append(i+1)
    df['Rank']=rank
    df=df.sort_index()
    df.to_csv(sys.argv[4])

if __name__=='__main__':
    main()