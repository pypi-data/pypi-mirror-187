import pandas as pd

import numpy as np
from scipy import mean
from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns

from colorama import Fore, Back, Style

import copy
import re
from typing import List

from warnings import warn

# -------------------------------------------------------------------- #

foregd = Fore.CYAN
backgd = Back.BLACK
style  = Style.BRIGHT
style_reset = Style.RESET_ALL

# -------------------------------------------------------------------- #
"""
Functions
----------
    feature_vs_target()
    explore_feature()
"""
# -------------------------------------------------------------------- #

#function
def feature_vs_target() -> None:
    pass 

# function:
def explore_feature( df : pd.DataFrame,
                     feature : str | int,
                     target : List[str] | List[int] | None = None,
                     visuals : bool | None = True ) -> None:

    """
    Explores the details of a feature in the DataFrame

    Parameters
    ----------
    df : pandas.DataFrame
    feature : str or list
    target : list<str> or list<int> or None, default None
    visuals : bool or None, default True
    """
    # when feature column-name is passed
    if type(feature) == str:
        df_feat = df.loc[:,[feature]]
        feat_name = feature
    # when feature column-number is passed
    elif type(feature) == int:
        df_feat = df.iloc[:,[feature]]
        feat_name = df_feat.columns[0]

    str1a  = "-------------- Feature  : "
    str1b  = " ----------------"
    str2   = "        Feature  : "
    str3   = "--               dtype  :  "
    str4   = "-- missing value count  :  "    
    str5   = "--  unique value count  :  "

    str6   = "--                 max  :  "
    str7   = "--                 min  :  "
    str8   = "--                mean  :  "
    str9   = "--         mode, count  :  "


    # print(f"{foregd}{style}{str1}{style_reset}")
    # print(f"{foregd}{style}{str2}{feat_name}{style_reset}")
    print(f"{foregd}{style}{str1a}{feat_name}{str1b}{style_reset}")   
    
    # data-type
    feat_dtype = df_feat[feat_name].dtypes
    print(f"{foregd}{style}{str3}{feat_dtype}{style_reset}")
    
    # missing values
    dfnull = df_feat.isnull()
    n_null = sum( dfnull[feat_name] == True )
    print(f"{foregd}{style}{str4}{n_null}{style_reset}")    

    # unique values
    vals = df_feat[feat_name].unique()
    n_unique = len(vals)
    print(f"{foregd}{style}{str5}{n_unique}{style_reset}")

    # if numeric column
    if 'int' in str(feat_dtype):
        feat_max  = int(df_feat[feat_name].max())
        feat_min  = int(df_feat[feat_name].min())
        feat_mean = int(np.mean(df_feat[feat_name]))
        feat_mode, feat_mode_cnt = stats.mode(df_feat[feat_name],     
                                               keepdims=False)
    elif 'float' in str(feat_dtype):
        feat_max  = df_feat[feat_name].max()
        feat_min  = df_feat[feat_name].min()
        feat_mean = np.mean(df_feat[feat_name])
        feat_mode = stats.mode(df_feat[feat_name],
                               keepdims=False)
    if re.search('int', str(feat_dtype)) or re.search('int', str(feat_dtype)):
        print(f"{foregd}{style}{str6}{feat_max}{style_reset}")
        print(f"{foregd}{style}{str7}{feat_min}{style_reset}")
        print(f"{foregd}{style}{str8}{feat_mean}{style_reset}")
        print(f"{foregd}{style}{str9}{feat_mode}, {feat_mode_cnt}{style_reset}")
    
    




