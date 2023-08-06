import numpy as np
import pandas as pd
import sys


def main(*argv):
    try:
        if len(argv) < 4:
            raise Exception("Pass 4 arguments: data_path, weights, impacts, output_path")

        file = argv[0]
        weight = argv[1]
        impacts = argv[2]
        output_path = argv[3]

        format = str(file).split(sep='.')[-1]

        if format == 'xlsx':
            df = pd.read_excel(file, index_col=None)
            df.to_csv('102197016-data.csv', encoding='utf-8', index=False)
        elif format == 'csv':
            df = pd.read_csv(file)
        else:
            raise Exception("Unsupported file format. Try uploading .xls, .xlsx, .csv only")


        if df.shape[0] < 3 or df.shape[1] < 3:
            raise Exception("Dataset must contain 3 rows and 3 columns")

        ncols = df.shape[1]
        weight = weight.split(sep=",")
        weights = []
        for i in weight:
            try:
                if float(i):
                    weights.append(float(i))
            except:
                raise Exception("Only numeric values for weights are allowed.")

        impacts = impacts.split(sep=",")

        for i in impacts:
            if i != '+' and i != '-':
                raise Exception("Impacts must contain + or - values only.")

        if len(weights) < ncols-1 or len(impacts) < ncols-1:
            raise Exception("Length of weights must equal impacts, and it must be equal to columns of dataset.")

        data = df.iloc[:, 1:]
        rss = data.apply( lambda x: np.sqrt(np.sum(np.power(x, 2))) , axis=0)
        normalized_data = data/rss

        weighted_normalized_data = weights * normalized_data

        cols_min = weighted_normalized_data.apply(np.min, axis=0)
        cols_max = weighted_normalized_data.apply(np.max, axis=0)

        ideal_best = []
        ideal_worst = []
        for i in range(ncols-1):
            if impacts[i] == '+':
                ideal_best.append(cols_max[i])
                ideal_worst.append(cols_min[i])
            else:
                ideal_best.append(cols_min[i])
                ideal_worst.append(cols_max[i])

        Smin = weighted_normalized_data.apply(lambda x: np.sqrt(np.sum(np.power(x - ideal_worst, 2))), axis=1)
        Smax = weighted_normalized_data.apply(lambda x: np.sqrt(np.sum(np.power(x - ideal_best, 2))), axis=1)

        perfScore = Smin / (Smin + Smax)

        rank = (pd.DataFrame(perfScore).rank(method='max', ascending=False)).astype(int)

        df['TopsisScore'] = perfScore
        df['Rank'] = rank

        if output_path.split(sep=".")[-1] == 'csv':
            df.to_csv(output_path, sep="\t", index=False)
        elif output_path.split(sep=".")[-1] == 'xlsx':
            df.to_excel(output_path, index=False)
        else:
            raise Exception("Output file must be .csv or .xls, .xlsx")
        print(df)

    except Exception as e:
        print("Error occured.", e)

if __name__ == "__main__":
    main()
