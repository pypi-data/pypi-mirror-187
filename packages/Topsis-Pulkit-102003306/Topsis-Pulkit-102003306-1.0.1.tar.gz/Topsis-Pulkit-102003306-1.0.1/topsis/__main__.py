import pandas as pd
import numpy as np
import math
import sys


def main():
    
    #normalisation
    df=pd.read_csv(sys.argv[1])
    for i in range(1,df.shape[1]):
        x=df.iloc[:,i]
        x1=np.array(x)
        sum=0
        for j in x1:
            sum=sum+j*j
        sum=math.sqrt(sum)
        x1=x1/sum
        df.iloc[:,i]=x1

    print(df)

    weights=(sys.argv[2]).split(',')

    for i in range(1,df.shape[1]):
        x=np.array(df.iloc[:,i])
        x=x*float(weights[i-1])
        df.iloc[:,i]=x
    print(df)

    badachota=(sys.argv[3]).split(',')

    best=[]
    worst=[]
    for i in range(1,df.shape[1]):
        x=np.array(df.iloc[:,i])
        if(badachota[i-1]=='+'):
            best.append(max(x))
            worst.append(min(x))
        elif(badachota[i-1]=='-'):
            best.append(min(x))
            worst.append(max(x))
        else:
            print('error')

    print(best)
    print(worst)

    best1=[]
    worst1=[]
    for i in range(0,df.shape[0]):
        r=np.array(df.iloc[i,1:])
        #print(r)
        sumb=0
        sumw=0
        for j in range(0,r.size):
            sumb=sumb+(r[j]-best[j])**2
            sumw=sumw+(r[j]-worst[j])**2
        best1.append(math.sqrt(sumb))
        worst1.append(math.sqrt(sumw))

    print(best1)
    print(worst1)
    perf=(np.array(worst1))/(np.array(best1)+np.array(worst1))
    s=np.copy(perf)
    s=np.sort(s)
    top=[]
    for i in range(0,perf.size):
        for j in range(0,perf.size):
            if(perf[i]==s[j]):
                top.append(perf.size-j)
    df1=pd.read_csv(sys.argv[1])
    df1['Performance']=perf
    df1['Topsis']=np.array(top)
    print(df1)
    df1.to_csv(sys.argv[4])
    


 




if __name__=='__main__':
    main()
 