from inspect import EndOfBlock
import numpy as np
import pandas as pd
import sys
import csv

def topsis(data, weights, impact):
    try:
        # Normalize the data
        data = data / np.linalg.norm(data, axis=0)
        # Multiply each criterion by its weight and impact
        data = data * weights *impact
        # Calculate the ideal solution
        ideal_solution = np.max(data,axis=0)
        ideal_solution2 = np.min(data,axis=0)

        # Calculate the relative closeness to the ideal solution
        relative_closeness1 = np.sqrt(np.sum((data - ideal_solution) ** 2, axis=1))
        relative_closeness2 = np.sqrt(np.sum((data - ideal_solution2) ** 2, axis=1))
        relative_closeness=relative_closeness2/(relative_closeness1+relative_closeness2)
            
        return relative_closeness
    except Exception as e:
        print("An error occurred:", e)
        return None
    
if __name__ == '__main__':
    try:
        # Read input file name from command line
        input_file = sys.argv[1] 
        # Read data from CSV file
        data = pd.read_csv(input_file,skiprows=0,index_col=0).values
        if(len(data[0])<2):
          print("Too less number of columns")
          sys.exit(1)
        
        # Read weight and impact from command line arguments
        weights = list(map(float, sys.argv[2].split(',')))
        impact = list(map(str, sys.argv[3].split(',')))
        if(len(weights)!=len(impact) or len(weights)!=len(data[0]) or len(impact)!=len(data[0])):
          print("Lengths of impact and weight must be equal to number of columns.")
          sys.exit(1)
        for i in range(0,len(impact)):
          if(impact[i]=="+"):
            impact[i]=1
          elif (impact[i]=="-"):
            impact[i]=-1
          else:
            print("Incorrect syntax for impacts") 
            sys.exit(1)
           
          
        # Perform TOPSIS analysis
        relative_closeness = topsis(data, weights, impact)
        if relative_closeness is not None:
            # write the output to a csv file
            np.savetxt(sys.argv[4], relative_closeness, delimiter=",",header="Topsis_score",comments="")
            df1=pd.read_csv(sys.argv[1])
            df=pd.read_csv(sys.argv[4])
            df = df.assign(Rank=df['Topsis_score'].rank(ascending=False))
            df3=df1.join(df)
            df3.to_csv(sys.argv[4],index=False)
            print("Output written successfully")
        else:
            print("An error occurred.")
    except Exception as e:
        print("An error occurred:", e)