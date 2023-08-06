import pandas as pd
import os
import sys

def main():
    # Arguments not equal to 5
    if len(sys.argv) != 5:
        print("wrong number of parameters")
        exit(1)

    # if file deos not exist
    elif not os.path.isfile(sys.argv[1]):
        print(f"{sys.argv[1]} does not exist!!")
        exit(1)

    # if file is not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"{sys.argv[1]} is not csv!!")
        exit(1)

    else:
        dataset, data = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        col = len(data.columns.values)

        # less then 3 columns in input dataset
        if col < 3:
            print(f"{sys.argv[1]} has less than 3 columns")
            exit(1)

        # Handeling non-numeric values
        for i in range(1, col):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and impact arrays
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("error in weights array please try again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("error in impact array please try again")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if col != len(weights)+1 or col != len(impact)+1:
            print("number of weights, number of impacts and number of columns are not same")
            exit(1)

        #if output file is not csv
        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("Output file extension must be csv")
            exit(1)

        #if output file already exists 
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])

        # vector normalisation
        for i in range(1, col):
            temp = 0
            for j in range(len(data)):
                temp = temp + data.iloc[j, i]**2
            temp = temp**0.5
            for j in range(len(data)):
                data.iat[j, i] = (
                    data.iloc[j, i] / temp)*weights[i-1]
        

        # finding ideal best and ideal worst
        ideal_best = (data.max().values)[1:]
        ideal_worst = (data.min().values)[1:]
        for i in range(1, col):
            if impact[i-1] == '-':
                ideal_best[i-1], ideal_worst[i-1] = ideal_worst[i-1], ideal_best[i-1]

        # calculating topsis score
        topsis_score = []
        for i in range(len(data)):
            euc_distp, euc_distn = 0, 0
            for j in range(1, col):
                euc_distp = euc_distp + (ideal_best[j-1] - data.iloc[i, j])**2
                euc_distn = euc_distn + (ideal_worst[j-1] - data.iloc[i, j])**2
            euc_distp, euc_distn = euc_distp**0.5, euc_distn**0.5
            topsis_score.append(euc_distn/(euc_distp + euc_distn))
        dataset['Topsis Score'] = topsis_score

        # calculating the rank 
        dataset['Rank'] = (dataset['Topsis Score'].rank(method='max', ascending=False))
        dataset = dataset.astype({"Rank": int})


        # Writing the csv
        dataset.to_csv(sys.argv[4], index=False)
        


if __name__ == "__main__":
    main()