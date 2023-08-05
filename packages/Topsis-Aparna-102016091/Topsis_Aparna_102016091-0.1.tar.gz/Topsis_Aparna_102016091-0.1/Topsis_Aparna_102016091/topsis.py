import numpy as np
import pandas as pd
import sys
import math as m

def topsisscore(initialfilename,weights,impacts,outputfilename):
    if(initialfilename.split('.')[-1]!='csv'):
        print("File extension not supported")
        exit(0)
    #Handling file not found exception
    try:
        dataset = pd.read_csv(initialfilename)
    except:
        print(f'File not found')
        sys.exit(0)
    #Handling columns less than 3 exception
    if len(dataset.columns)<3:
        print("Input file must contai 3 or more columns")
        sys.exit(0)
    #Handling weights not equal to number of columns exception
    if len(weights.split(','))!=len(dataset.columns)-1:
        print("Number of weights must be equal to number of columns")
        sys.exit(0)
    #Handling impacts not equal to number of columns exception
    if len(impacts.split(','))!=len(dataset.columns)-1:
        print("Number of impacts must be equal to number of columns")
        sys.exit(0)
    #Handling invalid impacts exception
    for i in impacts.split(','):
        if i!='+' and i!='-':
            print("Invalid impact")
            sys.exit(0)
    #Handling invalid weights exception
    for i in weights.split(','):
        if float(i)<0:
            print("Invalid weight")
            sys.exit(0)
    #Handling invalid output file name exception
    if outputfilename.split('.')[-1]!='csv':
        print("Invalid output file name")
        sys.exit(0)
    #Handling invalid input file name exception
    if initialfilename.split('.')[-1]!='csv':
        print("Invalid input file name")
        sys.exit(0)
    
    org_data=dataset.copy(deep=True)
    dataset = dataset.drop(dataset.columns[0],axis=1)
    dataset
    weights=pd.to_numeric(weights.split(','))

    for i in range(0,len(dataset.columns)):
            temp = 0
            for j in range(len(dataset)):
                temp = temp + dataset.iloc[j,i]**2
            temp=m.sqrt(temp)
            for j in range(len(dataset)):
                dataset.iloc[j,i]=(dataset.iloc[j,i]/temp)*weights[i-1]
                
    normalised=dataset
    bestValue = normalised.max().values
    worstValue = normalised.min().values
    impacts=impacts.split(',')
    ideal_array=[]
    for i in range(len(bestValue)):
        if impacts[i]=='+':
            ideal_array.append([bestValue[i],worstValue[i]])
        else:
            ideal_array.append([worstValue[i],bestValue[i]])
    ideal_array = np.array(ideal_array)
    ideal_array
    pos=[]
    neg=[]
    score = []

    for i in range(len(normalised)):
        temp_pos=0
        temp_neg=0
    
        for j in range(len(normalised.columns)):
            temp_pos=temp_pos + (ideal_array[j,0]-normalised.iloc[i,j])**2
            temp_neg = temp_neg + (ideal_array[j,1]-normalised.iloc[i,j])**2
        temp_pos=temp_pos**0.5
        temp_neg=temp_neg**0.5
        pos.append(temp_pos)
        neg.append(temp_neg)
        score.append(temp_neg/(temp_neg+temp_pos))
    org_data['topsis score']=score
    org_data['rank']=org_data['topsis score'].rank(method='max',ascending=False)
    org_data.to_csv(outputfilename)



if __name__ == "__main__":
    if(len(sys.argv)!=5):
        print("Invalid number of arguments")
        sys.exit(0)
    topsisscore(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])