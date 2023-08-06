
import sys
def topsis(inputname,w,im,outputname):
    import pandas as pd
    import sys
    import os
    def is_numeric1(t):
        try:
            t=float(t)
            if (isinstance(t, int)==True or isinstance(t, float)==True):
                return True
        except:
            print("Not a numeric value in columns 2nd and above!")
            sys.exit(0)
        return False
    
    #checking of the file exists
    if os.path.exists(inputname) == False:
        print("File does not exist!")
        sys.exit(0)

    #correct file type should be passed
    a=[inputname,outputname]
    for val1 in a:  
        nametemp=val1.split('.')
        if nametemp[1]!="csv":
            print("Enter correct file format, only .csv!")
            sys.exit(0)

    #reading the data frame
    df1=pd.read_csv(inputname) 
    df=pd.read_csv(inputname)  

    #every dataset should have more than 3 columns
    if df.shape[1]<=3:
        print(" No. of columns should be greater than 3!")
        sys.exit(0)
    
    #checking if all the columns from 2nd onwards have numeric values
    for i in range(1,df.shape[1]):
        for j in range(df.shape[0]):
            if(is_numeric1(df.iloc[j,i]))==False:
                print(df.iloc[j,i])
                print("All the values in 2nd column and further should be numeric!")
                sys.exit(0)

    impact1=im
    totalweight=0.00
    weight1=w
    impacts=impact1.split(',')
    weights=weight1.split(',')
    for i in range(len(weights)):
        totalweight=totalweight+float(weights[i])
    if df.shape[1]-1 != len(impacts) or df.shape[1]-1 != len(weights )or len(impacts)!= len(weights):
        print("Either the impacts or weights are not equal to number of columns(starting from 2nd) or the impacts or weights are not separated by commas!")
        sys.exit(0)

    #Impacts must be either +ve or -ve
    for i in impacts:
        if i not in ["+","-"]:
            print("Impacts should be either + or - !")
            sys.exit(0)
    
    #vector normalization
    xsquares=[0]*(df.shape[1])
    for i in range(1,df.shape[1]):
        for j in range(df.shape[0]):
            xsquares[i]=xsquares[i]+(df.iloc[j,i])*(df.iloc[j,i])
    for i in range(1,df.shape[1]):
        xsquares[i]=(xsquares[i])**0.5
    for i in range(1,df.shape[1]):
        for j in range(df.shape[0]):
            df.iloc[j,i]=(df.iloc[j,i])/xsquares[i]

    #weight assignment
    for i in range(1,df.shape[1]):
        for j in range(df.shape[0]):
            df.iloc[j,i]=(df.iloc[j,i])*(float(weights[i-1]))/totalweight
    
    #finding ideal best and ideal best
    #idb is ideal best and idw is ideal worst
    idb=[0]*(df.shape[1])
    idw=[0]*(df.shape[1])
    for i in range(1,df.shape[1]):
        if impacts[i-1]=="+":
                idb[i]=max(df.iloc[:,i])
                idw[i]=min(df.iloc[:,i])
        elif impacts[i-1]=="-":
                idb[i]=min(df.iloc[:,i])
                idw[i]=max(df.iloc[:,i])
    
    #calculating euclidean distance and performace matrix
    sip=[0]*(df.shape[0])
    sim=[0]*(df.shape[0])
    si=[0]*(df.shape[0])
    pi=[0]*(df.shape[0])
    for k in range(df.shape[0]):
        for l in range(1,df.shape[1]):
            sip[k]=sip[k]+(df.iloc[k,l]-idb[l])*(df.iloc[k,l]-idb[l])
            sim[k]=sim[k]+(df.iloc[k,l]-idw[l])*(df.iloc[k,l]-idw[l])
    for k in range(df.shape[0]):
        sip[k]=(sip[k])**0.5
        sim[k]=(sim[k])**0.5
        si[k]=sip[k]+sim[k]
        pi[k]=sim[k]/si[k]
    
    df=df1

    #adding the topsis score to dataframe
    df["Topsis Score"]=pi

    #ranking according to topsis score
    df["Rank"]=df["Topsis Score"].rank(ascending=False)

    #writing to an output file
    df.to_csv(outputname,index=False)

topsis(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
