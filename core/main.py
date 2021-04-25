import pubchempy as pcp
# from core.organize import Organize
import pandas as pd
import core
from core import ingredient
from core.ingredient.organize import Organize


# ingredient_file = "../data/toothpaste_ingredients_2021_02_12.csv"
# overview = "../data/toothpaste_overview_2020-04-01.csv"
# all1 = "../data/toothpaste_ingredient_overview2.csv"
# all2 = "../data/toothpaste_ingredient_overview_2_19_2021.csv"
new_data = "../data/ingredient/new_data_3_26_2021.csv"
# test_empty = "../scrape/test_merge_empty.csv"


def example_run(file):
    """

    :param file: Run File with ingredients
    :return: csv with cleaned ingredients and rdkit features
    """

    prod = Organize(file, 'active_from_ingredients', 'inactive_from_ingredients', feat_method=[0])
    prod.cleanIngredients()
    final_df = prod.combineFeatureSum()
    # final_df.to_csv("test_data_conversion.csv")
    final_df.to_csv("new_data_conversion_3.csv")

    # final_df.to_csv('example_3_ingre2Rdkit.csv')
    # inactive_df.reset_index(inplace=True)
    # inactive_df.to_csv("final_test.csv")


def compound_test(name):
    b = pcp.get_compounds(name, 'name')
    print(b)
    return b

def combine_df():
    df1 = pd.read_csv("final_conversion_test_2_20_2021.csv")
    df2 = pd.read_csv("new_data_conversion_2.csv")
    df = pd.concat([df1, df2], axis=0)


    df.to_csv('test_concat.csv')

def fillna():
    df = pd.read_csv("all_data_3_29_2021.csv")
    df.fillna(0, inplace=True)
    df.to_csv("all_data_3_29_2021_final.csv")


def toFindOz():
    df = pd.read_csv("withOz.csv")
    df = df[df['oz'] == "toFind"]
    df2 = pd.read_csv("../data/scrape/data_3_21_2021.csv")
    df3 = df2.merge(df, how="left", on="product")
    df3.dropna(inplace=True)
    df3.to_csv("findOz.csv")
    print(df3)


if __name__ == '__main__':
    # fillna()
    # toFindOz()
    # combine_df()
    example_run(new_data)
    # a = compound_test("SOLUM DIATOMEAE")
    # print(type(a))
    # b = string.split(',')
    # print(b)I(