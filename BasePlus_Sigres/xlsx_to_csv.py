#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd

csv_file = './BasePlus_Sigres_19062019.csv'
xlsx_file = './BasePlus_Sigres_19062019.xlsx'

# Handle errors while calling os.remove()
try:
    os.remove(csv_file)
except:
    print("Error while deleting file ", csv_file)

data_xls = pd.read_excel(xlsx_file, 'Planilha1', index_col=None)
data_xls.to_csv(csv_file, encoding='utf-8', index=False)