import pandas as pd
import numpy as np
import sys
import os
import logging

def main():
    # Arguments not equal to 5
    if len(sys.argv) != 5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python 102017169.py 102017169-data.csv '1,1,1,1' '+,+,-,+' final_dataset.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        final_dataset, input_file = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        #Drop 1st column
        input_file=input_file.drop(['Fund Name'],axis=1)
        #Convert to matrix
        input_file=input_file.to_numpy()
        m,n=input_file.shape
    

        # less then 3 columns in input dataset
        if n < 3:
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        # Handeling non-numeric value
    
        for i in range(1,n):
            pd.to_numeric(final_dataset.iloc[:, i], errors='coerce')
            final_dataset.iloc[:, i].fillna(
                (final_dataset.iloc[:, i].mean()), inplace=True)
       

        #Handling errors of weighted and impact arrays
        try:
            weight = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again")
            exit(1)
        impacts = sys.argv[3].split(',')
        for i in impacts:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again")
                exit(1)
        
        # Checking number of column,weights and impacts is same or not
        if n != len(weight) or n != len(impacts):
            print(
                "ERROR : Number of weights, number of impacts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        output_file=sys.argv[4]
        #Applying topsis algorithm
        topsis(input_file,final_dataset,m,n,weight,impacts,output_file)
        
        
sum=[]
def normalise(input_file,m,n,weight):
    for i in range(0,n):
        s=0
        for j in range(0,m):
             s=s+input_file[j][i]*input_file[j][i]
        sum.append(s**0.5)
    for i in range(0,n):
        for j in range(0,m):
          input_file[j][i]=input_file[j][i]/sum[i]*weight[i]
    return input_file 

def calculate(input_file,m,n,impacts):
    psol=[]
    nsol=[]
    for i in range(n):
        maxm = input_file[0][i]
        for j in range(m):
            if input_file[j][i] > maxm:
                maxm = input_file[j][i]
        psol.append(maxm)
    for i in range(n):
        minm = input_file[0][i]
        for j in range(m):
            if input_file[j][i] < minm:
                minm = input_file[j][i]
        nsol.append(minm)    
    for i in range(n):
        if impacts[i]=='-':
            psol[i],nsol[i]=nsol[i],psol[i]
    return psol,nsol        
  

def topsis(input_file,final_dataset,m,n,weight,impacts,output_file):
    input_file=normalise(input_file,m,n,weight)
    psol,nsol=calculate(input_file,m,n,impacts)
    
    score=[]
    
    
    for i in range(m):
        pdis,ndis=0,0
        for j in range(n):
            pdis=pdis+(input_file[i][j]-psol[j])**2
            ndis=ndis+(input_file[i][j]-nsol[j])**2
        pdis,ndis=pdis**0.5,ndis**0.5
        score.append(ndis/(pdis+ndis))    
    
    final_dataset['Topsis Score'] = score

    # calculating the rank according to topsis score
    final_dataset['Rank'] = (final_dataset['Topsis Score'].rank(
        method='max', ascending=False))
    final_dataset = final_dataset.astype({"Rank": int}) 
    print(final_dataset)
    final_dataset.to_csv(output_file)         

if __name__ == "__main__":
    main()