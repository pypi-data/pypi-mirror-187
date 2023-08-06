import pandas as pd
import numpy as np
import sys

def evaluate(data, weights, impact):
    r = len(data.axes[0])
    c = len(data.axes[1])

    squaresum = []
    for i in range(1,c) : 
        tempsum = 0.0
        for j in range (0,r):
            tempsum = tempsum + pow(data.iloc[j][i],2)
        squaresum.append(pow(tempsum,0.5)) #root of sums

    data2 = pd.DataFrame(index=range(0,r),columns=range(0,c-1))

    ##Normalised Matrix
    for i in range (1,c):
        for j in range (0,r):
            data2.iloc[j][i-1] = data.iloc[j][i]/squaresum[i-1]

    #weighted normalised vector
    for i in range (0,r): 
        for j in range (0,c-1):
            data2[j][i] =  data2[j][i]*weights[j]

    Vjp=[]
    for j in range (0,c-1):
        if(impact[j]=='+'):
            Vjp.append(max(data2[j]))
        elif(impact[j]=='-'):
            Vjp.append(min(data2[j]))

    Vjn=[]
    for j in range (0,c-1):
        if(impact[j]=='+'):
            Vjn.append(min(data2[j]))
        elif(impact[j]=='-'):
            Vjn.append(max(data2[j]))

    Sip=[]
    for i in range(0,r):
        temp = 0.0
        for j in range(0,c-1):
            temp = temp + pow(Vjp[j]-data2[j][i],2)
        Sip.append(pow(temp,0.5))

    Sin=[]
    for i in range(0,r):
        temp = 0.0
        for j in range(0,c-1):
            temp = temp + pow(Vjn[j]-data2[j][i],2)
        Sin.append(pow(temp,0.5))

    P =[] # performance score
    for i in range(0,r):
        P.append(Sin[i]/(Sin[i]+Sip[i]))

    ranks=[]
    from scipy.stats import rankdata
    rankdata(P, method='max')
    t = len(P) - rankdata(P, method="max") + 1
    for i in range(0,r):
        ranks.append(t[i])

    output = pd.DataFrame(list(zip(P, ranks)),columns =['Topsis Score', 'Ranks'])

    horizontal_concat = pd.concat([data, output], axis=1)
    return horizontal_concat

def main():
    n = len(sys.argv)
    if(n!=5):
        print('Incorrect Parameters')
        print('Enter <program.py> <InputDataFile.csv> <Weights> <Impacts> <ResultFileName.csv>')
        exit(0)
    #print(n)
    #print("\nName of Python script:", sys.argv[0])

    InputDataFile = sys.argv[1]
    w = sys.argv[2]
    im = sys.argv[3]
    ResultFileName = sys.argv[4]
    
    try:
        data = pd.read_csv(InputDataFile)
       
    except IOError:
       print ("There was an error reading", InputDataFile)
       sys.exit(0)
   
    weights = []
    for i in w:
        if(i!=','):
            weights.append(int(i))

    impact = []
    for i in im:
        if(i!=','):
            impact.append(i)
        if(i!="+" and i!="-" and i!=","):
            print('Impacts should be either + or - separated by ,')
            exit(0)


    col = len(data.axes[1])
    if col<=2:
        print('Input file must contain 3 or more columns')
        exit(0)
    if not ((len(weights)==len(impact)==col-1)):
        print('Check number of weights, impacts and number of columns in data. All 3 should be equal')
        exit(0)

    res = evaluate(data,weights,impact)
    print(res)
    res.to_csv(ResultFileName)


if __name__ == "__main__":
    main()