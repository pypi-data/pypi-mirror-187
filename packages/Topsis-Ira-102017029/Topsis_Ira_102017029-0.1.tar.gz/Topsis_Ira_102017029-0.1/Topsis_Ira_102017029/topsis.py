import sys
import pandas as pd
import numpy as np
import os
def topsis(A,weight,s) :
    data=A.copy()
    r=data.shape[0]
    c=data.shape[1]

    if c<3 :
        print("Error - Number of Rows are less than 3")
        exit(0)

    x=data.iloc[:,1:c]
    w1=list()
    w=list()
    length=len(weight)
    str=""
    for i in weight :
        if i!=',' :
            str=str+i
        else :
            w1.append(str)
            str=""
    w1.append(str)
    for i in w1 :
        w.append(float(i))
    
    if len(w)!=c-1:
        print("Error : Weight count is not correct ")
        exit(0)
    a=list()
    for i in range(0,c-1) :
        sum=0
        for j in range(0,r) :
            sum=sum+x.iloc[j,i]*x.iloc[j,i]
        a.append(sum**0.5)
    for i in range(0,c-1) :
        for j in range(0,r) :
            x.iloc[j,i]=x.iloc[j,i]*w[i]/a[i]
    impact=list()
    imp=s
    for i in imp:
        if i!=',' :
            impact.append(i)
    if len(impact)!=c-1:
        print("Error : Impact count is not correct ")
        exit(0)
    v1=list()
    v2=list()
    for i in range(0,c-1) :
        m1=x.iloc[0,i]
        m2=x.iloc[0,i]
        for j in range(1,r) :
            if m1<x.iloc[j,i] :
                m1=x.iloc[j,i]
            if m2>x.iloc[j,i] :
                m2=x.iloc[j,i]
        if impact[i]=='+':
            v1.append(m1)
            v2.append(m2)
        elif impact[i]=='-' :
            v1.append(m2)
            v2.append(m1)
        else :
            print("Error : Contain symbols other than +,-")
            exit(0)
    s1=list()
    s2=list()
    p=list()
    for i in range(0,r) :
        sum1=0
        sum2=0
        for j in range(0,c-1) :
            sum1=sum1+(x.iloc[i,j]-v1[j])**2
            sum2=sum2+(x.iloc[i,j]-v2[j])**2
        s1.append(sum1**0.5)
        s2.append(sum2**0.5)
        p.append(sum2**0.5/(sum1**0.5+sum2**0.5))
    p= pd.DataFrame(p)
    ranks=p.rank()
    for i in range (0,r) :
        ranks.iloc[i][0]=int(r+1-ranks.iloc[i][0])
    A['Topsis Score'] = p
    A['Rank'] = ranks
    print(A)

def cli_output():
    #print("ii")
    if len(sys.argv) != 5:
        print('Wrong Number of args')
        print('Input should be like - \n '
              'python [package name] [path of csv as string] [list of weights as string] [list of sign as string]')
    else:
        file_path = sys.argv[1]
        try:
            if os.path.exists(file_path):
                print('Path exist')
        except OSError as err:
            print(err.reason)
            exit(1)


        df = pd.read_csv(file_path)
        w = sys.argv[2]
        s= sys.argv[3]
        topsis(df, w, s)

if __name__ == '__main__':
    cli_output()