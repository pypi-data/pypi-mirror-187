import numpy as np
import pandas as pd
import sys

def main():
    # inputFileName, weight, impact, resultFileName
    inputFileName=sys.argv[1]
    resultFileName=sys.argv[4]
    if(len(sys.argv)!=5):
        print("ERROR: Number of arguments are not correct")
        exit()
        
    
    
    weight=[]
    impact=[]
    
    try:
        a = sys.argv[2]
        a = a.split(',')
          
        for i in a:
            weight.append(float(i))
            
        a = sys.argv[3]
        a = a.split(',')
        
      
    except:
        print("ERROR: Wrong Input")
        exit()
    
    for i in a:
        if i=='-':
            impact.append(-1)
        elif i=='+':
            impact.append(1)
        else:
            print("ERROR: Impacts must be either +ve or -ve.")
            exit()

    try:
        df=pd.read_csv(inputFileName)
        result_df=pd.read_csv(inputFileName)
    except:
        print("ERROR: File not Found")
        exit()
    
    row=df.shape[0]
    col=df.shape[1]
    
    if col<3:
        print("ERROR: More columns required")
        exit()
    
    if df.iloc[:,1:col].shape[1] != df.iloc[:,1:col].select_dtypes(include=np.number).shape[1]:
        print("ERROR: Data contains non-numeric value")
        exit()
        
    if len(weight)!=col-1 or len(impact)!=col-1:
        print("ERROR: Length of weight or impact is not equal to column")
        exit()
    
    rsq=[]
    for i in range(1,col):
        sq=0
        for j in range(0,row):
            sq=sq+df.iloc[j,i]**2
        rsq.append(sq**(0.5))
        
    
    for i in range(row):
        for j in range(1,col):
            df.iloc[i,j]=df.iloc[i,j]/rsq[j-1]
            
    
    for i in range(row):
        for j in range(1,col):
            df.iloc[i,j]=df.iloc[i,j]*weight[j-1]
            
    
    ideal_best=df.max(axis=0)
    ideal_worst=df.min(axis=0)
    
    for i in range(1,col):
        if impact[i-1]==-1:
            temp=ideal_best[i]
            ideal_best[i]=ideal_worst[i]
            ideal_worst[i] =temp
    
    s_pos=[]
    s_neg=[]
    
    for i in range(row):
        temp1=0
        temp2=0
        for j in range(1,col):
            temp1=temp1+((df.iloc[i,j]-ideal_best[j])**2)
            temp2=temp2+((df.iloc[i,j]-ideal_worst[j])**2)
        s_pos.append(temp1**(0.5))
        s_neg.append(temp2**(0.5))
        
    performance_score=[]
    for i in range(row):
        performance_score.append(s_neg[i]/(s_neg[i]+s_pos[i]))
        
    df['Performance Score']=performance_score
        
    rank=np.arange(1,row+1)
    df=df.sort_values(by=['Performance Score'],ascending=False)
    df['Rank']=rank
    df=df.sort_index()
    
    result_df['Performance Score']=df['Performance Score']
    result_df['Rank']=df['Rank']
    result_df.to_csv(resultFileName)
    # print(df.iloc[:,1:col])



if __name__ == "__main__":
    main()
    # file=r"D:\Thapar college\Sixth Sem\Predictive Analysis\Topsis\102017101-data.csv"
    # result_file=r"D:\Thapar college\Sixth Sem\Predictive Analysis\Topsis\102017100-result.csv"
    # weight=[1,1,1,1,2]
    # impact=[-1,1,1,1,-1]
    # topsis_func(file, weight, impact, result_file)



    
        
    # topsis_func(sys.argv[1], weight, impact, sys.argv[4])
