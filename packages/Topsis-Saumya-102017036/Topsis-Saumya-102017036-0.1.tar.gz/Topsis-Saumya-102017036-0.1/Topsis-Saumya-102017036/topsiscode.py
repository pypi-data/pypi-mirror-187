
import sys
import numpy as np
import pandas as pd

def normalised_matrix(df):
    nom = np.sqrt(np.sum(np.square(df), axis = 0))
    return np.divide(df, nom)
def multiply_weights_matrix(df, w):
    return np.multiply(df, w)


def per_score_and_rank(df, i):

    ideal_positive = df.max()
    ideal_positive .iloc[np.where(i == '-')] = df.min().iloc[np.where(i == '-')]

    ideal_negative  = df.min()
    ideal_negative.iloc[np.where(i == '-')] = df.max().iloc[np.where(i == '-')]
    S_pos = np.sqrt(np.sum(np.square(df - ideal_positive), axis = 1))
    S_neg = np.sqrt(np.sum(np.square(df - ideal_negative), axis = 1))


    performance_score = S_neg/(S_neg + S_pos)
    ranks = performance_score.rank(ascending = False)

    return performance_score, ranks


def main():
    try:
        if len(sys.argv) != 5:
            raise(IndexError)

        df = pd.read_csv(sys.argv[1], index_col=0)
        w = sys.argv[2]
        i = sys.argv[3]
        output_path = sys.argv[4]

    except FileNotFoundError as e:
        raise SystemExit(e)

    except IndexError:
        raise SystemExit(f"Usage: topsis <input_file_name> <weights> <impacts> <output_file_name>")

    else:
        w = w.replace(" ", "").split(",")
        try:
            w = np.array(w, dtype = float)
        except Exception:
            raise SystemExit("Weights must be numeric and seperated by ','. For example, \"0.25,0.25,1,0.25\"")

        i = np.array(i.replace(" ", "").split(","))


    try:
        if ((i == '+')|(i == '-')).all() != True:
            raise Exception("Impacts must be either '+' or '-' and seperated by ','. For example, \"+,-,+,-\"")

        if len(df.columns) < 2:
            raise Exception("Input file must contain 3 or more columns")

        if (len(df.columns) != len(w)) or (len(w) != len(i)):
            raise Exception("Length of weights and impacts should be equal to number of features")
        
        # if (df.dtypes == 'object'):
        if df.applymap(np.isreal).all().all() != True:
            raise Exception("Columns (excluding first one) in input file must contain numeric values only")

    except Exception as e:
        raise SystemExit(e)


    normalised_df = normalised_matrix(df)
    weighted_n_df = multiply_weights_matrix(normalised_df, w)

    df['TOPSIS Score'], df['Rank'] = per_score_and_rank(weighted_n_df, i)

    df.to_csv(output_path)

if __name__ == "__main__":
    main()