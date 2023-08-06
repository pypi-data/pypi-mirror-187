import os
import pandas as pd
import sys
import logging
def main():
    if len(sys.argv) !=5:
        print("Error : Number of paramters are not correct")
        print("Usage : python program.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)
        
        #File not found error 
    elif not os.path.isfile(sys.argv[1]):
        print(f"Error : {sys.argv[1]} Don't exist!")
        exit(1)
            
         #File not of csv extension   
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"Error : {sys.argv[1]} is not csv file !")
        exit(1)
        
    else:
        dataset=pd.read_csv(sys.argv[1])
        temp_data=pd.read_csv(sys.argv[1])
        col=len(temp_data.columns.values) #no of columns
        
        #less than 3 columns in input file
        if col <3:
            print("Error: Input file have less than 3 columns")
            exit(1)
            
        #Handeling non-numerical values    
        for i in range(1,col):
            pd.to_numeric(dataset.iloc[:,i],errors='coerce')
            dataset.iloc[:,i].fillna((dataset.iloc[:,i].mean()), inplace=True)
            
        #Handling errors of weights and impact
        if ',' not in sys.argv[2]:
            logging.error("Weights should be separated by ','")
            return
        try:
            weights=[int(i) for i in sys.argv[2].split(',')]
        except:
            print("Error: In weights array please check once")
            exit(1)
        
        
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i== '+' or i=='-'):
                print("Error: In impact array please check once,it must contain '+' or '-'")
                exit(1)
        if ',' not in sys.argv[3]:
            logging.error("Impacts should be separated by ','")
            return
        
        #Checking number of columns,weights and impacts
        if col != len(weights)+1 or col != len(impact)+1:
            print("ERROR : Number of weights, number of impacts and number of columns are not same")
            exit(1)
        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR: Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        topsis_pipy(temp_data,dataset,col,weights,impact)
        
        
            
            
           
            
#Normalising the array
def Normalize(temp_data,col,weights):
    for i in range(1,col):
        temp=0
        for j in range(len(temp_data)): #no of rows
            temp= temp +temp_data.iloc[j,i]**2 #sum of squares
        temp=temp**0.5
        for j in range(len(temp_data)):
            temp_data.iloc[j,i]=(temp_data.iloc[j,i]/temp)*weights[i-1]
    return temp_data
#Calculating positive and negative values
def calc(temp_data,col,impact):
    p_val=(temp_data.max().values)[1:]
    n_val=(temp_data.min().values)[1:]
    for i in range(1,col):
        if impact[i-1] == '-':
            p_val[i-1],n_val[i-1] = n_val[i-1],p_val[i-1]
    return p_val,n_val

def topsis_pipy(temp_data,dataset,col,weights,impact):
    #Normalising the array
    #print(temp_data)
    temp_data=Normalize(temp_data,col,weights)
    #Calculating positive and negative values
    p_val,n_val=calc(temp_data,col,impact)
    
    #Calculating topsis score
    finalscore=[]
    for i in range(len(temp_data)):
        temp_p,temp_n=0,0
        for j in range(1,col):
            temp_p=temp_p+(p_val[j-1]-temp_data.iloc[i,j])**2
            temp_n=temp_n+(n_val[j-1]-temp_data.iloc[i,j])**2
        temp_p,temp_n=temp_p*0.5,temp_n*0.5
        finalscore.append(temp_n/(temp_n+temp_p))
    dataset['Topsis Score'] =finalscore
    
    #calculating rank
    dataset['Rank'] = (dataset['Topsis Score'].rank(method='max',ascending=False))
    dataset=dataset.astype({"Rank":int})
    
    #Writing the csv
    dataset.to_csv(sys.argv[4],index=False)
    
    
if __name__=="__main__":
    #print(sys.argv)
     main()
    