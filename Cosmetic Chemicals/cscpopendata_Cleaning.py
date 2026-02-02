#### Data Source: https://catalog.data.gov/dataset/chemicals-in-cosmetics-d55bf

import pandas as pd

df = pd.read_csv('cscpopendata.csv')

# Remove unnecessary columns
df = df[['ProductName',
         'CompanyId',
         'CompanyName',
         'BrandName',
         'PrimaryCategoryId',
         'PrimaryCategory',
         'SubCategoryId',
         'SubCategory',
         'ChemicalId',
         'ChemicalName',
         'ChemicalCount']]

df.to_csv('cscpopendata_Cleaned.csv', index=False)

