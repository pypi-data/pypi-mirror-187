import pandas as pd
from colorama import Fore, Back, Style

import sys

sys.path.append('./edabox/core/utils/')

import process_frame

# --------------------------------------------------------------------- #
# Test on Kaggle Titanic Dataset
df = pd.read_csv('tests/data/titanic.csv')
samples, cols = df.shape
target = ['Survived']
id = 'PassengerId'

# process_frame.get_shape(df, target=['Embarked', 'Embarked', 'globglob'])

process_frame.get_shape(df, target=['Embarked'])

process_frame.explore_target(df, target=['Survived'])

process_frame.explore_features(df, target=target, id=id)

# --------------------------------------------------------------------- #