"""
Author: Ananya Thomas
Description :
This program uses command line arguments to implement Topsis : a Multi-Criteria Decision Ananlysis (MCDA) method
"""

# Importing packages
import numpy as np
import pandas as pd
import sys

# class defination
class Topsis:

  #init method
  def __init__(self, df , w, i,o):

    try:
        f = open(df, 'r')    
    except IOError:
       print ("There was an error reading", df)
       sys.exit(0)
    self.input = pd.read_csv(df)

    r,c = self.input.shape
    if c-1 < 3:
      raise Exception("Number of columns less than 3")  

    cols = self.input.iloc[:,-(c-1):].select_dtypes("object").columns
    if (len(cols) > 0):
      raise Exception("Non numeric values\nUsage : From the second to the last column must contain numeric values only")

    w = w.split(",")
    wl = len(w)
    if wl != (c-1):
      raise Exception("Number of weights not equal to number of columns")
    self.weight = [int(x) for x in w]

    i = i.split(",")
    il = len(i)
    if il != (c-1):
      raise Exception("Number of impacts not equal to number of columns")
    self.impact = i
    self.impact = [x.strip(' ') for x in self.impact]

    self.output = o

  # Creates a temporary dataframe to perform calculations 
  def calc(self):
    c = len(self.input.axes[1])
    calc = self.input.iloc[:,-(c-1):]
    return calc

  # Calculating normalized decision matrix
  def normalize(self,calc):
    c = len(calc.axes[1])
    cols = calc.columns
    calc[cols] = calc[cols] /calc[cols].abs().max()
  
  # Calculating weighted normalized decision matrix
    for i in self.weight:
      calc[cols] = calc[cols] * i
    return calc

  # Finding ideal best & ideal worst values
  def ideal(self,calc):
    r,c = calc.shape
    ibest = list()
    iworst = list()

    for i in range(0,c):

      if self.impact[i]=='+':
        ibest.append(max(calc.iloc[:,i]))
        iworst.append(min(calc.iloc[:,i]))

      elif self.impact[i] == '-':
        iworst.append(max(calc.iloc[:,i]))
        ibest.append(min(calc.iloc[:,i]))

      else:
        raise Exception("Impact is invalid\nUsage : Impacts must be either +ve or -ve")

    return calc,ibest, iworst

  # Calculating Euclidean distance from ideal best value and ideal worst value & TOPSIS score
  def euclidean(self,calc,ibest,iworst): 
    r,c = calc.shape
    best = np.zeros((r,1))
    worst = np.zeros((r,1))
    p = np.zeros((r,1)) 

    for j in range(r):  
        for i in range(c):  
            best[j] += (calc.iloc[j,i] - ibest[i]) ** 2
            worst[j] += (calc.iloc[j,i] - iworst[i]) ** 2    
        best[j] = (best[j]) ** (0.5)
        worst[j] = (worst[j]) ** (0.5)      
        p[j] = worst[j] / (worst[j] + best[j])

    return p
  
  # Ranking data points on the basis of TOPSIS score
  def rank(self,p):
    self.input["Topsis Score"] = p
    self.input['Rank'] = self.input['Topsis Score'].rank(ascending=False).astype(int)

  def sol(self): 
    df = self.calc()
    df2 = self.normalize(df)
    df3,ibest,iworst = self.ideal(df2)
    p = self.euclidean(df3,ibest,iworst)
    self.rank(p)
    self.output = self.input.to_csv(self.output)

def main():

  if len(sys.argv) != 5:
    raise Exception("Wrong number of inputs : \nUsage : topsis <input filename> <weights> <impacts> <output filename>")
  t = Topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
  t.sol()
    
if __name__ == "__main__":
    main()