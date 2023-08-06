import os
import sys
import pandas as pd
import numpy as np

def topsis(df_og, w, i, result_file_name):
    df = df_og.copy()
    df.drop(df.columns[[0]], axis=1, inplace=True)

    df.loc[len(df.index)] = df.apply(lambda x: np.sqrt(sum(x**2)), axis=0)
    df.iloc[:-1, :]=df.apply(lambda x: x[:-1] / x[len(x)-1])
    df.drop(len(df.index)-1, axis=0, inplace=True)

    df = df.apply(lambda x: x*w, axis=1)

    df.loc[len(df.index)] = i
    ib = df.apply(lambda x: x[:-1].max() if x[len(x)-1] == '+' else x[:-1].min())
    iw = df.apply(lambda x: x[:-1].min() if x[len(x)-1] == '+' else x[:-1].max())
    df.drop(len(df.index)-1, axis=0, inplace=True)

    eib = df.apply((lambda x: np.sqrt(sum((x - ib)**2))), axis=1)
    eiw = df.apply((lambda x: np.sqrt(sum((x - iw)**2))), axis=1)

    df_og['TopsisScore'] = (eiw / (eib + eiw)).round(6)
    df_og['Rank'] = df_og['TopsisScore'].rank(ascending=False)

    df_og.to_csv('./'+result_file_name, index=False)

def col_numeric(x):
    if x.dtype.kind in 'iuf':
       pass
    else:
        print('Column has non numeric values')
        exit(1)    

def cmd_args():
    num_arg = len(sys.argv)

    if num_arg != 5:
        print('Wrong number of arguments')
        print('Format of command line input-\npython [package name] [path of data csv as string] [weights as string seperated by ","] [impacts as string seperated by ","]')
    else:        
        data_file_path = sys.argv[1]
        w = sys.argv[2].replace(' ', '')
        i = sys.argv[3].replace(' ','')
        w = list(map(float, w.split(',')))
        i = list(map(str, i.split(',')))
        result_file_name = sys.argv[-1]
        
        try:
            if os.path.exists(data_file_path):pass
        except OSError as err:
            print(err.reason)
            exit(1)
        
        df_og = pd.read_csv(data_file_path)
        
        if len(df_og.columns())-1 < 3:
            print('Input columns are less than 3')
            exit(1)
        
        df_og.iloc[:, 1:].apply(col_numeric)
        
        if len(w) != len(df_og)-1:
            print('Number of value in wieghts and column mismatch')
            exit(1)
        elif len(i) != len(df_og)-1:
            print('Number of value in impacts and column mismatch')
            exit(1)
        
        for y in i:
            if y not in ('+', '-'):
                print('Impact value wrong')
                exit(1)
        
        topsis(df_og, w, i, result_file_name)

if __name__ == '__main__':
    cmd_args()    