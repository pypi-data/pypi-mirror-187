#Assignment-01 Python code for Topsis
import pandas as pd
import numpy as np
import sys

if len(sys.argv) != 5 :
    sys.exit('Wrong number of parameters')

#code for command line input
data = sys.argv[1]
w = sys.argv[2]
imp = sys.argv[3]
final_file = sys.argv[4]


#Reading .csv file
try:
    new =pd.read_csv(data)
except:
    sys.exit("The filename entered not found.")
#df.to_csv("102017167-data.csv",index=None,header=True)
#new =pd.DataFrame(pd.read_csv("102017167-data.csv"))
#print(newdf)

n_col = new.shape[1]
if(not(n_col >= 3)):
    sys.exit("Error:Number of columns in the dataset is less than 3.")
   
newdf = new.iloc[:,1:n_col]
copydf = newdf.copy()
n = copydf.shape[1]

#Error Handling for Weights and Impact values
w = w.split(',')
if (len(w) != n):
    sys.exit("Error: Number of weights are greater or less than number of columns")
imp = imp.split(',')
if(len(imp)!= n):
    sys.exit("Error:Number of impacts are greater or less than number of columns")

#print(newdf.isnull().sum())

#Normalization step
for i in range(n):
    for j in range(copydf.shape[0]):
        copydf.iloc[j,i] = np.square(copydf.iloc[j,i])
      

sq = []
for i in range(copydf.shape[1]):
    sq.append(np.sum(copydf.iloc[:,i]))
#print(sq)
sq=np.sqrt(sq)
#print(sq)

for i in range(newdf.shape[1]):
    for j in range(newdf.shape[0]):
        newdf.iloc[j,i] = newdf.iloc[j,i] / sq[i]
#print(newdf)
 
#Weights value 
w1= []
for i in range(len(w)):
    w1.append(float(w[i]))
#print(w1)


#Multiplying each columns with the weights
for i in range(newdf.shape[1]):
    for j in range(newdf.shape[0]):
        newdf.iloc[j,i] =(newdf.iloc[j,i] * w1[i])
#print(newdf)

#Impacts Values
imp1 = []
for i in range(n):
    if( imp[i] == '+' or imp[i] == '-'):
        imp1.append(imp[i])
    else:
        sys.exit("Wrong Impact Value entered. Enter only + or - values for impact.")
        
#print(imp1)

#v1 is the ideal best and v2 is the ideal worst.
v1= []
v2 = []
for i in range(n):
    if(imp1[i] == "+"):
        v1.append(max(newdf.iloc[:,i]))
        v2.append(min(newdf.iloc[:,i]))
    else:
        v1.append(min(newdf.iloc[:,i]))
        v2.append(max(newdf.iloc[:,i]))

#print(v1)
#print(v2)

#s1 is the Si+ and s2 is the Si-.
#Calculating the Si+ and Si- using Vi+ and Vi-.
s1 = []
s2 = []

m2 =[]
m3 = []
for i in range(newdf.shape[0]):
    m2.clear()
    m3.clear()
    for j in range(newdf.shape[1]):
        m2.append(np.square(newdf.iloc[i,j]-v1[j]))
        m3.append(np.square(newdf.iloc[i,j]-v2[j]))
    s1.append(np.sqrt(sum(m2)))
    s2.append(np.sqrt(sum(m3)))
#print(s1)
#print(s2)

#Calculating the Topsis Score.
score = []
for i in range(len(s1)):
    score.append(s2[i]/(s1[i]+s2[i]))

new["Topsis Score"] = score

#Calculating the Rank based on Topsis Score in Descending Order.The highest topsis score is given 1st Rank.
new["Rank"] = new["Topsis Score"].rank(ascending=False)
#print(new)

#Copying the reated dataframe with the results to outputfile
new.to_csv(final_file,index = False,header=True)
