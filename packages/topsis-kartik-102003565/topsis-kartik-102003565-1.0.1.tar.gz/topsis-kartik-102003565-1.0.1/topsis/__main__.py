#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
import numpy as np


class ParameterError(Exception):
    pass


class LessColumns(Exception):
    pass


class DataTypeError(Exception):
    pass


class CommaError(Exception):
    pass


class IncompleteValues(Exception):
    pass


class ImpactError(Exception):
    pass


class NegativeWeights(Exception):
    pass


def normalization(df):
    matrix = df / np.sqrt(np.sum(df**2, axis=0))
    return matrix


def Idealisation(matrix, impact):
    IdealBest = np.amax(matrix*impact, axis=0).abs()
    IdealWorst = np.amin(matrix*impact, axis=0).abs()
    return IdealBest, IdealWorst


def Euclidean(matrix, IdealBest, IdealWorst):
    DistanceBest = np.sqrt(np.sum((matrix - IdealBest) ** 2, axis=1))
    DistanceWorst = np.sqrt(np.sum((matrix - IdealWorst) ** 2, axis=1))
    return DistanceBest, DistanceWorst


def calculation(df, weights, impacts):
    impact = []
    for i in impacts:
        if i == '+':
            impact.append(1)
        else:
            impact.append(-1)
    impact = np.array(impact)
    matrix = normalization(df)
    matrix = matrix*weights

    IdealBest, IdealWorst = Idealisation(matrix, impact)

    DistanceBest, DistanceWorst = Euclidean(matrix, IdealBest, IdealWorst)
    score = DistanceWorst/(DistanceWorst+DistanceBest)
    rank = score.rank(method='max', ascending=False).astype('int')
    return score, rank


def main():
    try:
        if len(sys.argv) != 5:
            raise ParameterError
        df, weights, impacts, result_file_name = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
        dfo = pd.read_csv(df)
        names = dfo.iloc[:, 0]
        df = dfo.iloc[:, 1:]
        shape = df.shape
        if shape[1] < 2:
            raise LessColumns
        for i in range(shape[1]):
            if df.iloc[:, i].dtype.kind not in 'iufc':
                raise DataTypeError
        if (',' not in weights) or (',' not in impacts):
            raise CommaError
        weights = weights.split(',')
        impacts = impacts.split(',')
        if (len(weights) != shape[1]) or (len(impacts) != shape[1]):
            raise IncompleteValues
        for i in impacts:
            if i == '+' or i == '-':
                continue
            else:
                raise ImpactError
                break
        for i in range(len(weights)):
            weights[i] = float(weights[i])
            if i < 0:
                raise NegativeWeights
        score, rank = calculation(df, weights, impacts)
        dfo['Score'] = score
        dfo['Rank'] = rank
        print(dfo)
        result_file_name = result_file_name+'.csv'
        dfo.to_csv(result_file_name, index=False)
    except FileNotFoundError:
        print("Input File not found ")
    except ParameterError:
        print("Incorrect number of parameters ")
    except LessColumns:
        print("Less than 3 columns are there ")
    except DataTypeError:
        print("Incorrect data type found ")
    except CommaError:
        print("Enter weights and impacts correctly using ',' ")
    except IncompleteValues:
        print("Wrong inputs for weights or impacts ")
    except ImpactError:
        print("Enter only '+' or '-' for impacts ")
    except NegativeWeights:
        print("Weights should be positive ")

if __name__=='__main__':
    main()
