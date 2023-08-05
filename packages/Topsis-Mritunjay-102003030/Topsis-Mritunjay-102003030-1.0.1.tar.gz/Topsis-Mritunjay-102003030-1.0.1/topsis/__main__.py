import numpy as np
import pandas as pd
import sys

class ExtraParameterError(Exception):
  pass
class NotsufficientColumns(Exception):
  pass
class NotNumeric(Exception):
  pass
class InsufficientData(Exception):
  pass
class impacterror(Exception):
  pass

def main():
  try:
    if(len(sys.argv)!=5):
      raise ExtraParameterError
    ifile=sys.argv[1]
    w=sys.argv[2]
    impact=sys.argv[3]
    rfile=sys.argv[4]

    data=pd.read_csv(ifile)
    if data.shape[1]<3:
      raise NotsufficientColumns

    w1 = list(w.split(","))
    m=[]
    for i in w1:
      m.append(float(i))
    h= list(impact.split(","))

    for i in range(len(h)):
      if not((h[i]=="+") or (h[i]=="-")):
        raise impacterror
    
    t=data.iloc[:,1:]
    final=t

    if (len(m) != len(t.axes[1])) or (len(h) != len(t.axes[1])):
      raise InsufficientData
    
    for i in range(len(t.axes[1])):
      if not(t.iloc[:,i].dtype.kind in 'iufc'):
        raise NotNumeric
        
    def norm(n):
      norm = n
      for j in range(len(n.axes[1])):
        sum = 0
        for i in range(len(n.axes[0])):
          sum = sum + n.iloc[i,j]**2
        norm.iloc[:,j] = n.iloc[:,j].values/np.sqrt(sum)
      return norm

    x = norm(t)
    # print(x)

    for j in range(len(x.axes[1])):
      x.iloc[:,j] = x.iloc[:,j]*m[j]
    # print(x)

    v_p=[]
    v_n=[]

    for j in range(len(x.axes[1])):
      if h[j]=='-':
        v_p.append(x.iloc[:,j].min())
        v_n.append(x.iloc[:,j].max())
      else:
        v_p.append(x.iloc[:,j].max())
        v_n.append(x.iloc[:,j].min())


    s_p=[]
    s_n=[]
    def euc(n):
      for j in range(len(n.axes[0])):
        sum1 = 0
        sum2 = 0
        for i in range(len(n.axes[1])):
          sum1 = sum1 + (n.iloc[j,i]-v_p[i])**2
          sum2 = sum2 + (n.iloc[j,i]-v_n[i])**2
        s_p.append(np.sqrt(sum1))
        s_n.append(np.sqrt(sum2))

    y = euc(x)

    p = []
    for i in range(len(s_n)):
      value = 0
      value = s_n[i]/(s_p[i]+s_n[i])
      p.append(value)
    # print(p)

    data['Topsis Score']=p
    data['Rank'] = (data['Topsis Score'].rank(method='max', ascending=False))
    data = data.astype({"Rank": int})
    print(data)

    data.to_csv(rfile)
    print("File Created")
  except FileNotFoundError:
    print("File Not Found")
  except ExtraParameterError:
    print("Wrong Parameters Entered")
  except NotsufficientColumns:
    print("Columns in the input file is less than 3")
  except NotNumeric:
    print("Columns are not numeric")
  except InsufficientData:
    print("Inuput of weight/impact is not sufficient")
  except ValueError:
    print("Weight is not separated by comma")
  except impacterror:
    print("Impact must be either +/- and must be separated by comma")

if __name__=="__main__":
  main() 