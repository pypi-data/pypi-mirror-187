def main():
  import numpy as np
  import pandas as pd
  import sys 

  df = pd.read_csv(sys.argv[1])
  df
  tbl = df[df.columns[1:6]]
  tbl
  sum = np.empty([5])
  temp = int(0)
  k = int(0)


  #square rate sum
  for i in tbl:
    temp = 0
    for j in range(8):
      temp = temp + (tbl.loc[j].at[i])*(tbl.loc[j].at[i])
    sum[k] = np.sqrt(temp)
    k = k+1  
  print(sum)
  k = 0


  #normalising data
  for i in tbl:
    for j in range(8):
      tbl.loc[j].at[i] = tbl.loc[j].at[i]/sum[k]
    k = k+1  
  # print(tbl)    


  #weightage
  string = sys.argv[2]
  weight = string.split(',')
  weight = [eval(i) for i in weight]
  weightage = (np.array(weight))

  k = 0
  for i in tbl:
    for j in range(8):
      tbl.loc[j].at[i] = tbl.loc[j].at[i]*weightage[k]
    k = k+1  
  print(tbl)


  #impacts
  string = sys.argv[3]
  impact = string.split(',')
  impacts = (np.array(impact))
  k = 0


  #distance calcuation
  vplus = np.empty([5])
  vminus = np.empty([5])
  for i in tbl:
    if(impacts[k] == '+'):
      vplus[k] =  max(tbl[i])
      vminus[k] = min(tbl[i])  
    if(impacts[k] == '-'):
      vplus[k] =  min(tbl[i])
      vminus[k] = max(tbl[i])
    k = k+1     

  k = 0


  #final calculation and ranking
  splus = np.empty([8])
  sminus = np.empty([8]) 
  sresult = np.empty([8])
  for j in range(8):
    for i in tbl:
      splus[j] = splus[j] + (tbl.loc[j].at[i] - vplus[k])*(tbl.loc[j].at[i] - vplus[k]) 
      sminus[j] = sminus[j] + (tbl.loc[j].at[i] - vminus[k])*(tbl.loc[j].at[i] - vminus[k]) 
      k = k+1
    splus[j] = np.sqrt(splus[j])
    sminus[j] = np.sqrt(sminus[j])
    sresult[j] = splus[j]+sminus[j]
    k = 0     

  tbl["Score"] = sresult;

  sno = np.array([1,2,3,4,5,6,7,8])

  for i in range(7):  
    for j in range(7):  
      if(sresult[j]>sresult[j+1]):  
        temp = sresult[j]  
        sresult[j] = sresult[j+1]  
        sresult[j+1] = temp  
        temp2 = sno[j]
        sno[j] = sno[j+1]
        sno[j+1] = temp2

  tbl["Rank"] = sno
  print(tbl)

if __name__ == '__main__': 
  main() 