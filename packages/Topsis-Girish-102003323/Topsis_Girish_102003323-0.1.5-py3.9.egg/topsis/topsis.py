import sys
import pandas as pd
import numpy as np
from sklearn import preprocessing
import string
# -- NAME : GIRISH GUPTA
# -- VERSION : 0.1.5
# -- CREDITS : THAPAR INSTITUTE OF ENGINEERING AND TECHNOLOGY
def main():
    argument = sys.argv
    try:
        data = argument[1]
        weights = argument[2]
        impacts = argument[3]
        output = argument[4]
    except:
        sys.exit("\nERROR\nTHERE IS SOME PROBLEM WITH THE ARGUMENTS\nTHE COMMAND TO BE USED IS: SPECIFIED IN README.MD \n")
    try:
        dataset = pd.read_csv(data, header=0)
    except:
        sys.exit(
            "\nERROR\n FILE f{data} NOT FOUND\n THIS PACKAGE ACCEPTS \'CSV\' FILES ONLY !!\n")

    n = dataset.shape[0]
    c = dataset.shape[1]

    if (c <= 2):
        sys.exit("\n ERROR \n INPUT DATA SHOULD HAVE ATLEAST 3 COLUMNS!")
    try:
        weights = [int(i) for i in weights.split(',')]
    except:
        sys.exit("\nERROR\n WEIGHTS NOT ASSIGNED CORRECTLY \n")

    impacts = impacts.split(',')
    for i in impacts:
        if not (i == '+' or i == '-'):
            sys.exit("\nERROR\n IMPACTS NOT ASSIGNED CORRECTLY \n")
            
    if (len(weights) < c-1 or len(impacts) < c-1):
        sys.exit("\nERROR\n NUMBER OF WEIGHTS OR IMPACTS ARE SPARSE !!! \n")

    for z, i in enumerate(dataset.iloc[0, 1:]):

        if type(i) == str and i in string.ascii_letters:

            label_encoder = preprocessing.LabelEncoder()
            dataset.iloc[:, z + 1] = label_encoder.fit_transform(dataset.iloc[:, z+1])

    matrix = np.array(dataset.drop(['Fund Name'], axis=1))
    matrix_sq = np.square(matrix)
    sum_col = np.sum(matrix_sq, axis=0)
    sqrt_sum_col = np.sqrt(sum_col)
    sq_sum_matrix = np.array([sqrt_sum_col]*n)
    normalized_matrix = np.divide(matrix, sq_sum_matrix)


    weight_matrix = np.array([[int(i) for i in weights]]*n)
    weighed_input = np.multiply(normalized_matrix, weight_matrix)


    pos = []
    neg = []
    for i in range(c-1):
        if impacts[i] == '+':
            pos.append(max(weighed_input[:, i]))
            neg.append(min(weighed_input[:, i]))
        else:
            pos.append(min(weighed_input[:, i]))
            neg.append(max(weighed_input[:, i]))
    V_Postive_matrix = np.array([pos]*n)
    neg_matrix = np.array([neg]*n)

    diff_pos = np.subtract(weighed_input, V_Postive_matrix)
    diff_neg = np.subtract(weighed_input, neg_matrix)
    diff_neg_sq = np.square(diff_neg)
    diff_pos_sq = np.square(diff_pos)


    s_pos = np.sqrt(np.sum(diff_pos_sq, axis=1))
    s_neg = np.sqrt(np.sum(diff_neg_sq, axis=1))

    P = s_neg/(s_pos+s_neg)

    P_dataset = pd.DataFrame(P.transpose())
    dataset["Topsis Score"] = P
    dataset["Rank"] = P_dataset.rank(ascending=False)
    print("\n\nResult Found:\n")
    print(dataset)

    print(f"\n \nResult Stored at {output}")
    dataset.to_csv(output, index=False)
if __name__== "__main__":
    main()