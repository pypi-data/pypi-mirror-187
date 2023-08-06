import pandas as pd
import numpy as np
import sys

def topsis():
 if len(sys.argv)!=5:
    print("Wrong command line input")
    exit()

 try:
     with open(sys.argv[1], 'r') as filee:
            df=pd.read_csv(filee)
            
 except FileNotFoundError:
        print("File not found")
        exit()

 punctuation_dictionary = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '+': True, '*': True,'-': True, '=': True}
 punctuation_dictionary2 = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '*': True, '=': True}

 def char_check(new_list, punct_dict):
        for item in new_list:
            for char in item:
                if char in punct_dict:
                    return False

 def string_check(comma_check_list, punct_dict):
        for string in comma_check_list:
            new_list = string.split(",")
            if char_check(new_list, punct_dict) == False:
                print("Invalid input or Values not comma separated")
                exit()

 string_check(sys.argv[2], punctuation_dictionary)
 string_check(sys.argv[3], punctuation_dictionary2)

 nCol=len(df.columns)
 weights1 = list(sys.argv[2].split(","))
 impacts = list(sys.argv[3].split(","))

 weights = [eval(i) for i in weights1]

 if nCol<3:
        print("No of columns are less than 3.")
        exit()

 if len(impacts) != (nCol-1):
        print("No of values in impacts should be same as the number of columns.")
        exit()

 if len(weights) != (nCol-1):
        print("No of values in weights should be same as the number of columns.")
        exit()



 for i in range(len(impacts)):
    if(impacts[i]!="+" and impacts[i]!="-"):
       print("Impacts should be either '+' or '-'.")
       exit()

 for index,row in df.iterrows():
        try:
            float(row['P1'])
            float(row['P2'])
            float(row['P3'])
            float(row['P4'])
            float(row['P5'])
        except:
            df.drop(index,inplace=True)
            df["P1"] = pd.to_numeric(df["P1"], downcast="float")
            df["P2"] = pd.to_numeric(df["P2"], downcast="float")
            df["P3"] = pd.to_numeric(df["P3"], downcast="float")
            df["P4"] = pd.to_numeric(df["P4"], downcast="float")
            df["P5"] = pd.to_numeric(df["P5"], downcast="float")
            df = df.copy(deep=True)

 for i in range(1,nCol):
  temp=0
  for j in range(len(df)):
    temp=temp+df.iloc[j,i]**2
  temp=temp**0.5
  for j in range(len(df)):
    df.iat[j, i] = (df.iloc[j, i] / temp)*weights[i-1]


 ideal_best=(df.max().values)[1:]
 ideal_worst=(df.min().values)[1:]

 for i in range(1,nCol):
  if(impacts[i-1]=='-'):
    ideal_best[i-1],ideal_worst[i-1]=ideal_worst[i-1],ideal_best[i-1]

 score=[]
 distance_positive=[]
 distance_negative=[]
 for i in range(len(df)):
  temp_p,temp_n=0,0
  for j in range(1,nCol):
    temp_p=temp_p + (ideal_best[j-1]-df.iloc[i,j])**2
    temp_n=temp_n + (ideal_worst[j-1]-df.iloc[i,j])**2
  
  temp_p=temp_p**0.5
  temp_n=temp_n**0.5
  score.append(temp_n/(temp_p + temp_n))
  distance_negative.append(temp_n)
  distance_positive.append(temp_p)


 df['distance negative']=distance_negative
 df['distance positive']=distance_positive
 df['Topsis Score']=score

 df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
 df = df.astype({"Rank": int})
 print(df)

 df.to_csv(sys.argv[4],index=False)