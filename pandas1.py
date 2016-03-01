import numpy as np
from matplotlib import pyplot as plt
import pandas as po
#KungFuPanda

def prob1():
 s1 = po.Series([-3]*5,range(2,11,2))
 print s1
 s2 = po.Series({'Bill': 31, 'Sarah': 28, 'Jane': 34, 'Joe': 26})
 print s2

def prob2():
 N1 = 100
 for i in xrange(5):
  plt.subplot(5,1,i+1)
  s = np.zeros(N1)
  s[1:] = np.random.binomial(1,.5,size=(N1-1,))*2 - 1
  s = po.Series(s)
  s = s.cumsum()
  s.plot()
 plt.suptitle("Random un-biased walks of length 100")
 plt.tight_layout()
 plt.show()
 ns = [100,1000,10000]
 for i, n in enumerate(ns):
  plt.subplot(len(ns),1,i+1)
  s = np.zeros(n)
  s[1:] = np.random.binomial(1,.51,size=(n-1,))*2 - 1
  s = po.Series(s)
  s = s.cumsum()
  s.plot()
  plt.title("Random biased walk of length %d"%n)
 plt.tight_layout()
 plt.show()
   
def prob3():
 name = ['Bill', 'Alice', 'Joe', 'Jenny', 'Ted', 'Taylor', 'Tracy', 'Morgan','Liz']
 sex = ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'M', 'F']
 age = [20, 21, 18, 22, 19, 20, 20, 19, 20]
 rank = ['Sp', 'Se', 'Fr', 'Se', 'Sp', 'J', 'J', 'J', 'Se']
 ID = range(9)
 aid = ['y', 'n', 'n', 'y', 'n', 'n', 'n', 'y', 'n']
 GPA = [3.8, 3.5, 3.0, 3.9, 2.8, 2.9, 3.8, 3.4, 3.7]
 mathID = [0, 1, 5, 6, 3]
 mathGd = [4.0, 3.0, 3.5, 3.0, 4.0]
 major = ['y', 'n', 'y', 'n', 'n']
 studentInfo = po.DataFrame({'ID': ID, 'Name': name, 'Sex': sex, 'Age': age, 'Class':rank})
 otherInfo = po.DataFrame({'ID': ID, 'GPA': GPA, 'Financial_Aid': aid})
 mathInfo = po.DataFrame({'ID': mathID, 'Grade': mathGd, 'Math_Major': major})
 print studentInfo[(studentInfo['Age']>19 )&(studentInfo['Sex'] == 'M')][['ID','Name']]

def prob4():
 name = ['Bill', 'Alice', 'Joe', 'Jenny', 'Ted', 'Taylor', 'Tracy', 'Morgan','Liz']
 sex = ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'M', 'F']
 age = [20, 21, 18, 22, 19, 20, 20, 19, 20]
 rank = ['Sp', 'Se', 'Fr', 'Se', 'Sp', 'J', 'J', 'J', 'Se']
 ID = range(9)
 aid = ['y', 'n', 'n', 'y', 'n', 'n', 'n', 'y', 'n']
 GPA = [3.8, 3.5, 3.0, 3.9, 2.8, 2.9, 3.8, 3.4, 3.7]
 mathID = [0, 1, 5, 6, 3]
 mathGd = [4.0, 3.0, 3.5, 3.0, 4.0]
 major = ['y', 'n', 'y', 'n', 'n']
 studentInfo = po.DataFrame({'ID': ID, 'Name': name, 'Sex': sex, 'Age': age, 'Class':rank})
 otherInfo = po.DataFrame({'ID': ID, 'GPA': GPA, 'Financial_Aid': aid})
 mathInfo = po.DataFrame({'ID': mathID, 'Grade': mathGd, 'Math_Major': major})
 print po.merge(studentInfo[studentInfo["Sex"]=="M"],otherInfo,on="ID")[['ID','Age','GPA']]

def prob5():
 crime_data = po.read_csv('crime_data.txt',index_col="Year")
 crime_data["Rate"] = crime_data["Total"]/crime_data["Population"]
 crime_data["Rate"].plot()
 plt.show() 
 print "Top Years for Crime Rate"
 print crime_data.sort(columns="Rate",ascending=False)["Rate"][:5] 
 avg_crimes = crime_data["Total"].mean()
 avg_burgls = crime_data["Burglary"].mean()
 print "Average total crimes: %f. Average total burglaries %f." % (avg_crimes,avg_burgls)
 print "List of years when the total number of crimes was below average, but not burglary."
 print crime_data[(crime_data["Total"]<avg_crimes)&(crime_data["Burglary"]>avg_burgls)][["Total","Burglary"]]
 crime_rate.plot(x='Population',y='Murder')
 plt.show()
 crime_data[["Population","Violent","Robbery"]].to_csv("crime_subset.txt")
prob5() 


