import numpy as np
import pandas as pd
import sys


class CLIError(Exception):
    pass

class UnsupportedFileError(Exception):
    pass

class ColsNotEqualError(Exception):
    pass

class NotEnoughDataError(Exception):
    pass

class ImpactValueError(Exception):
    pass



try:
    if len(sys.argv) < 5:
        raise CLIError

    file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_path = sys.argv[4]
   

    format = str(file).split(sep='.')[-1]

    if format == 'xlsx':
        df = pd.read_excel(file, index_col=None)
        # print(df)
        df.to_csv('102197016-data.csv', encoding='utf-8', index=False)
        # df = pd.read_csv('data.csv')
    elif format == 'csv':
        df = pd.read_csv(file)
    else:
        raise UnsupportedFileError

    # print(df.head())

    if df.shape[0] < 3 or df.shape[1] < 3:
        raise NotEnoughDataError

    ncols = df.shape[1]
    weights = weights.split(sep=",")
    weights = [float(i) for i in weights]
    impacts = impacts.split(sep=",")

    for i in impacts:
        if i != '+' and i != '-':
            raise ImpactValueError

    # print(ncols)
    # print(weights, impacts)
    if len(weights) < ncols-1 or len(impacts) < ncols-1:
        raise ColsNotEqualError

    # 1 to ncols: only numeric values
    # print(df.info())

    # only numeric data
    data = df.iloc[:, 1:]
    # print(data)

    #  root of sum of square
    rss = data.apply( lambda x: np.sqrt(np.sum(np.power(x, 2))) , axis=0)
    # print(rss)

    # reduces bias, brings every value to same scale.
    normalized_data = data/rss
    # print(normalized_data)

    weighted_normalized_data = weights * normalized_data
    # print(weighted_normalized_data)

    cols_min = weighted_normalized_data.apply(np.min, axis=0)
    cols_max = weighted_normalized_data.apply(np.max, axis=0)
    # print(cols_min)
    # print(cols_max)

    ideal_best = []
    ideal_worst = []
    for i in range(ncols-1):
        if impacts[i] == '+':
            ideal_best.append(cols_max[i])
            ideal_worst.append(cols_min[i])
        else:
            ideal_best.append(cols_min[i])
            ideal_worst.append(cols_max[i])
    
    # print(ideal_worst)
    # print(ideal_best)

    # print(weighted_normalized_data.apply(lambda x: print(x), axis=1))

    Smin = weighted_normalized_data.apply(lambda x: np.sqrt(np.sum(np.power(x - ideal_worst, 2))), axis=1)
    Smax = weighted_normalized_data.apply(lambda x: np.sqrt(np.sum(np.power(x - ideal_best, 2))), axis=1)
    # print(Smin) 
    # print(Smax)

    perfScore = Smin / (Smin + Smax)
    # print(perfScore)

    rank = (pd.DataFrame(perfScore).rank(method='max', ascending=False)).astype(int)
    # rank = np.argsort(perfScore)

    df['TopsisScore'] = perfScore
    df['Rank'] = rank

    if output_path.split(sep=".")[-1] == 'csv':
        df.to_csv(output_path, sep="\t", index=False)
    elif output_path.split(sep=".")[-1] == 'xlsx':
        df.to_excel(output_path, index=False)
    else:
        raise UnsupportedFileError

    print(df)

except CLIError:
    print("Plese upload dataset, weights vector, impact vector and an output file.")

except UnsupportedFileError:
    print("Unsupported file format. Try uploading csv or xslx")

except ColsNotEqualError:
    print("Length of weights or impacts != number of cols in dataset")

except NotEnoughDataError:
    print("Dataset does not contain enough data. The data must be atleast 3 rows and 3 cols.")

except ImpactValueError:
    print("Unknown symbol encountered. Values allowed in impact vectors are: + or -")

except Exception as e:
    print("Error occured.", e)
