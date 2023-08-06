# importing libraries
import pandas as pd
from math import pow
import math as m
import string as s
from sklearn import preprocessing
import sys

filename = input("")
weights = input("")
impacts = input("")

def topsis(filename, weights, impact):
    
    # To check whether input file is valid or not
    try:
        file = open(filename)
        topsis_df = pd.read_csv(file, index_col = False)

    except FileNotFoundError:
        sys.exit("\nWrong input file is entered.")
    
    top_df = topsis_df.copy()

    # Calculating number of rows and coloumns
    rows = topsis_df.shape[0]
    cols = topsis_df.shape[1]


    # To check the number of coloumns in input file 
    if cols < 3:
        sys.exit("\nInput file must contain three or more coloumns.")
    
    w_list = weights.split(',')

    # To check whether weights are valid or not
    if len(w_list) != (cols - 1):
        print("\nNo of weight should be",cols-1, "and should be entered comma-separated.")
        sys.exit()

    for v in w_list:
        try:
            v = float(v)
        except:
            sys.exit("\nWeights should be numeric only.")

    impact_list = impact.split(',')

    # To check whether impacts are valid or not
    if len(impact_list) != (cols - 1):
        print("\nNo of impacts should be",cols-1, "and should be entered comma-separated.")
        sys.exit()

    for x in impact_list:
        if x != '+' and  x != '-':
            sys.exit("\nImpacts must be either +ve or -ve")

    # To check the non-numeric coloumns and converting them into numeric
    cat = topsis_df.select_dtypes(include=['object']).columns.tolist()
    cat.pop(0)

    if len(cat) > 0:
        for b in cat:
            label_encoder = preprocessing.LabelEncoder()
            topsis_df[b]= label_encoder.fit_transform(topsis_df[b])


    updated_data = pd.DataFrame()

    i = 1
    res = 0
    k_res = 0


    while i < cols:
        res = 0
        test_list = list(topsis_df.iloc[:, i])
    
        # Calculating root of sum of squares
        for j in test_list:
            res += pow(j, 2)

        res = round(m.sqrt(res),4)    
        
        # Dividing each by RSS and multiplying each with weights
        k_list = []
        for k in test_list:
            k_res = round((k/res),4)
            k_res = round(k_res * float(w_list[i-1]), 4)
            k_list.append(k_res)

        updated_data[i] = k_list

        i += 1

    performance = []
    f = 0
    best = []
    worst = []

    # Calculating ideal best and ideal worst
    while f < updated_data.shape[1]:
        
        if impact_list[f] == '+':
            v_best = (updated_data.iloc[:, f]).max()
            v_worst = (updated_data.iloc[:, f]).min()
        else:
            v_best = (updated_data.iloc[:, f]).min()
            v_worst = (updated_data.iloc[:, f]).max()

        best.append(v_best)
        worst.append(v_worst)

        f += 1


    t = 0
    s_pos = []
    s_neg = []
    joined = [best, worst]

    # Calculating Eucledian Distance
    while t < updated_data.shape[0]:
        v_list1 = list(updated_data.iloc[t,:])

        for z in range(0, len(joined)):
            sum = 0
            for i, j in zip(v_list1, joined[z]):
                a = round((i-j),4)
                a = (a**2)
                sum += a

            b = round(m.sqrt(sum), 4)

            if z == 0:
                s_pos.append(b)
            else:
                s_neg.append(b)

        t += 1

    # Calculating performance score
    performance = []
    for i, j in zip(s_pos, s_neg):
        c = round((j)/(i + j), 6)
        performance.append(c)

    # Topsis Score and Rank
    top_df['Topsis Score'] = performance
    top_df['Rank'] = top_df['Topsis Score'].rank(ascending = False).astype(int)

    print(top_df)

topsis(filename, weights, impacts)