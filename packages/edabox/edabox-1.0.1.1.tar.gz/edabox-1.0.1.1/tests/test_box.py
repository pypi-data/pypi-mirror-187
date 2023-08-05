import pandas as pd
from colorama import Fore, Back, Style

from pprint import pprint
import sys

# sys.path.insert(0,'../edabox/core/')
sys.path.append('./edabox/core/')
import box

sys.path.append('./edabox/tests/data/')
pprint(sys.path)
# Test on Kaggle Titanic Dataset
df = pd.read_csv('tests/data/titanic.csv')

# dbx = box.DataBox(df, target=[])
dbx = box.DataBox(df, target=['Survived'])

dbx.look_inside()

