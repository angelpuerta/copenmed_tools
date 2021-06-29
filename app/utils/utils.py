from pandas import DataFrame


def list_difference(list1, list2):
    list(set(list1) - set(list2))


def build_dataframe(column: DataFrame, relationship_dic: dict):
    return column\
        .drop(column.columns.difference(relationship_dic.keys()), axis=1, errors='ignore')\
        .rename(columns=relationship_dic, inplace=False)
