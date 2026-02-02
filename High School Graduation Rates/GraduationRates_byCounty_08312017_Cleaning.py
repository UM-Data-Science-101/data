#### Data Source: https://catalog.data.gov/dataset/graduationrates-bycounty-08312017-4c264

import pandas as pd

df = pd.read_csv('GraduationRates_byCounty_08312017.csv')

# Remove unnecessary columns
df = df.drop(['OBJECTID', 'Shape__Area', 'Shape__Length'], axis=1)

# Drop counties with missing graduation rates
df = df.dropna(subset=['GradRate']) 

df.to_csv('GraduationRates_byCounty_08312017_Cleaned.csv', index=False)

