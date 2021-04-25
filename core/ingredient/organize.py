from core.ingredient.convert import Convert
from core.ingredient.ingest import Ingest
import pandas as pd
from collections import Counter


class Organize(Ingest, Convert):
    """Objective: Organize data """
    def __init__(self, csv, active_col, inactive_col, feat_method):
        super().__init__(csv, active_col, inactive_col)
        # self.convert = Convert()
        self.feat_method = feat_method

    @staticmethod
    def removeEmptyFromFrame(df, active_col, inactive_col):
        """Remove empty values on both ingredient columns in dataframe"""
        return df.loc[~((df[active_col] == "[]") & (df[inactive_col] == "[]")), :]

    def cleanIngredients(self):
        """Clean active and inactive ingredients"""
        self.cleanActiveIngredient()
        self.cleanInactiveIngredient()
        # self.data = Organize.removeEmptyFromFrame(self.data, self.active_col, self.in/active_col)
        # print(self.data['number'])
        # self.data = self.data.drop(['index'], axis=1)


    @staticmethod
    def ingredientToFeatureSum(df, smiles_column_name, feat_method):
        """Calculate rdkit features for ingredients and summing all of them for each product"""
        smiles_series = Convert.ingredientToSmiles(df[smiles_column_name])
        for i in list(smiles_series):
            temp_df = Convert.featurize(i, feat_method)
            # smiles_list = list(temp_df['smiles'])
            # if not temp_df.empty:
            temp_df = temp_df.drop(['smiles'], axis=1)
            sum_dict = temp_df.sum().to_dict()
            sum_dict['smiles'] = i
            dfFromDict = pd.DataFrame.from_records([sum_dict])
            cols = dfFromDict.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            dfFromDict = dfFromDict[cols]

            yield dfFromDict
            # else:
            #     pass

    def featureSumDf(self, smiles_column_name):
        # if inactive:
        """Concating pandas dataframe for each product"""
        return pd.concat(list(Organize.ingredientToFeatureSum(self.data, smiles_column_name=smiles_column_name,
                                                              feat_method=self.feat_method)))

    def combineFeatureSum(self):
        """Organize and return final dataframe with all featurization"""

        print("data length",len(self.data))
        active_df = self.featureSumDf(smiles_column_name=self.active_col)
        active_df.reset_index(inplace=True, drop=True)

        inactive_df = self.featureSumDf(smiles_column_name=self.inactive_col)
        inactive_df.reset_index(inplace=True, drop=True)

        # active_df.to_csv("active_before_concat.csv")
        # inactive_df.to_csv("inactive_before_concat.csv")

        active_smiles = active_df['smiles']
        print(active_smiles)

        self.data['active_smiles'] = list(active_smiles)
        print("inactive data length",len(inactive_df))

        inactive_smiles = inactive_df['smiles']
        self.data['inactive_smiles'] = list(inactive_smiles)

        active_df = active_df.drop(['smiles'], axis=1)
        inactive_df = inactive_df.drop(['smiles'], axis=1)

        active_records = active_df.to_dict('records')
        inactive_records = inactive_df.to_dict('records')

        final_list = []
        for active, inactive in zip(active_records, inactive_records):
            combine_dict = Counter(active) + Counter(inactive)
            final_list.append(dict(combine_dict))
        print(final_list)
        combined_df = pd.DataFrame.from_records(final_list)
        # combined_df.dropna(inplace=True, dro)
        self.data = self.data.loc[~((self.data[self.inactive_col] == 0) & (self.data[self.inactive_col] == 0)), :]
        self.data.reset_index(inplace=True, drop=True)
        # self.data.reset_index(inplace=True)
        combined_df = pd.concat([self.data, combined_df], axis=1)
        # combined_df = Organize.removeEmptyFromFrame(combined_df, 'active_from_ingredients', 'inactive_from_ingredients')
        combined_df.reset_index(inplace=True, drop=True)
        combined_df.fillna(0, inplace=True)
        # combined_df = combined_df.drop(['index'], axis=1)

        return combined_df



        