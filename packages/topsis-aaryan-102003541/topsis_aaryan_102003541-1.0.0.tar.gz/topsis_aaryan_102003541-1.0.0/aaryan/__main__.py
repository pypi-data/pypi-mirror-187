import pandas as pd
import numpy as np
import os
import sys

def main():
    # Arguments not equal to 5
    if len(sys.argv)!=5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python <file_name>.py <input_file_name>.csv <weights>(1,1,1,1) <impacts>(+,+,-,+) <output_file_name>.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} File Does not exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR :oops!! {sys.argv[1]} is not a csv file!!")
        exit(1)
    else:
        argumentList=sys.argv[:]
        impacts=argumentList[3].split(",")
        a=argumentList[1]
        dataset=pd.read_csv(a)
        nCol = len(dataset.columns.values)
        if nCol < 3:
            print("ERROR : Please Check Input file have less then 3 columns requires more than 3")
            exit(1)
        # Handling non-numeric value
        
        for i in range(1, nCol):
            # dataset.iloc[:, i].fillna((dataset.iloc[:, i].mean()), inplace=True)
            try:
                temp = np.array(dataset.iloc[:,i].values,dtype='float64')
            except:
                print(dataset.iloc[:,i])
                print("oops!! there is non-numeric values in input file")
                exit(1)
        # pd.to_numeric(dataset.iloc[:, i], errors='coerce')
        # dataset.iloc[:, i].fillna((dataset.iloc[:, i].mean()), inplace=True)
        # Handling errors of weighted and impact arrays
        try:
            w = [float(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again whether entered correctly or not")
            exit(1)
        for i in impacts:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again whether entered correctly or not")
                exit(1)
        # Checking number of column,weights and impacts is same or not
        if nCol != len(w)+1 or nCol != len(impacts)+1:
            print(
                "ERROR :Please check Number of weights, number of impacts and number of columns in input file are not same")
            exit(1)
        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])


        data1=dataset.iloc[:,1:].values
        normalized_matrix = data1 / (np.sum(data1**2, axis=0)**0.5)
        w=np.array(w)
        weighted_matrix=normalized_matrix*w
        pos_ideal_solution = np.amax(weighted_matrix, axis=0) 
        neg_ideal_solution = np.amin(weighted_matrix, axis=0)
        impacts=np.array(impacts)
        for i in range(len(impacts)):
            if impacts[i]=='-':
                pos_ideal_solution[i],neg_ideal_solution[i]=neg_ideal_solution[i],pos_ideal_solution[i]
        pos_distance =(np.sum((weighted_matrix - pos_ideal_solution)**2, axis=1)**0.5)
        neg_distance = (np.sum((weighted_matrix - neg_ideal_solution)**2, axis=1)**0.5)
        topsis_score=neg_distance/(neg_distance+pos_distance)
        dataset["Topsis Score"]=topsis_score
        dataset['Rank'] = (dataset['Topsis Score'].rank(method='max', ascending=False))
        dataset = dataset.astype({"Rank": int})
        dataset.to_csv(sys.argv[4], index=False)


if __name__ == "__main__":
    main()