import sys
import logging
import os.path
from os import path
import pandas as pd
import math

def root_mean_square(df, collen):
    rms = (df**2).mean(axis=0)**0.5
    return rms

def normalised_decision_matrix(df, collen, rms):
    npv = df.div(rms, axis=1)  
    return npv 

def weight_assignment(npv, w, collen):
    w = [float(x) for x in w]
    npv = npv.mul(w, axis=1)
    return npv

def ideal_values(npv, collen, imp):
    vp = []
    vn = []
    for i in range(0, collen):
        m = []
        for j in range(0, len(npv.index)):
            m.append(npv.iloc[j, i])
        if imp[i] == '+':
            vp.append(max(m))
            vn.append(min(m))
        else:
            vp.append(min(m))
            vn.append(max(m))
    return vp, vn   

def cal_euclidean_dist(npv, collen, vp, vn):
    sp = []
    sn = []

    for i in range(0, len(npv.index)):
        a = 0
        b = 0
        for j in range(0, collen):
            a = a + (npv.iloc[i, j] - vp[j]) ** 2
            b = b + (npv.iloc[i, j] - vn[j]) ** 2
        sp.append(math.sqrt(a))
        sn.append(math.sqrt(b))
    return sp, sn  

def cal_performance(sp, sn, rowlen):
    p = []
    for i in range(0, rowlen):
        a = sp[i] + sn[i]
        p.append(sn[i] / a)
    return p       

def main():
    if len(sys.argv) != 5:
        logging.exception("Error! minimum of 5 paramters are required\nUsage: python file.py <filename1.csv> <Weights> <Impacts> <resultfile.csv>")
        exit(0)

    filename = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result_path = sys.argv[4]

    if not path.isfile(filename):
        raise Exception("File %s does not exist, provide the correct path" %(filename))

    df = pd.read_csv(filename)
    df = df.set_index(df['Fund Name'])
    df.drop(df.columns[0],inplace = True, axis=1)

    if len(df.columns) < 3:
        raise Exception("File %s does not have enough columns" % (filename))

    try:
        w = weights.split(',')
    except:
        logging.exception("The weights are not seperated by ','.") 

    try:
        imp = impacts.split(',')
    except:
        logging.exception("The impacts are not seperated by ','.")           

    if (len(w) == len(imp) and len(w) == len(df.columns)):
        pass
    else:
        raise Exception("Length of Weights,Impacts and dataframe columns from 2nd to last are not same")

    for i in range(len(imp)):
        if imp[i] == "+" or imp[i] == "-":
            pass
        else:
            raise Exception("Impacts have not all the values of '+' or '-' only")    

    rms = root_mean_square(df, len(df.columns))
    normalized_matrix = normalised_decision_matrix(df, len(df.columns), rms)
    weight_matrix = weight_assignment(normalized_matrix, w, len(df.columns))
    best_list, worst_list = ideal_values(weight_matrix, len(df.columns), imp)
    s_plus, s_minus = cal_euclidean_dist(weight_matrix, len(df.columns), best_list, worst_list)
    performace_score = cal_performance(s_plus, s_minus, len(df.index))

    df['Topsis Score'] = performace_score
    df['Rank'] = df['Topsis Score'].rank(ascending=False)
    df.index.name = 'Fund Name'
    df.reset_index(inplace=True)
    df.to_csv(result_path, index=False)


if __name__ == "__main__":
    main()