import pandas as pd
from colorama import Fore, Back, Style

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# from pprint import pprint
# pprint(sys.path)

from edabox import DataBox

# Test on Kaggle Titanic Dataset
df = pd.read_csv('./data/titanic.csv')

# dbx = box.DataBox(df, target=[])
dbx = DataBox(df, target=['Survived'])

dbx.look_inside()

