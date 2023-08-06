import sys
import copy
import numpy as np
import os.path
import pandas as pd
import topsispy as tp
from pandas.api.types import is_numeric_dtype

def main():
    
    if(os.path.exists(sys.argv[1])==False):
        print("File Doesn't Exist")
        exit(1)

    if len(sys.argv)!=5:
        print("No. Of Arguments Needed - 5")
        exit(1)

    i=pd.read_csv(sys.argv[1])

    if len(i.columns)<3:
        print("No, of Columns Required -> Atleast 3")
        exit(1)

    for j in range(1,len(i.columns)):
        if(is_numeric_dtype(i.iloc[:,j])==False):
            print("One or More Column Doesn't have all numeric values")

    df = pd.read_csv(sys.argv[1])

    sys.argv[2] = sys.argv[2].split(',')
    sys.argv[2] = [int(i) for i in sys.argv[2]]

    sys.argv[3] = sys.argv[3].split(',')

    for j in range(len(sys.argv[3])):
        if sys.argv[3][j]=="+" or sys.argv[3][j]=="-":
            continue
        else:
            print("Required Symbols -> + or - ")
            exit(1)

    sys.argv[3] = list(map(lambda x:x.replace('+','1'),sys.argv[3]))
    sys.argv[3] = list(map(lambda x:x.replace('-','-1'),sys.argv[3]))
    sys.argv[3] = [int(i) for i in sys.argv[3]]

    if((len(sys.argv[2])==len(sys.argv[3]) and len(sys.argv[2])==len(i.columns)-1)==False):
        print("Reqd. Condition -No. of weights = No. of impacts = No. of columns (2 to last)")
        exit(1)

    table=i.drop(columns=['Fund Name'])
    arr = table.to_numpy()
    topsis = tp.topsis(arr, sys.argv[2], sys.argv[3])
    table = pd.DataFrame(arr)
    table.insert(0,"Fund Name",i["Fund Name"])
    table = table.rename(columns={0:"P1",1:'P2',2:'P3',3:'P4',4:'P5'})
    table['Topsis Score'] = topsis[1]
    ranks = []
    copy_list = copy.deepcopy(topsis[1])
    copy_list = np.array(copy_list)
    copy_list = -np.sort(-copy_list)
    for i in range(len(topsis[1])):
        ele = topsis[1][i]
        ranks.append(np.where(copy_list==ele)[0][0]+1)

    table['Rank'] = ranks
    table.to_csv(sys.argv[4])

if __name__=='__main__':
    main()