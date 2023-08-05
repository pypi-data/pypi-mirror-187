import pandas as pd

from colorama import Fore, Back, Style

import copy
import re
from typing import List

from warnings import warn

from edabox.core.utils import process_feature

# -------------------------------------------------------------------- #

foregd = Fore.CYAN
backgd = Back.BLACK
style  = Style.BRIGHT
style_reset = Style.RESET_ALL

# -------------------------------------------------------------------- #
"""
Functions
---------
    get_shape()
    explore_target()
    explore_features()
"""
# -------------------------------------------------------------------- #

# function: 
def get_shape(df : pd.DataFrame,
              target :list | None = None,
              id : str | int | None = None ) -> None:
    samples, cols = df.shape
    """
    Displayes the Sample, Feature and Target counts inside the DataFrame

    Parameters
    ----------
    df : pandas.DataFrame
    target : list or None, default None
    id : str or int or None, default None
    """

    str1 = "======================================"
    str2 = "Samples  : "
    str3 = "Columns  : "
    str4 = "Features : "
    str5 = "Targets  : "


    print(f"{foregd}{style}{str1}{style_reset}")
    print(f"{foregd}{style}{str2}{samples}{style_reset}")    

    if target == None:
        print(f"{foregd}{style}{str3}{cols}{style_reset}")
    else:
        target_valid = {el for el in target if el in df.columns}
        ntarget = len(target_valid)

        if ntarget < len(target):
            warn("'Target' names are either not in the dataset or entered more than once")

        features = cols - ntarget 
        str_targets = str(ntarget)

        print(f"{foregd}{style}{str4}{features}{style_reset}")
        print(f"{foregd}{style}{str5}{str_targets}{style_reset}")

    # print(f"{foregd}{style}{str1}{style_reset}")


# function: 
def explore_target(df : pd.DataFrame,
                   target :list | None = None ) -> None:
    
    """
    Displays the Target column details

    Parameters
    ----------
    df : pandas.DataFrame
    target : list or None, default None
    """
    if target != None:
       target_valid = {str(el) for el in target if el in df.columns}
       ntarget = len(target_valid)

       if ntarget == 0:
        return

       if ntarget < len(target):
        warn("'Target' names are either not in the dataset or entered more than once")

       str1 = "======================================"
       str2 = "            Target Classes            "
       str3 = "Binary Classes      : "
       str4 = "Multi-label Classes : "
       str5 = "Targets  : "

       print(f"{foregd}{style}{str1}{style_reset}")
       print(f"{foregd}{style}{str2}{style_reset}")        

       dict_target_bin  = {}
       dict_target_mult = {}
       for el in target_valid:
        label_cnt = df[el].nunique()
        df_label = df[[el]].drop_duplicates()
        if label_cnt == 2:
            dict_target_bin[el] = list(df_label[el])
        elif label_cnt > 2:
            dict_target_mult[el] = list(df_label[el])

        # print(f"{foregd}{style}{str3}{style_reset}")
        for key, val in dict_target_bin.items():
            str_key_val = "" + key + ": { "
            str_labels  = " -> "
            for el in val:
                label_cnt = sum( df[key] == el )
                str_labels = str_labels + str(label_cnt) + ", "
                str_key_val = str_key_val + str(el) + ", "

            str_labels = str_labels + "end"
            str_labels = re.sub(", end", "", str_labels)

            str_key_val = str_key_val + "}"
            str_key_val = re.sub(', }', ' }', str_key_val)

            str_key_val = str_key_val + str_labels
            print(f"{foregd}{style}{str_key_val}{style_reset}")


# function: 
def explore_features(df : pd.DataFrame,
                     target : List[str] | List[int] | None = None,
                     id : str | int | None = None,
                     features : List[str] | List[int] | None = None,
                     verbose : bool | None = False ) -> None:
    """
    Explores the feature-details of the DataFrame

    Parameters
    ----------
    df : pandas.DataFrame
    target : list or None, default None
    id : str or int or None, default None
    features : list<str> or list<int> or None, default None
    """
    df_feat = copy.deepcopy(df)
    if target != None:
        # when target column-names are passed
        if type(target) == List[str]:
          df_feat = df.drop(target, axis=1)
        # when target column-names are passed
        elif type(target) == List[str]:
            pass # WIP

    if id != None:
        # when ID column-name is passed
        if type(id) == str:
            df_feat = df_feat.drop([id], axis=1)
        # when ID column-number is passed
        elif type(id) == int:
            pass # WIP            
    
    if features != None:
        # when feature column-names are passed
        if type(features) == List(str):
            features_valid = [el for el in features if el in df.columns]
            df_feat = df[features_valid]
            if len(features_valid) < len(features):
                warn("One or more 'features' are either not in the dataset or entered more than once")
        # when feature column-numbers are passed
        elif type(features) == List(int):
            pass # WIP

    for feature in df_feat.columns:
        process_feature.explore_feature(df, feature=feature)