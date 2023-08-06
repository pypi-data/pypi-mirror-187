import sys

# command line arguments

def parser(args):
    dataFile = args[1]   # dataset csv file
    weights = args[2]    # weights
    impacts = args[3]    # impacts
    resFile = args[4]    # result file
    return (dataFile, weights, impacts, resFile)
    
def process(dataFile, weights, impacts, resFile) :
  import pandas as pd
  import numpy as np
  import sys

  w = list(int(i) for i in weights.split(','))
  im = list(i for i in impacts.split(','))

# message for wrong inputs.

  if(len(w) != len(im)) :
    print('Number of elements in Weights and Impacts should be same')  
    sys.exit(0)

  try:
    data = pd.read_csv(dataFile)

# Handling of “File not Found” exception
  except FileNotFoundError:
    print('File not Found')

  else :
    df = data.iloc[:, 1 :].values
    m = len(data)
    n = len(data.columns) - 1

# Input file must contain three or more columns.
    if(n < 3):
      print('Less than 3 Columns')
      sys.exit(0)
    rss = []

    for j in range(0, n):
      s = 0
      for i in range(0, m):
        s += np.square(df[i, j])
      rss.append(np.sqrt(s))

    for j in range(0, n):
      df[:, j] /= rss[j]
      df[:, j] *= w[j]

# Finding ideal best and worst value
    best = []
    worst = []

    for j in range(0, n):
      if(im[j] == '+'): 
        best.append(max(df[:, j]))
        worst.append(min(df[:, j]))

      elif(im[j] == '-'):
        best.append(min(df[:, j]))
        worst.append(max(df[:, j]))

      else:
        print('Signs in Impact can be either + or - only')
        sys.exit(0)

# Calculating Euclidean Distance
    ebest = []
    eworst = []

    for i in range(0, m):
      ssdb = 0
      ssdw = 0

      for j in range(0, n):
        ssdb += np.square(df[i, j] - best[j])
        ssdw += np.square(df[i, j] - worst[j])

      rssdb = np.sqrt(ssdb)
      rssdw = np.sqrt(ssdw)
      ebest.append(rssdb)
      eworst.append(rssdw)

# Calculate Performance Score
    p = []

    for i in range(0, m):
      measure = eworst[i] / (eworst[i] + ebest[i])
      p.append(measure * 100)

    data['Topsis Score'] = p
    data['Rank'] = data['Topsis Score'].rank(ascending = False)
    print(data)
    data.to_csv(resFile)

# Caculating Topsis
def topsis():
  dataFile, weights, impacts, resFile = parser(sys.argv)
  process(dataFile, weights, impacts, resFile)
  
if __name__ == "__main__":
    dataFile, weights, impacts, resFile = parser(sys.argv)
    topsis(dataFile, weights, impacts, resFile)