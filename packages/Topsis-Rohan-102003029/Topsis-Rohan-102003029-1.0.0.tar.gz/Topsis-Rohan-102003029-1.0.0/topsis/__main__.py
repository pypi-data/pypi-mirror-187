import sys
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype

class InsufficientArguments(Exception):
    pass
class NonNumericDataset(Exception):
    pass
class InsufficientColumns(Exception):
    pass
class NonNumeric(Exception):
    pass
class InsufficientWeights(Exception):
    pass
class InvalidImpacts(Exception):
    pass
class InsufficientImpacts(Exception):
    pass

def main():
    try:
        if len(sys.argv) != 5:
            raise InsufficientArguments

        input_file = sys.argv[1]
        weights = sys.argv[2]
        impacts = sys.argv[3]
        result_file = sys.argv[4]

        dataset = pd.read_csv(input_file)
        for i in range(1, dataset.shape[1]):
            if(not is_numeric_dtype(dataset.iloc[:, i])):
                raise NonNumericDataset

        row_length = dataset.shape[0]
        col_length = dataset.shape[1]
        if col_length <= 3:
            raise InsufficientColumns
        
        wts = weights.split(',')
        if wts[0] == '' or wts[-1] == '':
            raise NonNumeric
        for value in wts:
            value = float(value)
        
        w = np.fromstring(weights, dtype=float, sep=",")
        if len(w) != col_length - 1:
            raise InsufficientWeights

        imp = np.array(impacts.split(','))
        if len(imp) != col_length - 1:
            raise InsufficientImpacts
        index = 0
        for c in impacts:
            if (index % 2 == 0 and c not in '+-') or (index % 2 != 0 and c not in ',') or (impacts[-1] in ','):
                raise InvalidImpacts
            index += 1

        data = dataset.iloc[:, 1:]
        column_names = list(dataset.columns)
        column_names.extend(['Topsis Score', 'Rank'])
        row_names = dataset.iloc[:, 0].values

        arr = np.array(data)

        squared_arr = arr**2
        col_sums = np.sqrt(np.sum(squared_arr, axis=0))
        arr = arr / col_sums

        w = np.fromstring(weights, dtype=float, sep=",")
        arr = arr * w

        imp = np.array(impacts.split(','))
        ideal_best = []
        ideal_worst = []
        for col in range(arr.shape[1]):
            if imp[col] == '+':
                ideal_best.append(np.amax(arr[:, col]))
                ideal_worst.append(np.amin(arr[:, col]))
            else:
                ideal_best.append(np.amin(arr[:, col]))
                ideal_worst.append(np.amax(arr[:, col]))

        difference = arr - ideal_best
        squared_difference = difference**2
        sum_of_squared_difference = np.sum(squared_difference, axis=1)
        best_euclidean_distance = np.sqrt(sum_of_squared_difference)
        best_euclidean_distance = best_euclidean_distance.reshape(-1, 1)
        best_euclidean_distance

        difference = arr - ideal_worst
        squared_difference = difference**2
        sum_of_squared_difference = np.sum(squared_difference, axis=1)
        worst_euclidean_distance = np.sqrt(sum_of_squared_difference)
        worst_euclidean_distance = worst_euclidean_distance.reshape(-1, 1)
        worst_euclidean_distance

        p = worst_euclidean_distance / (best_euclidean_distance + worst_euclidean_distance)
        result = np.concatenate((data, p), axis=1)

        score = result[:, -1]
        sort_indices = np.argsort(score)
        ranks = np.empty(len(score))
        ranks[sort_indices] = np.arange(1, len(sort_indices) + 1)
        ranks = len(ranks) - ranks + 1
        result = np.concatenate((result, ranks.reshape(-1, 1)), axis=1)

        result = np.concatenate((row_names.reshape(-1, 1), result), axis=1)
        final_dataframe = pd.DataFrame(result, columns=column_names)
        final_dataframe['Rank'] = final_dataframe['Rank'].astype(int)

        final_dataframe.to_csv(sys.argv[4], index=False)

    except InsufficientArguments:
        print("4 parameters: inputFileName, Weights, Impacts, resultFileName must be provided")  

    except NonNumericDataset:
        print("the dataset should contain numeric values from 2nd to the last column")

    except InsufficientColumns:
        print("Provide a dataset with more than 3 columns")

    except NonNumeric:
        print("Provide comma separated numeric values")

    except InsufficientWeights:
        print("{} weights must be provided".format(col_length - 1))

    except InsufficientImpacts:
        print("{} impacts must be provided".format(col_length - 1))

    except InvalidImpacts:
        print("Invalid format for impacts. Provide comma-separated '+' or '-' values")
        
    except FileNotFoundError:
        print("The data file: {} has not been found in the current directory".format(input_file))

    except ValueError:
        print("Weights should be numeric")


if __name__ == '__main__':
    main()    