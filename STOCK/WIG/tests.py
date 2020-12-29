from django.test import TestCase

# Create your tests here.
from pathlib import Path
import os
import json
import pandas as pd
path = Path(__file__).parent.parent
url_data = os.path.join(path , 'data/')


data=pd.read_csv(f'{url_data}06n.csv') 
for row in data.itertuples(index=False):

    if type(row[5]) is int:
        print("volumen",row[5])

        break
         