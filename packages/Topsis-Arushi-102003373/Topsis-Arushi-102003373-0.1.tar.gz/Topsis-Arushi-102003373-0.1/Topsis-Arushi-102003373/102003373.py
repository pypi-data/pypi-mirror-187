import pandas as pd
import os
import sys


def main():
    if len(sys.argv) != 5:
        print("error:number of parameters")
        print("try: python 102003373.py 102003373-data.csv '1,1,1,1,1' '+,+,-,+,-' 102003373-result.csv ")
        exit()
    
    elif not os.path.isfile(sys.argv[1]):
        print(f"error:{sys.argv[1]} don't exist")
        exit()

    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"error:{sys.argv[1]} is not csv")
        exit()

    else:
        output, input = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])
        col = len(input.columns.values)

        if col < 3:
            print("error:Input file have less then 3 columns")
            exit()

        for i in range(1, col):
            pd.to_numeric(output.iloc[:, i], errors='coerce')
            output.iloc[:, i].fillna(
                (output.iloc[:, i].mean()), inplace=True)
    
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("error:In weights array please check again")
            exit()
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("error:In impact array please check again")
                exit()

        if col != len(weights)+1 or col != len(impact)+1:
            print("error:Number of weights, number of impacts and number of columns not same")
            exit()

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("error:output file extension is wrong")
            exit()
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        topsis_pipy(input, output, col, weights, impact)


def normalize(input, col, weights):
    for i in range(1, col):
        temp = 0
        for j in range(len(input)):
            temp = temp + input.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(input)):
            input.iat[j, i] = (
                input.iloc[j, i] / temp)*weights[i-1]
    return input


def cal(input, col, impact):
    sp = (input.max().values)[1:]
    sm = (input.min().values)[1:]
    for i in range(1, col):
        if impact[i-1] == '-':
            sp[i-1], sm[i-1] = sm[i-1], sp[i-1]
    return sp, sm


def topsis_pipy(input, output, col, weights, impact):
    input = normalize(input, col, weights)

    sp, sm = cal(input, col, impact)

    score = []
    for i in range(len(input)):
        temp_p, temp_n = 0, 0
        for j in range(1, col):
            temp_p = temp_p + (sp[j-1] - input.iloc[i, j])**2
            temp_n = temp_n + (sm[j-1] - input.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    output['Topsis Score'] = score

    output['Rank'] = (output['Topsis Score'].rank(method='max', ascending=False))
    output = output.astype({"Rank": int})

    output.to_csv(sys.argv[4], index=False)


if __name__ == "__main__":
    main()