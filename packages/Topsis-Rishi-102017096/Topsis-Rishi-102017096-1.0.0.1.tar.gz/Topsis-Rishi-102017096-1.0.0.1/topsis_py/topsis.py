import pandas as pd
import numpy as np
import math
import sys


#Handling input arguments
def main():
    if len(sys.argv) != 5:
        print('Please provide complete 5 arrguments')
        sys.exit()

    #Exception handling for command line arguments
    try:
        filename = sys.argv[1]
        weights = sys.argv[2]
        impact = sys.argv[3]
        output_filename = sys.argv[4]

        for i in weights:
            try:
                #for decimal value of weights
                float(i)
            except:
                if i not in [',','.']:
                    print('Weights must be a comma separated list of numbers')
                    sys.exit()
        for i in impact:
            if i not in ['+', '-', ',']:
                print("Impact must me comma sepearted")
                sys.exit()
        weights = weights.split(",")
        #for weights in decimal value
        weights = [float(x) for x in weights]
        impact = impact.split(",")
    except:
        print("Input values are invalid")
        sys.exit()
    # handling impact +,- values
    flag = False
    for i in impact:
        if (i != '+' and i != '-'):
            flag = True
            break
    if flag == True:
        print("Impacts must be either +ve or -ve.")
        sys.exit()
    # handling input file
    try:
        my_dataframe = pd.read_csv(filename)
    except:
        print("File Not Found")
        sys.exit()
    # print(df)
    df = my_dataframe.iloc[:, 1:].copy(deep=False)
    typedf = df.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())

    for i in typedf:
        if i == False:
            print("All Value must be numeric ")
            sys.exit()


    # Array of root mean square value of all columns
    rms = {}
    r = len(df)
    c = len(df.columns)
    # handling number of columns
    if c < 3:
        print("Input file must contain three or more columns")
        sys.exit()
    if len(weights) != c:
        print("Weight values are insufficient")
        sys.exit()
    if len(impact) != c:
        print("Impact values are insufficient")
        sys.exit()


    df.astype(float)
    for i in df:
        df[i].astype(float)

    for i in df:
        sum = 0
        for j in df[i]:
            sum = sum+j*j
        rms[i] = sum

    for i in rms:
        rms[i] = math.sqrt(rms[i])
    # print(rms)
    
    for i in df:
        for j in range(0, r):
            df[i][j] = float(df[i][j]/rms[i])

    idx = 0
    for i in df:
        w = weights[idx]
        for j in range(0, r):
            df[i][j] = w*df[i][j]
        idx = idx+1


    ideal_best = {}
    ideal_worst = {}

    idx = 0
    for i in df:
        if impact[idx] == "+":
            ideal_best[i] = df[i].max()
            ideal_worst[i] = df[i].min()
        if impact[idx] == "-":
            ideal_best[i] = df[i].min()
            ideal_worst[i] = df[i].max()
        idx = idx+1


    eucd_1 = []
    eucd_2 = []

    # Formation of normalized decison matrix
    for i in range(0, r):
        temp_p = 0
        temp_n = 0
        for j in df:
            best = ideal_best[j]
            worst = ideal_worst[j]
            temp_p = temp_p+(df[j][i]-best)*(df[j][i]-best)
            temp_n = temp_n+(df[j][i]-worst)*(df[j][i]-worst)
        eucd_1.append(math.sqrt(temp_p))
        eucd_2.append(math.sqrt(temp_n))


    # topsis score
    pscore = []

    for i in range(0, r):
        pscore.append(
            eucd_2[i]/(eucd_2[i]+eucd_1[i]))

    rank = {}

    pscore_sorted = np.sort(pscore)[::-1]

    for i in range(len(pscore_sorted)):
        rank[pscore_sorted[i]] = i+1


    ranks = []

    for i in pscore:
        y = rank[i]
        ranks.append(y)

    print(ranks)
    my_dataframe["Topsis_Score"] = pd.Series(pscore)
    my_dataframe["Rank"] = pd.Series(ranks)
    my_dataframe.to_csv(output_filename)
    print(my_dataframe)

if __name__ == '__main__':
    main()

# Rishi Malik
# 102017096
# CS5