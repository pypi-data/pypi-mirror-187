def topsis():
  import numpy as np
  import pandas as pd
  import sys 

  #check for file not found
  try:
      with open(sys.argv[1],'r') as filse:
        df = pd.read_csv(filse)
  except FileNotFoundError as e:
      print(f"FileNotFoundError successfully handled\n"
          f"{e}")
      exit()


  tbl = df[df.columns[1:len(df.columns)]]
  sum = np.empty([5])
  temp = int(0)
  k = int(0)


  #check for len
  if(len(sys.argv) != 5):
    print("Error, Invalid number of arguments")
    exit()

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
  for i in impacts:
    if i != '+' and i != '-':
      print("Wrong input, enter + or -")
      exit()
  k = 0


  colno = len(tbl.columns)
  if(colno < 3):
    print("Columns number < 3")
    exit()

  if(colno != len(weightage)):
    print("Number not equal to weightage")
    exit()

  if(colno != len(impacts)):
    print("Number not equal to impacts")
    exit()
  #distance calcuation
  vplus = np.empty([len(tbl.columns)])
  vminus = np.empty([len(tbl.columns)])
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

  tbl["Score"] = sresult

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
  result = sys.argv[4]  
  tbl.to_csv(result,index=False)