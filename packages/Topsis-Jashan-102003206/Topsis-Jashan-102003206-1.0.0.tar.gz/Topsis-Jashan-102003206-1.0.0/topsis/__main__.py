import sys
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype


class ArgumentsError(Exception):
    pass


class ColumnsError(Exception):
    pass


class TypeError(Exception):
    pass


class EqualityError(Exception):
    pass


class ImpactsError(Exception):
    pass


class SeparationError(Exception):
    pass


class CommaError(Exception):
    pass


def main():
    try:
        if (len(sys.argv) != 5):
            raise ArgumentsError

        df = pd.read_csv(sys.argv[1])
        df_temp = pd.read_csv(sys.argv[1])

        if (df.shape[1] < 3):
            raise ColumnsError

        for i in range(1, df.shape[1]):
            if (not is_numeric_dtype(df.iloc[:, i])):
                raise TypeError

        if (',' not in sys.argv[2]) or (',' not in sys.argv[3]):
            raise CommaError

        weights = sys.argv[2].split(sep=',')
        impacts = sys.argv[3].split(sep=',')

        # print(weights)
        # print(impacts)

        for i in impacts:
            if (i != '+' and i != '-'):
                raise ImpactsError

        if len(weights) != len(impacts) or len(impacts) != (df.shape[1]-1):
            raise EqualityError

        best = []
        worst = []

        for i in range(1, df.shape[1]):
            rmse = np.sqrt(np.sum(np.square(df.iloc[:, i].values)))
            df.iloc[:, i] = df.iloc[:, i]/rmse
            df.iloc[:, i] = df.iloc[:, i]*float(weights[i-1])
            if impacts[i-1] == '+':
                best.append(max(df.iloc[:, i]))
                worst.append(min(df.iloc[:, i]))
            if impacts[i-1] == '-':
                best.append(min(df.iloc[:, i]))
                worst.append(max(df.iloc[:, i]))

        best = np.array(best)
        worst = np.array(worst)

        Topsis_Score = []

        for i in range(df.shape[0]):
            S_best = np.sqrt(np.sum(np.square(df.iloc[i, 1:].values-best)))
            S_worst = np.sqrt(np.sum(np.square(df.iloc[i, 1:].values-worst)))
            Topsis_Score.append(S_worst/(S_worst+S_best))

        Rank = [(sorted(Topsis_Score, reverse=True).index(i)+1)
                for i in Topsis_Score]

        df = df_temp

        df['Topsis Score'] = Topsis_Score
        df['Rank'] = Rank

        df.to_csv(sys.argv[4], index=False)

        # print("Output File:", sys.argv[4], "generated")

    except ArgumentsError:
        print("Number of Arguments passed must be equal to 4")
        print("\nThe correct syntax is: \ntopsis <input_file> <weights> <impacts> <output_file>\n")

    except FileNotFoundError:
        print("No such file or directory: ", sys.argv[1])

    except ColumnsError:
        print("Input file must contain three or more columns")

    except TypeError:
        print("All columns except first must contain numeric values only")

    except EqualityError:
        print("Number of weights, number of Impacts and number of Columns (from 2nd to last columns) must be same")

    except ImpactsError:
        print("Impacts must be either +ve or -ve and must be separated by ',' (comma)")

    except ValueError:
        print(
            "Weights must contain numeric values only and must be separated by ',' (comma)")

    except CommaError:
        print("Impacts and weights must be separated by ',' (comma)")


if __name__ == '__main__':
    main()
