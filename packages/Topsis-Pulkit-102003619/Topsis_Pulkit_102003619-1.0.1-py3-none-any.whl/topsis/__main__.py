import numpy as np
import pandas as pd
import copy
import sys 
from pathlib import Path

# Function for Calculating the Topsis score
def Calculate_topsis_score(matrix,impacts):

  r,c = np.shape(matrix)
  array_ideal_best = []
  array_ideal_worst = []
  for j in range(c):
    if(impacts[j]==1):
      array_ideal_best.append(np.max(matrix[:,j]))
      array_ideal_worst.append(np.min(matrix[:,j]))
    else:
      array_ideal_best.append(np.min(matrix[:,j]))
      array_ideal_worst.append(np.max(matrix[:,j]))


  array_ideal_best = np.array(array_ideal_best)
  array_ideal_worst = np.array(array_ideal_worst)

  total_positive_score = []
  total_negative_score = []

  for i in range(r):
    calc_s_plus = np.linalg.norm(matrix[i,:] - array_ideal_best)
    calc_s_minus = np.linalg.norm(matrix[i,:] - array_ideal_worst)
    total_positive_score.append(calc_s_plus)
    total_negative_score.append(calc_s_minus)

  topsis_score_vector = []
  for i in range(r):
    topsis_score_vector.append(total_negative_score[i]/(total_negative_score[i] + total_positive_score[i]))
  
  return topsis_score_vector


# Function for normalization
def Perform_normalization(matrix):
  r,c = np.shape(matrix)
  squared_sum = []
  for j in range(c):
    sum = 0
    for i in range(r):
      sum += matrix[i][j]**2
    squared_sum.append(sum**0.5)

  for j in range(c):
    for i in range(r):
      matrix[i][j] /= squared_sum[j]  
  return matrix

# Function to Calculate Weighted Values
def apply_weights(matrix, weights):
  r, c = np.shape(matrix)
  for j in range(c):
    for i in range(r):
      matrix[i][j] *= weights[j]
  return(matrix)


# Function to Calculate rank array
def find_rank(topsis_score):
  ranks = []
  copy_list = copy.deepcopy(topsis_score)
  copy_list.sort(reverse=True)
  for i in range(len(topsis_score)):
    ele = topsis_score[i]
    ranks.append(copy_list.index(ele)+1)
  return ranks


def main():

  number_args = len(sys.argv)
  ## checking if number of arguments are correct or not
  if(number_args != 5):
    raise Exception('Error in the number of Arguments')

  file = sys.argv[1] # file path
  file_path=Path(sys.argv[1])
  weights_string = sys.argv[2] 
  impacts_string = sys.argv[3]
  result_file = sys.argv[4]
  impacts = []
  weights = []

  array_impacts = (impacts_string.split(','))
  array_weights = (sys.argv[2].split(','))

  if(len(array_weights)!=len(array_impacts)):
    raise Exception('Error in the number of arguments')

  for i in range(len(array_impacts)):
    if(array_impacts[i]=='+'):
      impacts.append(1)
    elif(array_impacts[i]=='-'):
      impacts.append(-1)
    elif(array_impacts[i]==','):
      continue
    else:
      raise Exception('Error in the string of Impacts')

  try:
    for i in range(len(array_weights)):
      weights.append(float(array_weights[i]))
  except:
    print('Error in the string of Weights')
    exit(1)

  for i in range(len(weights)):
    if(weights[i]<0):
      raise Exception('Error : Negative value of Weight not acceptible')

  if not(file_path.exists()):
    raise Exception('File Not Found')

  if not(len(weights)==len(impacts)):
    raise Exception('Error in the number of Inputs')

  df = pd.read_csv(file)
  #number of rows, columns
  num_rows = len(df.axes[0])
  number_cols = len(df.axes[1])
  #column names
  col_names = list(df.columns)
  #ids
  column_ids = df.iloc[:,0]

  #exception handling for dataframe
  if(number_cols<3):
    raise Exception('Columns in csv file less than 3')

  accepted_types = ['float64','float32', 'int64', 'int32']

  for i in range(1,number_cols):
    if not(df.iloc[:,i].dtype in accepted_types):
      raise Exception('Invalid Column dtype')

  if not(number_cols-1==len(weights)):
    raise Exception('Error with Number of columns in input file to Weights Input')

  if not(number_cols-1==len(impacts)):
    raise Exception('Error with Number of Columns in input file to Impacts Input')


  feature_df = df.iloc[:,1:number_cols]
  matrix = np.array(feature_df)
  #feature_df
  original_matrix = copy.deepcopy(matrix)
  Perform_normalization(matrix)
  apply_weights(matrix, weights)
  topsis_score = Calculate_topsis_score(matrix, impacts)
  ranks = find_rank(topsis_score)

  topsis_score = np.array(topsis_score)
  ranks = np.array(ranks)

  topsis_score = topsis_score.reshape(-1,1)
  ranks = ranks.reshape(-1,1)

  column_ids = np.array(column_ids)
  column_ids = column_ids.reshape(-1,1)


  temp = np.append(original_matrix, topsis_score, axis = 1)
  temp2 = np.append(temp, ranks, axis = 1)
  resultant_matrix = np.append(column_ids, temp2, axis = 1)

  col_names.append('Topsis Score')
  col_names.append('Rank')
  result_df = pd.DataFrame(resultant_matrix, columns = col_names)
  print("Results:")
  print(result_df)

  result_df.to_csv(result_file, index=False)


# driver code    
if __name__ == "__main__":
    main()
    