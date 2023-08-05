import numpy as np
import pandas as pd
import copy
import sys 
from pathlib import Path

# Function for normalization
def normalize(matrix):
  rows,cols = np.shape(matrix)
  square_sum = []
  for j in range(cols):
    sum = 0
    for i in range(rows):
      sum += matrix[i][j]**2
    square_sum.append(sum**0.5)

  for j in range(cols):
    for i in range(rows):
      matrix[i][j] /= square_sum[j]  
  return matrix

# Function for weighted values
def apply_weights(matrix, weights):
  rows, cols = np.shape(matrix)
  for j in range(cols):
    for i in range(rows):
      matrix[i][j] *= weights[j]
  return(matrix)

# Function to find topsis score
def find_topsis_score(matrix,impacts):
  rows,cols = np.shape(matrix)
  ideal_best = []
  ideal_worst = []
  for j in range(cols):
    if(impacts[j]==1):
      ideal_best.append(np.max(matrix[:,j]))
      ideal_worst.append(np.min(matrix[:,j]))
    else:
      ideal_best.append(np.min(matrix[:,j]))
      ideal_worst.append(np.max(matrix[:,j]))
  ideal_best = np.array(ideal_best)
  ideal_worst = np.array(ideal_worst)
  positive_score = []
  negative_score = []
  for i in range(rows):
    s_plus = np.linalg.norm(matrix[i,:] - ideal_best)
    s_minus = np.linalg.norm(matrix[i,:] - ideal_worst)
    positive_score.append(s_plus)
    negative_score.append(s_minus)

  topsis_score_vector = []
  for i in range(rows):
    topsis_score_vector.append(negative_score[i]/(negative_score[i] + positive_score[i]))
  
  return topsis_score_vector

# Function to get rank array
def find_rank(topsis_score):
  ranks = []
  copy_list = copy.deepcopy(topsis_score)
  copy_list.sort(reverse=True)
  for i in range(len(topsis_score)):
    ele = topsis_score[i]
    ranks.append(copy_list.index(ele)+1)
  return ranks


def main():

  num_args = len(sys.argv)
  ## checking for correct number of arguments
  if(num_args != 5):
    raise Exception('Invalid Number of Arguments')

  file = sys.argv[1] # file path as a string
  file_path=Path(sys.argv[1])
  weights_string = sys.argv[2] 
  impacts_string = sys.argv[3]
  result_file = sys.argv[4]
  impacts = []
  weights = []

  for i in range(1,len(weights_string)-1,2):
    if not(weights_string[i]==','):
      raise Exception('Invalid Weights Input')

  for i in range(1,len(impacts_string)-1,2):
    if not(impacts_string[i]==','):
      raise Exception('Invalid Impacts Input')


  for i in range(len(impacts_string)):
    if(impacts_string[i]=='+'):
      impacts.append(1)
    elif(impacts_string[i]=='-'):
      impacts.append(-1)
    elif(impacts_string[i]==','):
      continue
    else:
      raise Exception('Invalid Impacts String')

  weights_string = (sys.argv[2].split(','))

  for i in range(len(weights_string)):
    weights.append(float(weights_string[i]))

  for i in range(len(weights)):
    if(weights[i]<0):
      raise Exception('Invalid Weight Value')

  if not(file_path.exists()):
    raise Exception('File Not Found')

  if not(len(weights)==len(impacts)):
    raise Exception('Inconsistent number of Inputs')

  df = pd.read_csv(file)
  #number of rows, columns
  num_rows = len(df.axes[0])
  num_cols = len(df.axes[1])
  #column names
  column_names = list(df.columns)
  #ids
  column_ids = df.iloc[:,0]

  #exception handling for dataframe
  if(num_cols<3):
    raise Exception('Columns in csv file less than 3')

  accepted_types = ['float64','float32', 'int64', 'int32']

  for i in range(1,num_cols):
    if not(df.iloc[:,i].dtype in accepted_types):
      raise Exception('Invalid Column dtype')

  if not(num_cols-1==len(weights)):
    raise Exception('Number of columns in input file inconsistent with Weights Input')

  if not(num_cols-1==len(impacts)):
    raise Exception('Number of Columns in input file inconsistent with Impacts Input')


  feature_df = df.iloc[:,1:num_cols]
  matrix = np.array(feature_df)
  #feature_df
  original_matrix = copy.deepcopy(matrix)
  normalize(matrix)
  apply_weights(matrix, weights)
  topsis_score = find_topsis_score(matrix, impacts)
  ranks = find_rank(topsis_score)

  topsis_score = np.array(topsis_score)
  ranks = np.array(ranks)

  topsis_score = topsis_score.reshape(-1,1)
  ranks = ranks.reshape(-1,1)

  column_ids = np.array(column_ids)
  column_ids = column_ids.reshape(-1,1)


  temp = np.append(original_matrix, topsis_score, axis = 1)
  temp2 = np.append(temp, ranks, axis = 1)
  result_matrix = np.append(column_ids, temp2, axis = 1)

  column_names.append('Topsis Score')
  column_names.append('Rank')
  result_df = pd.DataFrame(result_matrix, columns = column_names)
  print("Results:")
  print(result_df)

  result_df.to_csv(result_file, index=False)


# driver code    
if __name__ == "__main__":
    main()
    