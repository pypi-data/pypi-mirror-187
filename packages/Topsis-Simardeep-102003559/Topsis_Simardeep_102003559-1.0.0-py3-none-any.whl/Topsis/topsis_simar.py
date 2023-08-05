import numpy as np
import pandas as pd
import sys

class col_numeric(Exception):
    pass
class ParameterError(Exception):
    pass


class columnError(Exception):
    pass


class weight_impact_error(Exception):
    pass


class impact_value_error(Exception):
    pass


class comma_error(Exception):
    pass


def normalize(df):
    shape = df.shape
    for i in range(0, shape[1]):
        res = np.sqrt(sum(pow(df.iloc[:, i].values, 2)))

        df.iloc[:, i] = df.iloc[:, i]/res


def weight_assignment(df, w_l):
    shape = df.shape
    j = 0
    for i in range(0, shape[1]):
        df.iloc[:, i] = df.iloc[:, i].values*w_l[j]
        j = j+1


def ideal_best_worst(df, impact):
    shape = df.shape
    j = 0
    # df.loc[len(df.index)] = ['Amy', 89, 93]
    V_pos = []
    V_neg = []
    for i in range(0, shape[1]):
        if (impact[j] == '+'):
            num = max(df.iloc[:, i].values)
            num1 = min(df.iloc[:, i].values)
            V_pos.append(num)
            V_neg.append(num1)

        else:
            num = min(df.iloc[:, i].values)
            num1 = max(df.iloc[:, i].values)
            V_pos.append(num)
            V_neg.append(num1)

        j = j+1
    df.loc[len(df.index)] = V_pos
    df.loc[len(df.index)] = V_neg


def euclidean(df):
    shape = df.shape
    S_pos = []
    S_neg = []
    j = 0

    for i in range(0, shape[0]-2):
        num = np.sqrt(
            sum(pow(df.iloc[i, :].values-df.iloc[shape[0]-2, :].values, 2)))
        num1 = np.sqrt(
            sum(pow(df.iloc[i, :].values-df.iloc[shape[0]-1, :].values, 2)))
        # num1=np.sqrt(sum(pow(df.iloc[i,:].values,2)-pow(df.iloc[shape[0]-1,:].values,2)))
        S_pos.append(num)
        S_neg.append(num1)
    # print(S_pos)
    # print(S_neg)

    S_pos_neg = []
    for i in range(0, len(S_pos)):
        S_pos_neg.append(S_pos[i]+S_neg[i])

    performance = []
    for i in range(0, len(S_pos)):
        performance.append(S_neg[i]/S_pos_neg[i])

    return (performance)


def main():

    try:
        if (len(sys.argv) != 5):
            raise ParameterError

        filename = sys.argv[1]
        weights = sys.argv[2]
        impact = sys.argv[3]
        result_file=sys.argv[4]

        df = pd.read_csv(filename)
        df_original = df.copy(deep=True)

        col1 = df.iloc[:, 0]
        df = df.iloc[:, 1:]
        


        shape = df_original.shape
        no_of_col = shape[1]

        no_of_col_2 = shape[1]-1
        for i in range(no_of_col_2):
           if not(df.iloc[:,i].dtype.kind in 'iufc'):
            raise col_numeric
        if ((',' in weights == False) or (',' in impact == False)):
            raise comma_error

        if (no_of_col < 3):
            raise columnError

        weight_list = list(weights.split(","))
        impact_list = list(impact.split(","))

        if (len(weight_list) != no_of_col_2 or len(impact_list) != no_of_col_2):
            raise weight_impact_error
        else:
            pass

        for i in range(0, len(impact_list)):
            if (impact_list[i] == '+' or impact_list[i] == '-'):
                pass
            else:
                raise impact_value_error

        weight_list1 = []
        for i in weight_list:
            weight_list1.append(float(i))

        normalize(df)

        weight_assignment(df, weight_list1)
        # print (df)
        ideal_best_worst(df, impact_list)
        # print(df)
        performance = euclidean(df)
        df_original['Performance'] = performance

        df_original['Rank'] = (df_original['Performance'].rank(method='max', ascending=False))
        df_original = df_original.astype({"Rank": int})
        print(df_original)
        df_original.to_csv(result_file)
        print('output csv file also generated')

    except FileNotFoundError:
        print("Input File not found")
    except col_numeric:
        print("columns from 2nd to last in csv files should only contain numeric values")
    except ValueError:
        print("Enter Correct type of value in weights or impacts")
    except ParameterError:
        print("Enter correct number of parameters")
    except columnError:
        print("Input File must contain three or more columns ")
    except weight_impact_error:
        print("Enter appropriate number of weights or impacts")
    except impact_value_error:
        print("Enter appropriate impact values")
    except comma_error:
        print("Enter weights and impacts in correct format using commas as suggested above")
