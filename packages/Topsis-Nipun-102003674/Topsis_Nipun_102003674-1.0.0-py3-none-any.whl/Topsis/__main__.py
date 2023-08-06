#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 22:58:35 2023

@author: Nipun Garg
"""
import pandas as pd
import numpy as np
import sys
import os

def main():
    if len(sys.argv) != 5:
        print("Incorrect number of parameters")
        exit(0)
    else:
         if os.path.isfile(sys.argv[1])==False:
            print("File not Found ")
            exit(0)
         else:
            topsis_df = pd.read_csv(sys.argv[1])
            col=len(topsis_df.columns)
            
            if col<3:
                print("File must contain 3 or more columns ")
                exit(0)

        # Impacts must be either +ve or -ve.
        # Impacts and weights must be separated by ‘,’ (comma).
            try:
                weights = [int(i) for i in sys.argv[2].split(',')]
            except:
                print("Impacts and weights must be separated by ‘,’ (comma).")
                exit(0)
            impact = sys.argv[3].split(',')
            for i in impact:
                if not (i == '+' or i == '-'):
                    print("Impacts must be either +ve or -ve.")
                    exit(0)

        # Checking number of column,weights and impacts is same or not
            if col != len(weights)+1 or col != len(impact)+1:
                print(
                    "Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.")
                exit(0)

            if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
                print("ERROR : Output file extension is wrong")
                exit(0)
            if os.path.isfile(sys.argv[4]):
                os.remove(sys.argv[4])
                
            topsis(topsis_df,weights,impact)   
def topsis(topsis_df,weights,impact):
    import math
    newdata=topsis_df.iloc[:,1:]
    topsis_df=np.array(newdata).astype('float32')
    output=pd.DataFrame(topsis_df)
    a = (output.shape)
    rows = a[0]
    columns = a[1]
    for i in range(0,columns):
        Fsum=0
        for j in range(0,rows):
            Fsum += topsis_df[j][i]*topsis_df[j][i]
        Fsum = math.sqrt(Fsum)
        for j in range(0,rows):
            topsis_df[j][i] = topsis_df[j][i]/Fsum
    
    for x in range(0,columns):
        for y in range(0,rows):
            topsis_df[y][x] *= weights[x]

    vPlus = []
    vMinus = []
    
    def findMin(x,rows):
        m = 100
        for i in range(0,rows):
            if(topsis_df[i][x]<m):
                m=topsis_df[i][x]
        return m
    
    def findMax(x,rows):
        m = -1
        for i in range(0,rows):
            if(topsis_df[i][x]>m):
                m=topsis_df[i][x]
        return m
    
    for x in range(0,columns):
        if(impact[x]=='+'):
           vPlus.append(findMax(x,rows))
           vMinus.append(findMin(x,rows))
    
        else:
            vPlus.append(findMin(x,rows))
            vMinus.append(findMax(x,rows))        
            
    #calculatind the s+ and s- values 
    #computing the performance score for each row     
    def svalue(a,b):
        sub = a-b
        ans = sub**2
        return ans
    
    p = []
    #print(vPlus)
    #print(vMinus)
    for i in range(0,rows):
        sum1 = 0
        sum2 = 0
        for j in range(0,columns):
            sum1 = sum1+svalue(topsis_df[i][j],vPlus[j])
            sum2 = sum2+svalue(topsis_df[i][j],vMinus[j])
        sum1 = math.sqrt(sum1)
        sum2 = math.sqrt(sum2)
#        print(sum1)
#        print(sum2)
#        print("*****")
        p.append(sum2/(sum1+sum2))
        
    output['performance score'] = p
    rank = [0 for x in range(rows)]
    count=1
    q = p.copy()
    for i in range(0,rows):
        maxpos = q.index(max(q))
        rank[maxpos] = count
        count=count+1
        q[maxpos]=-1
    
    output['rank'] = rank
    print(output)
    output.to_csv(sys.argv[4])
    return output    

if __name__=="__main__":
    main()            
            
        

