import pandas as pd
import numpy as np
import math
import sys

def main():
    n=len(sys.argv)
    if n!=5:
        print("The number of parameters passed are not correct, format should be <program.py> <InputDatafile> <weights> <impacts> <ResultFileName>")
        quit()

    try: 
        df=pd.read_csv(sys.argv[1])
    except:
        print("File not found")
        sys.exit(0)

    df=pd.read_csv(sys.argv[1])
    result=df.copy()
    df=df.drop(df.columns[0],axis=1)
    wt=sys.argv[2].split(',')
    weight=len(wt)
    impacts=sys.argv[3].split(',')
    impact=len(impacts)
    output=sys.argv[4]
    add_row=[]
    ideal_best=[]
    ideal_worst=[]


    if df.shape[1] <3:
        print("Number of columns should be greater than 3")
        quit()

    if weight!=impact:
        print("Number of elements passed in weight is not equal to impacts")
        quit()

    if df.shape[1]!=weight:
        print("Number of columns and weight/impact passed are not equal")
        quit()
    
    for i in impacts:
        if i !='+' and i!='-':
            print("Impact should be +/-")
            quit()

    cat=[]
    for i in df.columns:
        cat.append(i)
    cat.pop(0)
    for i in cat:
        if df[i].dtype!=np.int64 and df[i].dtype!=np.float64:
            print("Data type should be numeric")
            quit()

    #Step1 Normalization
    for i in range(len(df.axes[1])):
        sum=0
        for j in range(len(df.axes[0])):
            sum+=df.iloc[j,i]**2
        add_row.append(math.sqrt(sum))
    # print(add_row)

    # Weights normalization
    for i in range(len(df.axes[1])):
        for j in range(len(df.axes[0])):
           df.iloc[j,i]= float(df.iloc[j,i])/float(add_row[i])
           df.iloc[j,i]= float(df.iloc[j,i])*float(wt[i])

    # Ideal best and ideal worst
    high=[]
    low=[]
    for i in range(len(df.axes[1])):
        high.append(df.iloc[:,i].max())
        low.append(df.iloc[:,i].min())

    for i in range(len(high)):
        if impacts[i] == '+':
            ideal_best.append(high[i])
            ideal_worst.append(low[i])
        else:
            ideal_best.append(low[i])
            ideal_worst.append(high[i])
    # print(ideal_best)
    # print(ideal_worst)
    # Euclidean distance
    S_best=[]
    S_worst=[]
    for i in range(len(df.axes[0])):
        total_best=0
        total_worst=0
        for j in range(len(df.axes[1])):
            total_best+=(df.iloc[i][j]-ideal_best[j])**2
            total_worst+=(df.iloc[i][j]-ideal_worst[j])**2
        S_best.append(total_best**0.5)
        S_worst.append(total_worst**0.5)
    # print(S_best)
    # print(S_worst)

    # Performance coloumn
    Performance=[]
    for i in range(len(S_best)):
        Performance.append(float(S_worst[i])/float((S_best[i]+S_worst[i])))
    # print(Performance)
    
    result['Performance']=Performance
    result['Rank']=result['Performance'].rank(ascending=False).astype(int)

    # print(df)
    # print(result)
    result.to_csv(output,index=False)
    print("Success")

if __name__ == '__main__':

    main()


    
        

