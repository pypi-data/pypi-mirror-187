import pandas as pd

import typing

from utils import process_frame


class DataBox:
    """
    DataBox class
    
    Parameters
    ----------
    df : pandas.DataFrame
    target : list or None, default None
        For datasets, used for predictive-modelling or classification, takes the name of the 'target' columns.
        It is highly recommended to specify the 'target' columns, in order to gain better insight into the dataset. 
    id : str or int or none, default None
      Unique identifier column for each row in a dataset.
      It is highly recommended to specify the 'id' columns, in order to gain better insight into the dataset.
    """
    def __init__(self, df : pd.DataFrame,
                 target : list | None = None,
                 id : str | int | None = None):
        self.df = df
        self.target = target
        self.id = id
    
    @property
    def frame(self) -> pd.DataFrame:
        return self.df

    def get_shape(self):
        process_frame.get_shape(self.df,self.target)

    def look_inside(self):
        df = self.df

        self.get_shape()
        process_frame.explore_target(self.df, self.target)
        process_frame.explore_features(self.df, self.target)


