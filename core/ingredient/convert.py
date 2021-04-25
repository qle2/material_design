import pandas as pd
import re
import pubchempy as pcp
from rdkit import Chem
import ast
import time
from descriptastorus.descriptors import MakeGenerator
from core.ingredient.ingest import Ingest


class Convert:
    """Objective: Convert ingredient names to smiles"""
    @staticmethod
    def __aw__(df_column, function, **props):
        """
        Wrapper function for parallel apply. Actual runs the pandas.apply on an individual CPU.
        """
        # a = df_column.apply(function, **props)
        return df_column.apply(function, **props)

    @staticmethod
    def ingredientToSmiles(df_column):
        """Using parallel apply to specidic columns in dataframe"""
        return Convert.__aw__(df_column, Convert.toSmiles)

    @staticmethod
    def toSmiles(ingreList):
        """Ingredient to SMILES"""
        compound_obj_list = []

        for string in ingreList:
            compound = pcp.get_compounds(string, 'name')
            time.sleep(1)
            if len(compound) == 0:
                    compound_obj_list.append(string)

            elif len(compound) == 1:
                compound_obj_list.append(compound[0].canonical_smiles)
            else:
                compound = [[i] for i in compound]
                compound_obj_list.append(compound[0][0].canonical_smiles)
        time.sleep(0.75)
        return str(compound_obj_list)

    @staticmethod
    def featurize(smiles_list, feat_method):
        """Featurize SMILES to rdkit features"""
        # smiles_list = [re.sub(r'^\[|\]+$|\'+', '', str(i)) for i in smiles_list]
        smiles_list = re.sub(r'^\[|\]+$|\'+', '', smiles_list)
        smiles_list = smiles_list.split(',')
        feat_sets = ['rdkit2d', 'rdkitfpbits', 'morgan3counts', 'morganfeature3counts', 'morganchiral3counts',
                     'atompaircounts']

        selected_feat = [feat_sets[i] for i in feat_method]
        generator = MakeGenerator(selected_feat)
        columns = []

        # get the names of the features for column labels
        for name, numpy_type in generator.GetColumns():
            columns.append(name)

        final_smiles_list = []
        for smiles in smiles_list:
            toMol = Chem.MolFromSmiles(smiles)
            if toMol is None:
                pass
            else:
                final_smiles_list.append(Chem.MolToSmiles(toMol))
        features = list(map(generator.process, final_smiles_list))
        df_smiles = pd.DataFrame.from_dict({'smiles': final_smiles_list})

        df_features = pd.DataFrame(features, columns=columns)
        df_smiles = df_smiles[~df_smiles.index.duplicated(keep='first')]
        df_features = df_features[~df_features.index.duplicated(keep='first')]
        if feat_method == [0]:
            feats = [val for val in columns if re.search(r'fr_|Count|Num|%s', val)]
            df_features = df_features[feats]

        final_df = pd.concat([df_smiles, df_features], axis=1)
        final_df = final_df.dropna()

        # remove the "RDKit2d_calculated = True" column(s)
        final_df = final_df.drop(list(final_df.filter(regex='_calculated')), axis=1)
        final_df = final_df.drop(list(final_df.filter(regex='[lL]og[pP]')), axis=1)
        # print(df)
        return final_df






