#Code for topsis
import pandas as pd  
import numpy as np
import sys

##Taking the input as arguments
inputDataFile=sys.argv[1]
weightsAr=sys.argv[2]
impactsAr=sys.argv[3]
opfile=sys.argv[4]
#importing the data
##Handling file not found exception
try:
    data=pd.read_csv(inputDataFile)
except:
    sys.exit('No Such file found!')
datacp=data.copy()
print(data)
########################################################
#Taking inputs

weights=weightsAr.split(',')
impacts=impactsAr.split(',')

##Handling exception for wrong number of arguments
if len(weights)!=data.shape[1]-1:
    sys.exit('Incompatible number of arguments for weights')
if len(impacts)!=data.shape[1]-1:
    sys.exit('Incompatible number of argumnets for impacts')



print(weights)
##converting weights into int
for x in range(len(weights)):
    weights[x]=float(weights[x])

#######################################################
res=data.copy()
res=res.drop(res.columns[0],axis=1)
data=data.drop(data.columns[0],axis=1)


res #copy of the original dataset for calculation of sqrt
#######################################################
#Calculating squares and summing them
sqSum=[]#Sqareroot of sum of squares of each column values
sq=0

##Sqauring the elements of the data
for x in range(res.shape[1]):
    res.iloc[:,x]=np.square(res.iloc[:,x])





##Summing the squares of each element    
for y in range(res.shape[1]):
    sqSum.append(np.sum(res.iloc[:,y]))

#Calculating the squareroot of the summed elements    
sqSum=np.sqrt(sqSum)


    
#res
sqSum
for j in range(res.shape[1]):
    data.iloc[:,j]=data.iloc[:,j]/sqSum[j]
# data

##################################CHECKED#############################






##Multiplying with the weights
for m in range(res.shape[1]):
    data.iloc[:,m]=data.iloc[:,m]*weights[m]



############CHECKED#############################
########################################################################

##Calculating the ideal best and ideal worst
idealBest=[]
idealWorst=[]

for x in range(data.shape[1]):
    if impacts[x]=='+':
        idealBest.append(max(data.iloc[:,x]))
        idealWorst.append(min(data.iloc[:,x]))
    elif impacts[x]=='-':
        idealBest.append(min(data.iloc[:,x]))
        idealWorst.append(max(data.iloc[:,x]))
    else:
        print('Invalid Symbol')
        exit()



#############CHECKED##########################

       
###################################################
#To calculate S+ & S-

spl=[]
smm=[]
temp=0
temn=0
for c in range(data.shape[0]): 
    for d in range(data.shape[1]):
        temp+=(data.iloc[c,d]-idealBest[d])**2
        temn+=(data.iloc[c,d]-idealWorst[d])**2
    spl.append(np.sqrt(temp))
    smm.append(np.sqrt(temn))
    temp=0
    temn=0



##Calculating Performance score
perfomScore=[]

for l in range(len(smm)):
    perfomScore.append(smm[l]/(spl[l]+smm[l]))
# print()

# print(perfomScore)
finalres=[]
for g in range(len(perfomScore)):
    finalres.append([perfomScore[g],perfomScore.index(perfomScore[g])])

finalres.sort()
finalres.reverse()


##Appending finalres, i.e list of perfomance score, original index & rank

for x in  range(len(finalres)):
    finalres[x].append(x)

for m in range(data.shape[0]):
    datacp.loc[finalres[m][1],'Topsis Score']=finalres[m][0]
    
for n in range(data.shape[0]):
    datacp.loc[finalres[n][1],'Rank']=int(finalres[n][2]+1)


# print(datacp)
# print()
# print()
# print()
# print()
datacp.to_csv(opfile)
