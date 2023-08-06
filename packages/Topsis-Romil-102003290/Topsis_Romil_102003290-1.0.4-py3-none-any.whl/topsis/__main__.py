import numpy as np
import pandas as pd
import math
import sys
def main():
  a=sys.argv[1]
  w=sys.argv[2].split(",")
  try:
   w=[int(i) for i in w]
  except:
   print("Enter only integer values")
   exit(1) 
  i=sys.argv[3].split(",")
  save=sys.argv[4]


  # print(a)
  try:

    a=pd.read_csv(a)

  except:

      print("File not Found")
      exit(1)


  b=a.iloc[:,1:].values
  try:
    c=np.array(b,dtype='int64')
  except:
    print("File contains non integer values")

  weights=np.array(w)
  impact=np.array(i)
  m=b.shape[0]
  n=b.shape[1]
  div=[]
  print(weights)



  for j in range(1,n+1):
    col=a.iloc[:,j].values
    colsq=col**2
    #print(colsq)
    colsq1=sum(colsq)
    
    div.append(math.sqrt(colsq1))
    #print(div)

  for j in range(n):
          b[:,j]=b[:,j]/div[j]
          b[:,j]=b[:,j]*weights[j]
  #print(b)
  vbest=[]
  vworst=[]
  for j in range(n):
    if(impact[j]=="+"):
        vbest.append(max(b[:,j]))
        vworst.append(min(b[:,j]))
    elif (impact[j]=="-"):
        vbest.append(min(b[:,j]))
        vworst.append(max(b[:,j]))
    else:
        print("Not the required value")
        exit(1)
  si=[]
  sj=[]
  s=[]
  p=[]

  for j in range(m):
    c=(sum((b[j,:]-vbest)**2))
    si.append(math.sqrt(c))
  #print(si)
  for j in range(m):
    d=(sum((b[j,:]-vworst)**2))
    sj.append(math.sqrt(d))
  print(si)
  print(sj)

  for j in range(m):
    s.append(si[j]+sj[j])
  print(s)
  for j in range(m):
    p.append(sj[j]/s[j])
  print(p)
  r1 = np.array(p)
  sorted_indices = np.argsort(-r1)
  ranks = np.empty_like(sorted_indices)
  ranks[sorted_indices] = np.arange(len(a))+1
  print(ranks)
  a['perfomancescore']=p
  a['rank']=ranks
  print(a)
 
  a.to_csv(save)
if __name__=='__main__':
    main()
