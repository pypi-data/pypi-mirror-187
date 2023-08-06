import pandas as pd
import numpy as np
import sys
import os

def topsis(df,weight,imp,output):
    dataset = df.drop(df.columns[0],axis=1)
    dataOutput = dataset.copy()
    numRows = dataset.shape[0]
    numCol = dataset.shape[1]

    if numCol<3 :
        print("Error - Number of columns are less than 3")
        exit(0)

    sum1=list()
    for i in range(0,numCol):
        temp = dataset.iloc[:,i].values
        sum = 0
        for j in temp:
            sum = sum + j*j
        sum = pow(sum,0.5)
        sum1.append(sum)
    
    for i in range(0,numCol) :
        for j in range(0,numRows) :
            dataset.iloc[j,i]=dataset.iloc[j,i]/sum1[i]

    w1=list()
    wt=list()
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

    if len(wt)!=numCol:
        print("Weight count is not correct ")
        exit(0)

    for i in range(0,numCol):
        j = wt[i]
        temp = dataset.iloc[:,i].values
        for k in range(0,numRows):
            temp[k] = temp[k]*j

    idealbest = []
    idealworst = []
    impact=list()
    for i in imp:
        if i!=',' :
            impact.append(i)

    if len(impact)!=numCol:
        print("Impact count is not correct ")
        exit(0)

    for i in range(0,numCol):
        mini = sys.maxsize
        maxi = ~sys.maxsize
        temp = dataset.iloc[:,i].values
        for j in range(0,numRows):
            if(temp[j] < mini):
                mini = temp[j]
            if(temp[j] > maxi):
                maxi = temp[j]

            if impact[i] == "+":
                idealbest.append(maxi)
                idealworst.append(mini)
            elif impact[i] == "-":
                idealbest.append(mini)
                idealworst.append(maxi)

    euclidbest = []
    euclidworst = []

    for i in range(0,numRows):
        temp = dataset.iloc[i].values
        sum1 = 0
        sum2 = 0
        for j in range(0,numCol):
            sum1 = sum1 + pow(temp[j] - idealbest[j],2)
            sum2 = sum2 + pow(temp[j] - idealworst[j],2)

        sum1 = pow(sum1,0.5)
        sum2 = pow(sum2,0.5)

        euclidbest.append(sum1)
        euclidworst.append(sum2)

    perf = []
    for i in range(0,numRows):
        x = euclidworst[i]/(euclidworst[i] + euclidbest[i])
        perf.append(x)

    rank = []
    performanceScore = perf.copy()
    perf.sort(reverse=True)

    for i in range(0,numRows):
        for j in range(0,numRows):
            if performanceScore[i] == perf[j]:
                rank.append(j+1)
                break
            elif performanceScore[i] != perf[j]:
                continue

    dataOutput["Topsis Score"] = performanceScore
    dataOutput["Rank"] = rank
    print(dataOutput)
    dataOutput.to_csv(output)



def outfunc():
    if len(sys.argv)!=5 :
        print("Arguments are not equal to four !! Enter arguments in the order <input.csv> <weights> <impacts> <output.csv>")
        exit(0)
    else:
        path = os.getcwd()
        file = sys.argv[1]
        if not (os.path.isfile(file)):  
            print("Error: Input file doesn't exist")
            exit(0)
        
        df = pd.read_csv(sys.argv[1])

        weight = sys.argv[2]
        imp=sys.argv[3]
        output = sys.argv[4]

        topsis(df,weight,imp,output)


if __name__ == '__main__':
    outfunc()