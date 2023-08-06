import numpy as np
import pandas as pd
import sys
import os

def main():
    n = len(sys.argv)
    
    #checking if correct no. of inputs are provided or not
    if(n!=5):
        print("ERROR: Provide correct number of inputs.")
        exit()
   
    #checking if files are in .csv
    if not sys.argv[1].endswith(".csv"):
        print("ERROR:{} is not a csv file.".format(sys.argv[1]))
        exit()
    if not sys.argv[4].endswith(".csv"):
        print("ERROR:{} is not a csv file.".format(sys.argv[4]))
        exit()
    
    #checking if the output file name is provided
    if sys.argv[4]=='':
        print("ERROR: Please provide an output file name.")
        exit()
    
    #check if the dataset is in the current working directory
    isExist = os.path.exists(sys.argv[1])
    if(isExist==0):
        print("ERROR:{} does not exist".format(sys.argv[1]))
        exit()
    
    #checking if the weights are provided in correct format
    try:
        weights = sys.argv[2].split(",")
    except ValueError:
        print("ERROR: Weights are not provided in the correct format.")
        exit()
    
    #checking if the impacts are provided in the correct format
    try:
        impacts = sys.argv[3].split(",")
    except ValueError:
        print("ERROR: Impacts are not provided in the correct format.")
        exit()
    
    weights = sys.argv[2].split(",")
    impacts = sys.argv[3].split(",")
    
    data=pd.read_csv(sys.argv[1])
    
    if len(weights)!=len(data.columns)-1:
        print("ERROR: Number of weights not equal to number of features.")
        exit()
    if len(impacts)!=len(data.columns)-1:
        print("ERROR: Number of impacts not equal to number of features.")
        exit()
    if(len(data.columns)-1<=2):
        print("ERROR: INput file must contain 3 or more columns.")
        exit()
    for i in impacts:
        if i !='+' and i !='-':
            print("ERROR: Impacts should be in +/-.")
            exit()
    df=data.copy(deep=True)
    output=data.copy(deep=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    result=sys.argv[4]
    x=df.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
    for i in x:
        if i==False:
            print("ERROR: The data might have non numeric values.")
            exit()
    
    D=topsis(df,weights,impacts,output)
    D.to_csv(result, index=False)
    sys.stdout.write("{} has been created in the current working directory.".format(result))

def topsis(df,w,impacts,output):
    ncol=len(df.columns)
    n=np.size(df)
    nrow=int(n/ncol)
    rss=[]
    #root of sum of squares
    for j in range(0,ncol):
        ans=0
        for i in range(0,nrow):
            h=df.iloc[i][j]
            ans=ans+np.square(h)
        rss.append(np.sqrt(ans))
    #dividing these
    for i in range(0,nrow):
        for j in range(0,ncol):
            df.iloc[i][j]=float(df.iloc[i][j])/float(rss[j]) 
    #assigning weights
    for i in range(0,nrow):
        for j in range(0,ncol):
            df.iloc[i][j]=float(df.iloc[i][j])*float(w[j])
    
    #max min values
    max_val=df.max().values
    min_val=df.min().values
    
    #arranging with impacts
    for i in range(0,ncol):
        if impacts[i]=='-':
            max_val[i],min_val[i]=min_val[i],max_val[i]
    #calculating euclidean dist
    sp=[]
    sn=[]
    for i in range(0,nrow):
        sum1=0
        sum2=0
        for j in range(0,ncol):
            sum1=sum1+np.square(df.iloc[i][j]-max_val[j])
            sum2=sum2+np.square(df.iloc[i][j]-min_val[j])
        sp.append(np.sqrt(sum1))
        sn.append(np.sqrt(sum2))
    
    #performance measure
    p=[]
    for i in range(0,nrow):
        p.append(float(sn[i])/float(sn[i]+sp[i]))

    output['Score']=p
    output['Rank']=output['Score'].rank(ascending=False).astype(int)
    return output

if __name__ == "__main__":
    main()