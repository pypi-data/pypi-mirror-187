import pandas as pd
import os
import sys
        
def idealvalues(temp, col, impact): #calculating positive and negative ideal values
    p_ideal = (temp.max().values)[1:]
    n_ideal = (temp.min().values)[1:]
    for i in range(1, col):
        if impact[i-1] == '-':
            p_ideal[i-1], n_ideal[i-1] = n_ideal[i-1], p_ideal[i-1]
    return p_ideal, n_ideal

def normal(temp, col, weights):  #normalizing array using min-max
    for i in range(1, col):
        temp = 0
        for j in range(len(temp)):
            temp = temp + temp.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp)):
            temp.iat[j, i] = (temp.iloc[j,i]/temp)*weights[i-1]
    return temp

def main():
    if len(sys.argv) != 5:  #if arguments are not equal to 5, throw an error
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)

    elif not os.path.isfile(sys.argv[1]): #if file is not found throw an error
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]: #if file is not in csv format throw an error
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        dataset, temp = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])
        col = len(temp.columns.values)

        if col < 3: #if no of columns is less than 3 throw an error
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        for i in range(1, col): #handling non numeric values (labels and null values)
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna((dataset.iloc[:, i].mean()), inplace=True)

        try:        #handling errors of weighted and impact arrays
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again")
                exit(1)

        if col != len(weights)+1 or col != len(impact)+1:   #if number of columns is not equal to number of weights and impact, throw an error
            print("ERROR : Number of weights, number of impacts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)

        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])

        topsis_pipy(temp, dataset, col, weights, impact)

def topsis_pipy(temp, dataset, col, weights, impact):

    temp = normal(temp, col, weights)

    p_ideal, n_ideal = idealvalues(temp, col, impact)

    score = []
    for i in range(len(temp)):
        pos, neg = 0, 0
        for j in range(1, col):
            pos = pos + (p_ideal[j-1] - temp.iloc[i, j])**2
            neg = neg + (n_ideal[j-1] - temp.iloc[i, j])**2
        pos, neg = pos**0.5, neg**0.5
        score.append(neg/(pos + neg))
    dataset['Topsis Score'] = score

    dataset['Rank'] = (dataset['Topsis Score'].rank(method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})

    dataset.to_csv(sys.argv[4], index=False)

if __name__ == "__main__":
    main()