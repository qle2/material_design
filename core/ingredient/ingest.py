import re
import pubchempy as pcp
from rdkit import Chem
import ast
import time
import pandas as pd


class Ingest:
    """Objective: Clean files """
    def __init__(self, csv, active_col, inactive_col):
        self.csv = csv
        self.data = pd.read_csv(csv)
        # self.data = self.data.set_index('number')
        self.remove = ['anticavity', 'Inactive:', 'active:', 'inactive','Ingredients:', 'antigingivitis', 'ingredients',
                       'active', 'ingredient', 'antihypersensitivity',':', 'flavors','certified',
                'w/v', 'antisensitivity', 'purpose', 'toothpaste', 'w v', 'natural',  'flavor',
                       ' antisensitivity', "maximum fda sensitivity", 'organic', '&nbsp',
                       'fluoride ion', '(baking soda)', '*non GMO ?Food Grade', 'antibacterial', '0 24', '0 15',
                       'Non-GMO', 'stabilized', 'Strawberry juice and other natural flavor.', 'and', 'other',
                       '/Antiplaque.', 'functional', 'strawberry', 'coming soon', 'antigngivitis']
        self.product = self.data['number']
        # self.data = self.data.drop('number', axis=1)
        self.inactive_col = inactive_col
        self.active_col = active_col

    @staticmethod
    def removeEmptyFromList(target_list):
        final_list = []
        for fullString in target_list:
            remove_empty = [i for i in fullString if i]
            final_list.append(remove_empty)
        return final_list

    @staticmethod
    def toRealList(strList):
        return [ast.literal_eval(i) for i in strList]

    @staticmethod
    def toLower(strList):
        return [i.lower() for i in strList]

    @staticmethod
    def removeEmptyFromFrame(df, active_col, inactive_col):
        # return df[(df[active_col] != """['']""") & (df[inactive_col] != """[]""")]
        # return df.query("""{active} != '['']' & {inactive} != '[]'""".format(active=active_col, inactive=inactive_col))
        return df.loc[~((df[active_col] == "['']") & (df[inactive_col] == "[]")), :]

    def cleanActiveIngredient(self):
        data = self.data
        data = Ingest.removeEmptyFromFrame(data, self.active_col, self.inactive_col)
        self.data = data
        toList = list(data[self.active_col])
        toLower = [i.lower() for i in toList]  # Convert string to lower case
        real_list = Ingest.toRealList(toLower)

        real_list = Ingest.removeEmptyFromList(real_list)
        removed_list = []
        for inner in real_list:
            in_list = []
            for string in inner:
                for word in self.remove:
                    sentence_new = string.replace(word, '')  # Remove the extra words in self.remove
                    string = sentence_new
                in_list.append(string)
            removed_list.append(in_list)

        removed_list = Ingest.removeEmptyFromList(removed_list)

        cleaned_list = []
        for inner in removed_list:
            in_list = []
            for i in inner:
                if len(i) > 3:
                    in_list.append(i)
            cleaned_list.append(in_list)  # Remove empty string

        more_cleaning= []
        for inner in cleaned_list:
            in_list = []
            for string in inner:
                if string.find(';') != -1:
                    fix_split = string.split(';')  # Strip at ; to get compounds in the same string divided by ;
                    for i in fix_split:
                        in_list.append(i)
                elif string.find(',') != -1:
                    fix_split = string.split(',')  # Strip at ; to get compounds in the same string divided by ;
                    for i in fix_split:
                        in_list.append(i)
                elif string.find('-') != -1 and not string.startswith('peg'):
                    fix_split = string.split('-')  # Strip at ; to get compounds in the same string divided by ;
                    for i in fix_split:
                        in_list.append(i)
                elif string.find('  ') != -1:
                    fix_split = string.split('  ')  # Strip at ; to get compounds in the same string divided by ;
                    for i in fix_split:
                        in_list.append(i)
                else:
                    in_list.append(string)
            more_cleaning.append(in_list)

        active_list = []   # Clean everything that is not related to the chemical. Can be better....
        for inner in more_cleaning:
            in_list = []
            for string in inner:
                res = re.sub(r"[\{\(\[].*?[\)\]\}]|(\s\d\.\d+\%)|\W\s$|\W+$|\W\w$|^\-\s|\.+|\w\:|^\W|^\s\W\s|\s\W\s$", "", string)
                new_res = re.sub(r"^\s\W\s\W|\s\S\s$|^\s+\W\s|^\-\s|^\w\s|^\w\s\S\s\S|\d+\%|\*+|\s\d\%", "", res)
                final_res = re.sub(r"\s\d\%\S|^\S\s|^\w\s+|[\(].*|\s+$|^\s+|\.$|\s\d$|\d+\s\%|\:|\)|\s+$|\s\d+$", "", new_res)
                final_res = re.sub('  ', ' ', final_res)

                if 0 < len(final_res) < 60 and final_res != 's':
                    # pip install nltk(final_res, len(final_res))
                    in_list.append(final_res)
            active_list.append(in_list)

        active_list = Ingest.removeEmptyFromList(active_list)
        print(active_list)
        data[self.active_col] = active_list
        data = Ingest.removeEmptyFromFrame(self.data, self.active_col, self.inactive_col)
        # return active_list
        self.data = data


    def cleanInactiveIngredient(self):
        data = self.data
        data = Ingest.removeEmptyFromFrame(data, self.active_col, self.inactive_col)
        self.data = data
        ingreList = list(data[self.inactive_col])
        toLower = Ingest.toLower(ingreList)

        real_list = Ingest.toRealList(toLower)

        final_list = []
        for inner in real_list:
            in_list = []
            for string in inner:
                res = re.sub(r"\.$", '', string)
                in_list.append(res)
            final_list.append(in_list)

        data[self.inactive_col] = final_list
        data = Ingest.removeEmptyFromFrame(self.data, self.active_col, self.inactive_col)

        self.data = data
