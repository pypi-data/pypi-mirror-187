import pandas as pd
import numpy as np
import logging
import sys
# reading the CSV file
# logging.basicConfig(filename="101903244-log.log",level = logging.DEBUG,encoding='utf-8')

# n=len(sys.argv)
# inputFile= sys.argv[1]
# weight=sys.argv[2]
# impact=sys.argv[3]
# outputFile=sys.argv[4]

# csvFile = pandas.read_csv('102003687-data.csv')
def topsis(inputFile,weight,impact,outputFile):
    # logging.basicConfig(filename="101903244-log.log",level = logging.DEBUG,encoding='utf-8')
    if ',' not in weight:
        logging.error("Array weights should be separated by ','")
        return
    
    weight = weight.split(',')
    try:
        weight = list(map(int,weight))
    except ValueError:
        logging.error("Weights has non integral value")
        return

    if ',' not in impact:
        logging.error("Array impacts should be separated by ','")
        return
    impact = impact.split(',')
    # outfile = args[4]


    for x in impact:
        if x != '+' and x != '-':
            logging.error("Impact must contain only '+' or '-'")
            return

    try:
         csvFile = pd.read_csv(inputFile)
    except FileNotFoundError:
        logging.error("Input file provided not found")
        return
    df = csvFile.iloc[:,1:]
    (r,c)=df.shape
    if(c != len(weight) or c != len(impact)):
        logging.error("Length of inputs not match.")
        return
    if(c < 3):
        logging.error("Less Number of columns in Input File")
        return
    # impact = impact.split(',')
    for i in range(r):
        rows = list(df.iloc[i])
        for j in range(c):
            try:
                rows[j] = pd.to_numeric(rows[j])
            except ValueError:
                logging.error(f"Non numeric value encountered in input.csv at {i}th row and {j}th coln")
                return
    # weight=weight.split(',')
    for i in range(0,len(weight)):
        if(impact[i]=='+'):
            weight[i]=int(weight[i])
        else:
            weight[i]=int(weight[i])*-1

    squaresum=[]
    for i in range(0,c):
        sum=0
        for j in range(0,r):
            sum+=df.iloc[j,i]**2
        squaresum.append(sum**0.5)

    for i in range(0,c):
        sum=0
        for j in range(0,r):
            df.iloc[j,i]=df.iloc[j,i]/squaresum[i]

    for i in range(0,c):
        sum=0
        for j in range(0,r):
            df.iloc[j,i]=df.iloc[j,i]*weight[i]

    vinegative=[]
    vipositive=[]
# vineg=100000000
# vipos=-100000000
    for i in range(0,c):
        vineg=100000000
        vipos=-100000000
        for j in range(0,r):
            vineg=min(vineg,df.iloc[j,i])
            vipos=max(vipos,df.iloc[j,i])
        vinegative.append(abs(vineg))
        vipositive.append(abs(vipos))

    sinegative=[]
    sipositive=[]
    for i in range(0,r):
        sum1=0
        sum2=0
        for j in range(0,c):
            sum1+=(df.iloc[i,j]-vipositive[j])**2
            sum2+=(df.iloc[i,j]-vinegative[j])**2
        sipositive.append(sum1**0.5)
        sinegative.append(sum2**0.5)

    topsis_score=[]
    for i in range(0,r):
        topsis_score.append(sinegative[i]/(sinegative[i]+sipositive[i]))

    array=np.array(topsis_score)
    order=array.argsort()
    ranks=order.argsort()
    ranks=ranks+1

    csvFile['Topsis Score'] = topsis_score
    csvFile['Rank'] = ranks
    csvFile.to_csv(outputFile)

